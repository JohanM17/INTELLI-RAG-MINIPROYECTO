from pydantic import BaseModel, Field

# --- Respuestas genéricas ---

class UploadResponse(BaseModel):
    """Modelo de Pydantic para la respuesta exitosa al subir un PDF."""
    message: str
    document_id: str
    filename: str
    chunks_created: int

# --- Solicitudes y Respuestas de Chat ---

class ChatRequest(BaseModel):
    """Modelo de Pydantic para validar la pregunta entrante del usuario."""
    # Usamos Field(...) para documentar y validar el contenido
    question: str = Field(..., description="La pregunta que deseas hacerle a los documentos.")

class ChatResponse(BaseModel):
    """Modelo de Pydantic para devolver las respuestas y meta-información al usuario."""
    answer: str
    # Opcional: Podríamos retornar en qué documentos se basó
    # documents_used: list[str]

# --- Solicitudes Administrativas ---

class ActionResponse(BaseModel):
    """Modelo estándar de éxito para borrados o reseteos."""
    message: str
