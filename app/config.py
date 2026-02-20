from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")  # openai | none

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "membership_benefits_kb")

    top_k: int = int(os.getenv("TOP_K", "6"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))

settings = Settings()
