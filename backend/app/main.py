from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
async def root():
    """Punto de entrada principal con mensaje de bienvenida."""
    return {"message": "Bienvenido a Intelli-RAG API", "status": "online"}

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de salud del sistema."""
    return {"status": "healthy"}
