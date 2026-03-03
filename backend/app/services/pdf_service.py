import fitz  # PyMuPDF
from fastapi import UploadFile
import io

class PDFService:
    """Servicio para la extracción de contenido desde archivos PDF."""
    
    @staticmethod
    def extract_text(file: UploadFile) -> str:
        """
        Lee un archivo PDF subido y extrae todo su contenido de texto.
        """
        # Leemos el contenido del archivo en memoria para evitar guardar archivos temporales
        content = file.file.read()
        pdf_document = fitz.open(stream=content, filetype="pdf")
        
        text = ""
        # Recorremos cada página y acumulamos el texto
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
            
        pdf_document.close()
        return text
