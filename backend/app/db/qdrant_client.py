from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings

# Patrón Singleton: Mantenemos una única instancia viva en memoria
# para evitar que Qdrant bloquee la carpeta al intentar abrirla múltiples veces.
_qdrant_client = None

def get_qdrant_client() -> QdrantClient:
    """ Inicializa y retorna el cliente de Qdrant con persistencia local (Singleton). """
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(path=settings.QDRANT_PATH)
    return _qdrant_client

def init_qdrant():
    """ 
    Asegura que la colección necesaria exista en Qdrant.
    Si no existe, la crea con la configuración de vectores adecuada.
    """
    client = get_qdrant_client()
    
    # Verificamos si la colección ya existe
    collections = client.get_collections().collections
    exists = any(c.name == settings.COLLECTION_NAME for c in collections)
    
    if not exists:
        print(f"Creando colección: {settings.COLLECTION_NAME}")
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=settings.VECTOR_SIZE, 
                distance=models.Distance.COSINE
            ),
        )
    else:
        print(f"La colección '{settings.COLLECTION_NAME}' ya existe.")
