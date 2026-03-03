from fastapi import FastAPI
from app.core.config import settings
from app.db.qdrant_client import init_qdrant

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup_event():
    """Acciones a ejecutar cuando el servidor inicia."""
    init_qdrant()

@app.get("/")
async def root():
    """Punto de entrada principal con mensaje de bienvenida."""
    return {"message": "Bienvenido a Intelli-RAG API", "status": "online"}

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de salud del sistema."""
    return {"status": "healthy"}
