# Tiered Membership RAG Recommendation Engine (Base/Bronze/Silver/Gold)

Enterprise-style Retrieval-Augmented Generation (RAG) backend that recommends membership benefits using a knowledge base stored in a vector database (Qdrant).  
Designed for recruiter demos: clear API, tier-based limits, and evidence/citations.

## What it does
- Ingests a benefits document into **Qdrant** using embeddings.
- Accepts a user profile:
  - `tier`: base | bronze | silver | gold
  - `criteria`: list of needs/preferences
- Retrieves relevant knowledge chunks and returns:
  - matched criteria with evidence
  - recommended benefits grounded in KB
  - rationale
  - citations (source + chunk_id)

## Tier limits (per spec)
- Base: 4 criteria / 4 benefits
- Bronze: 7 criteria / 7 benefits
- Silver: 10 criteria / 10 benefits
- Gold: 20 criteria / 20 benefits

## Architecture
FastAPI → Qdrant retrieval → (optional) LLM generation → tier-limited recommendations + citations.

Add screenshots to `assets/`:
- `assets/architecture.png`
- `assets/demo_swagger.png`
- `assets/demo_recommendation.png`

---

## Tech stack
- FastAPI (REST API)
- Qdrant (vector database)
- OpenAI embeddings + optional OpenAI generation
- Docker / docker-compose
- pytest

---

## Quickstart (Docker)
### 1) Clone + configure env
```bash
git clone <your_repo_url>
cd tiered-membership-rag-recommendation-engine
cp .env.example .env

2) Start services
```bash
docker compose up --build -d
3) Ingest the benefits KB
```bash
docker compose exec api python scripts/ingest_benefits.py
4) Open Swagger UI
```bash
http://localhost:8000/docs
