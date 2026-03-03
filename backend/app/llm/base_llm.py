from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Interfaz abstracta para proveedores de modelos de lenguaje."""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: str) -> str:
        """Genera una respuesta basada en un prompt y un contexto recuperado."""
        pass
