import cohere
from app.core.config import settings

class EmbeddingService:
    """Clase encargada de interactuar con el modelo de embeddings de Cohere."""
    
    def __init__(self):
        self.co_client = cohere.Client(api_key=settings.COHERE_API_KEY)
        # Modelo v3.0 optimizado para recuperación de información (RAG)
        self.model_name = "embed-english-v3.0"

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Toma una lista de textos y usa Cohere para convertirlos
        en vectores numéricos.
        
        Args:
            texts: Lista de fragmentos (chunks) a vectorizar.
            
        Returns:
            Lista de vectores numéricos, donde cada vector corresponde
            a un fragmento de la lista de entrada.
        """
        # Protegemos contra listas vacías
        if not texts:
            return []
            
        response = self.co_client.embed(
            texts=texts,
            model=self.model_name,
            # Para búsquedas en documentos RAG, el tipo de imputs suele ser search_document
            input_type="search_document" 
        )
        
        return response.embeddings
