from typing import List

def simple_chunk(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Simple, reliable char-based chunker.
    """
    text = text.strip()
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        # move start forward with overlap
        start = end - overlap
        if start < 0:
            start = end
        if start >= len(text):
            break
    return chunks
