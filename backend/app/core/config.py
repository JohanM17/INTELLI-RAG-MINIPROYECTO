import os
from dotenv import load_dotenv

# Carga de variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    """Configuración global de la aplicación."""
    PROJECT_NAME: str = "Intelli-RAG API"
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    QDRANT_PATH: str = os.getenv("QDRANT_PATH", "./qdrant_storage")
    
    # Configuración del sistema RAG
    COLLECTION_NAME: str = "documents"
    VECTOR_SIZE: int = 1024  # Dimensión real para el modelo Cohere embed-english-v3.0

settings = Settings()
