from fastapi import FastAPI
from app.core.config import settings
from app.db.qdrant_client import init_qdrant

# Importamos las rutas
from app.api import routes_upload, routes_chat, routes_manage

app = FastAPI(title=settings.PROJECT_NAME)

# Añadimos los sub-enrutadores a la aplicación principal
app.include_router(routes_upload.router)
app.include_router(routes_chat.router)
app.include_router(routes_manage.router)

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
