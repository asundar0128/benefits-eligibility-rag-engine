from typing import Dict, Any
from app.config import settings
from app.utils.text_splitter import simple_chunk
from app.rag.qdrant_client import get_qdrant, ensure_collection
from app.rag.embeddings import embed_texts_openai, embedding_dim_for

async def ingest_markdown(markdown_text: str, source: str = "benefits.md") -> Dict[str, Any]:
    chunks = simple_chunk(markdown_text, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        return {"chunks": 0, "status": "no_text"}

    vectors = await embed_texts_openai(chunks)
    dim = embedding_dim_for(settings.openai_embedding_model)

    qdrant = get_qdrant()
    ensure_collection(qdrant, dim)

    points = []
    for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
        points.append({
            "id": i,
            "vector": vec,
            "payload": {
                "text": chunk,
                "source": source,
                "chunk_id": i
            }
        })

    qdrant.upsert(collection_name=settings.qdrant_collection, points=points)
    return {"chunks": len(chunks), "status": "ok", "collection": settings.qdrant_collection}
