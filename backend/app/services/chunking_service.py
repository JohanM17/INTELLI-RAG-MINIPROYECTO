class ChunkingService:
    """Servicio para dividir textos largos en fragmentos manejables (chunks)."""
    
    @staticmethod
    def create_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
        """
        Divide el texto en fragmentos con un solapamiento definido.
        
        Args:
            text: El texto completo extraído del documento.
            chunk_size: Cantidad de caracteres por cada fragmento.
            chunk_overlap: Cantidad de caracteres compartidos entre fragmentos adyacentes.
            
        Returns:
            Lista de fragmentos de texto.
        """
        if not text:
            return []
            
        chunks = []
        # Cálculo del paso entre fragmentos considerando el solapamiento
        step = chunk_size - chunk_overlap
        if step <= 0:
            step = chunk_size # Prevenir bucle infinito si el solapamiento es mal configurado
            
        for i in range(0, len(text), step):
            chunk = text[i:i + chunk_size]
            # Limpiamos espacios extra en los extremos
            clean_chunk = chunk.strip()
            if clean_chunk:
                chunks.append(clean_chunk)
            
        return chunks
