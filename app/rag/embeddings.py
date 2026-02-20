from typing import List
from app.config import settings

def embedding_dim_for(model: str) -> int:
    # Common OpenAI embedding dims:
    # text-embedding-3-small => 1536
    # text-embedding-3-large => 3072
    if model == "text-embedding-3-small":
        return 1536
    if model == "text-embedding-3-large":
        return 3072
    return 1536

async def embed_texts_openai(texts: List[str]) -> List[List[float]]:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")

    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.openai_api_key)

    resp = await client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts
    )
    return [d.embedding for d in resp.data]
