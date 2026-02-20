from typing import List, Dict, Any
from app.config import settings
from app.rag.qdrant_client import get_qdrant
from app.rag.embeddings import embed_texts_openai

async def retrieve_context(query: str, top_k: int | None = None) -> List[Dict[str, Any]]:
    top_k = top_k or settings.top_k
    qdrant = get_qdrant()

    [q_vec] = await embed_texts_openai([query])
    hits = qdrant.search(
        collection_name=settings.qdrant_collection,
        query_vector=q_vec,
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )

    results = []
    for h in hits:
        payload = h.payload or {}
        results.append({
            "score": float(h.score),
            "text": payload.get("text", ""),
            "source": payload.get("source", ""),
            "chunk_id": payload.get("chunk_id", None)
        })
    return results
