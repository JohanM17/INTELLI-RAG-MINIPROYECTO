from fastapi import APIRouter, HTTPException, Depends
from app.services.vector_service import VectorService
from app.models.schemas import ActionResponse

# Las definimos sin prefijo porque las agruparemos por separado en main.py o aquí mismo
router = APIRouter(tags=["Manage Documents"])

def get_vector_service():
    return VectorService()

@router.get("/documents", response_model=list[dict])
async def get_documents(vector_db: VectorService = Depends(get_vector_service)):
    """
    Obtiene todos los documentos guardados en Qdrant.
    """
    try:
        return vector_db.list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/document/{document_id}", response_model=ActionResponse)
async def delete_document(document_id: str, vector_db: VectorService = Depends(get_vector_service)):
    """
    Elimina los fragmentos y vectores de un documento específico 
    de la base de datos usando su document_id.
    """
    try:
        vector_db.delete_document(document_id=document_id)
        return ActionResponse(message=f"Documento con ID {document_id} eliminado exitosamente de Qdrant.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reset", response_model=ActionResponse)
async def reset_database(vector_db: VectorService = Depends(get_vector_service)):
    """
    Realiza la limpieza total de la base de datos vectorial.
    """
    try:
        vector_db.reset_collection()
        return ActionResponse(message="La base de datos vectorial Qdrant ha sido vaciada y reseteada.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
