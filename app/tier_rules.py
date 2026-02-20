from typing import Dict, List, Tuple

# Per your spec:
# base: 4 criteria, 4 benefits
# bronze: 4 + 3 = 7
# silver: 7 + 3 = 10
# gold: 10 + 10 = 20
TIER_LIMITS: Dict[str, Tuple[int, int]] = {
    "base": (4, 4),
    "bronze": (7, 7),
    "silver": (10, 10),
    "gold": (20, 20),
}

def apply_tier_limits(tier: str, items: List[dict], limit_type: str = "benefits") -> List[dict]:
    """
    Trim list of items based on tier limits.
    items should already be ranked by relevance (best first).
    """
    if tier not in TIER_LIMITS:
        raise ValueError(f"Unknown tier: {tier}")

    criteria_limit, benefit_limit = TIER_LIMITS[tier]
    limit = benefit_limit if limit_type == "benefits" else criteria_limit
    return items[:limit]
