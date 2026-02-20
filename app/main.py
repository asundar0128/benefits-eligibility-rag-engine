from fastapi import FastAPI, HTTPException
from app.models import UserProfile, RecommendationResponse
from app.rag.recommend import recommend
from app.config import settings

app = FastAPI(
    title="Tiered Membership RAG Recommendation Engine",
    version="0.1.0",
    description="Tier-based RAG recommendation system for membership benefits (Base/Bronze/Silver/Gold)."
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "collection": settings.qdrant_collection,
        "qdrant_url": settings.qdrant_url
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_endpoint(profile: UserProfile):
    try:
        result = await recommend(profile.tier, profile.criteria)
        return RecommendationResponse(
            user_id=profile.user_id,
            tier=profile.tier,
            matched_criteria=result.get("matched_criteria", []),
            recommended_benefits=result.get("recommended_benefits", []),
            rationale=result.get("rationale", ""),
            citations=result.get("citations", []),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
