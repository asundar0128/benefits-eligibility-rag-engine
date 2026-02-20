import json
from typing import Dict, Any, List
from app.config import settings
from app.rag.retrieve import retrieve_context
from app.rag.prompt import build_recommendation_prompt
from app.tier_rules import apply_tier_limits

async def generate_with_openai(prompt: str) -> str:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI generation")

    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.openai_api_key)

    resp = await client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You output strict JSON only. No markdown. No extra text."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""

def safe_json_load(s: str) -> Dict[str, Any]:
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(s[start:end+1])
    raise ValueError("Model output was not valid JSON")

async def recommend(tier: str, criteria: List[str]) -> Dict[str, Any]:
    query = f"Tier={tier}. User needs: " + "; ".join(criteria)
    contexts = await retrieve_context(query)

    # Retrieval-only mode
    if settings.llm_provider == "none":
        return {
            "matched_criteria": [{"criteria": c, "evidence": "retrieval-only mode", "source": "", "chunk_id": None} for c in criteria],
            "recommended_benefits": [],
            "rationale": "Retrieval-only mode. Set LLM_PROVIDER=openai for generated recommendations.",
            "citations": contexts
        }

    prompt = build_recommendation_prompt(tier, criteria, contexts)
    raw = await generate_with_openai(prompt)
    parsed = safe_json_load(raw)

    matched = parsed.get("matched_criteria", [])
    benefits = parsed.get("recommended_benefits", [])
    rationale = parsed.get("rationale", "")

    # Enforce tier limits (assumes items ordered by relevance)
    matched_limited = apply_tier_limits(tier, matched, limit_type="criteria")
    benefits_limited = apply_tier_limits(tier, benefits, limit_type="benefits")

    citations = []
    for b in benefits_limited:
        citations.append({
            "source": b.get("source"),
            "chunk_id": b.get("chunk_id"),
            "evidence": b.get("evidence")
        })

    return {
        "matched_criteria": matched_limited,
        "recommended_benefits": benefits_limited,
        "rationale": rationale,
        "citations": citations
    }
