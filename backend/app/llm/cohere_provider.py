import cohere
from app.llm.base_llm import BaseLLM
from app.core.config import settings

class CohereProvider(BaseLLM):
    """Implementación del proveedor de LLM usando Cohere."""
    
    def __init__(self):
        self.client = cohere.Client(api_key=settings.COHERE_API_KEY)

    def generate_response(self, prompt: str, context: str) -> str:
        # Construcción del prompt siguiendo las reglas del RAG
        full_prompt = f"""
        Usa el siguiente contexto para responder a la pregunta del usuario. 
        Si la información no está en el contexto, di que no encontraste información relevante.
        No inventes datos. No tienes memoria de conversaciones anteriores.

        CONTEXTO:
        {context}

        PREGUNTA:
        {prompt}

        RESPUESTA:
        """
        response = self.client.chat(
            message=full_prompt,
            temperature=0.3 # Baja temperatura para respuestas más precisas y menos creativas
        )
        
        return response.text.strip()
