from pydantic import BaseModel, Field
from typing import Literal, List, Dict, Any

Tier = Literal["base", "bronze", "silver", "gold"]

class UserProfile(BaseModel):
    user_id: str = Field(..., examples=["u_001"])
    tier: Tier
    criteria: List[str] = Field(..., description="User criteria/needs/preferences (strings).")

class RecommendationResponse(BaseModel):
    user_id: str
    tier: Tier
    matched_criteria: List[Dict[str, Any]]
    recommended_benefits: List[Dict[str, Any]]
    rationale: str
    citations: List[Dict[str, Any]]
