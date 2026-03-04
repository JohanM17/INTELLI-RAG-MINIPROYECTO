import uuid
from qdrant_client import models
from app.db.qdrant_client import get_qdrant_client
from app.core.config import settings
from datetime import datetime

class VectorService:
    """Capa de abstracción para todas las operaciones en Qdrant (Base de datos vectorial)."""
    
    def __init__(self):
        # Obtenemos la conexión persistente a la base local
        self.qdrant = get_qdrant_client()
        self.collection_name = settings.COLLECTION_NAME
        
    def save_vectors(self, document_id: str, filename: str, chunks: list[str], embeddings: list[list[float]]):
        """
        Almacena vectores en Qdrant junto con texto y metadata para su posterior recuperación.
        
        Args:
            document_id: ID único generado para identificar un archivo subido.
            filename: Nombre del archivo original.
            chunks: Fragmentos de texto a almacenar.
            embeddings: Vectores numéricos listos por Cohere (uno por chunk).
        """
        # Verificamos que todo coincida (mismos chunks que vectores)
        if len(chunks) != len(embeddings):
            raise ValueError("El número de chunks no coincide con el número de embeddings.")

        points = []
        upload_time = datetime.utcnow().isoformat()

        # Genera y configura estructuras PointStruct para Qdrant
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())
            
            point = models.PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "filename": filename,
                    "text": chunk,
                    "upload_timestamp": upload_time
                }
            )
            points.append(point)

        # Inserción masiva de vectores en la colección
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def delete_document(self, document_id: str):
        """Elimina vectores asociados a un document_id específico."""
        self.qdrant.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id)
                    )
                ]
            )
        )

    def list_documents(self) -> list[dict]:
        """Extrae la lista de documentos únicos almacenados."""
        # Recupera registros para procesar metadata de documentos
        records, _ = self.qdrant.scroll(
            collection_name=self.collection_name, 
            limit=1000,
            with_payload=True, 
            with_vectors=False
        )
        
        # Agrupación por document_id para evitar duplicados por chunks
        unique_docs = {}
        for record in records:
            doc_id = record.payload.get("document_id")
            if doc_id and doc_id not in unique_docs:
                unique_docs[doc_id] = {
                    "document_id": doc_id,
                    "filename": record.payload.get("filename", "Documento Sin Nombre"),
                    "upload_timestamp": record.payload.get("upload_timestamp", "")
                }
                
        return list(unique_docs.values())

    def reset_collection(self):
        """
        Elimina todos los vectores de la colección manteniendo la estructura.
        """
        self.qdrant.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter() # Filtro vacío para eliminación total
        )
