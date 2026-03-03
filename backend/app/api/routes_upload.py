from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.services.rag_service import RAGService
from app.llm.cohere_provider import CohereProvider
from app.models.schemas import UploadResponse

router = APIRouter(prefix="/upload", tags=["Upload Documents"])

# Dependency Injection para instanciar el servicio con Cohere
def get_rag_service():
    return RAGService(llm_provider=CohereProvider())

@router.post("/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...), rag: RAGService = Depends(get_rag_service)):
    """
    Sube un documento PDF. El sistema lo leerá, dividirá, 
    creará los embeddings y lo guardará en Qdrant.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF válido.")
        
    try:
        # Aquí el Orquestador hace todo el trabajo pesado
        result = rag.process_and_store_pdf(file)
        return UploadResponse(
            message="Documento procesado e indexado con éxito.",
            document_id=result["document_id"],
            filename=result["filename"],
            chunks_created=result["chunks_created"]
        )
    except Exception as e:
        # Capturamos cualquier error en el flujo
        raise HTTPException(status_code=500, detail=str(e))
