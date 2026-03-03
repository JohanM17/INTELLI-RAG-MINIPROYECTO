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

        # Iteramos simultáneamente a través de fragmentos y vectores usando zip()
        for chunk, embedding in zip(chunks, embeddings):
            # Qdrant requiere un ID numérico o UUID formato string para cada punto
            point_id = str(uuid.uuid4())
            
            # Configuramos el "Punto" a la estructura de Qdrant
            point = models.PointStruct(
                id=point_id,
                vector=embedding, # Los 4096 números
                # Payload es la metadata; aquí viven nuestro texto original y datos del archivo
                payload={
                    "document_id": document_id,
                    "filename": filename,
                    "text": chunk, # Esto es lo que la IA leerá luego
                    "upload_timestamp": upload_time
                }
            )
            points.append(point)

        # Enviamos el bulto completo de vectores (upsert crea si no existe o reemplaza si existen ids conflictivos)
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points
        )
