from fastapi import APIRouter, HTTPException, Depends
from app.services.rag_service import RAGService
from app.llm.cohere_provider import CohereProvider
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Query and Chat"])

def get_rag_service():
    return RAGService(llm_provider=CohereProvider())

@router.post("/", response_model=ChatResponse)
async def ask_question(request: ChatRequest, rag: RAGService = Depends(get_rag_service)):
    """
    Envía una pregunta usando los documentos ya indexados.
    Recuerda: No mantiene historial de las preguntas previas.
    """
    try:
        # Aquí el Orquestador maneja todo el flujo de búsqueda vectorial y LLM
        answer = rag.ask_question(question=request.question)
        
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
