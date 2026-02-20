def build_recommendation_prompt(tier: str, criteria: list[str], contexts: list[dict]) -> str:
    context_text = "\n\n---\n\n".join(
        f"[source={c.get('source')} chunk={c.get('chunk_id')} score={c.get('score'):.3f}]\n{c.get('text')}"
        for c in contexts
    )

    criteria_text = "\n".join(f"- {c}" for c in criteria)

    return f"""
You are an enterprise membership-benefits recommendation assistant.

TASK:
Given a user's tier and criteria, recommend benefits ONLY from the provided knowledge base excerpts.
Do not invent benefits. If unsure, say what information is missing.

USER TIER: {tier}
USER CRITERIA:
{criteria_text}

KNOWLEDGE BASE EXCERPTS:
{context_text}

OUTPUT FORMAT (STRICT JSON):
{{
  "matched_criteria": [{{"criteria":"...", "evidence":"...", "source":"...", "chunk_id": 0}}],
  "recommended_benefits": [{{"benefit":"...", "why":"...", "evidence":"...", "source":"...", "chunk_id": 0}}],
  "rationale": "one-paragraph explanation"
}}
""".strip()
