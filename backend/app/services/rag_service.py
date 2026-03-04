import uuid
from fastapi import UploadFile
from app.services.pdf_service import PDFService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.llm.base_llm import BaseLLM

class RAGService:
    """
    Orquestador principal del sistema RAG. 
    Coordina la interacción entre PDFs, Chunks, Embeddings, Vector DB y el LLM.
    """
    def __init__(self, llm_provider: BaseLLM):
        # Inyectamos la dependencia del LLM (Patrón Strategy implementado)
        self.llm = llm_provider
        
        # Instanciamos los demás servicios
        self.pdf_service = PDFService()
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def process_and_store_pdf(self, file: UploadFile) -> dict:
        """Flujo completo: PDF -> Texto -> Chunks -> Embeddings -> Qdrant"""
        # 1. Extraer Texto
        text = self.pdf_service.extract_text(file)
        
        # 2. Dividir en Chunks
        chunks = self.chunking_service.create_chunks(text)
        
        # 3. Generar Embeddings para todos los chunks
        embeddings = self.embedding_service.create_embeddings(chunks)
        
        # 4. Guardar en Base de Datos Vectorial
        doc_id = str(uuid.uuid4())
        self.vector_service.save_vectors(
            document_id=doc_id,
            filename=file.filename,
            chunks=chunks,
            embeddings=embeddings
        )
        
        return {
            "document_id": doc_id,
            "filename": file.filename,
            "chunks_created": len(chunks)
        }

    def ask_question(self, question: str, top_k: int = 3) -> str:
        """
        Ejecuta el flujo de consulta RAG.
        """
        # Vectorización de la consulta del usuario
        question_embedding = self.embedding_service.co_client.embed(
            texts=[question],
            model=self.embedding_service.model_name,
            input_type="search_query"
        ).embeddings[0]

        # Búsqueda de fragmentos por similitud vectorial
        search_result = self.vector_service.qdrant.query_points(
            collection_name=self.vector_service.collection_name,
            query=question_embedding,
            limit=top_k
        ).points

        # Reconstrucción del contexto basado en resultados relevantes
        context_chunks = []
        for hit in search_result:
            if hit.score > 0.2: 
                context_chunks.append(hit.payload["text"])
                
        context = "\n\n---\n\n".join(context_chunks)

        # Generación de respuesta final mediante el LLM
        return self.llm.generate_response(prompt=question, context=context)
