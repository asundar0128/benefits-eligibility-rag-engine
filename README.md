# Tiered Membership RAG Recommendation Engine

Enterprise-Style Retrieval-Augmented Generation (RAG) Backend

An enterprise-grade Retrieval-Augmented Generation (RAG) system that recommends membership benefits based on tier (Base, Bronze, Silver, Gold) using a knowledge base stored in Qdrant.

Designed for technical recruiter demos and AI infrastructure interviews: clean architecture, tier-based constraints, grounded outputs, and citation-backed recommendations.

## Overview
This system ingests structured benefit documentation into a vector database and exposes a FastAPI endpoint that:

- Accepts a user profile (tier + criteria)

- Retrieves relevant knowledge chunks

- Applies tier-based limits

- Returns evidence-backed recommendations

- Includes rationale and citations

All recommendations are grounded in the knowledge base.

## Key Features
- Vector search powered by Qdrant
- OpenAI embeddings for semantic retrieval
- Tier-based recommendation limits
- Evidence-backed outputs with citations
- FastAPI REST interface
- Dockerized for easy deployment
- Pytest-ready test structure

## Tier Limits (Business Logic)
| Tier   | Max Criteria | Max Benefits |
| ------ | ------------ | ------------ |
| Base   | 4            | 4            |
| Bronze | 7            | 7            |
| Silver | 10           | 10           |
| Gold   | 20           | 20           |

The API automatically enforces limits per tier.

## Architecture

FastAPI → Qdrant (vector retrieval) → Optional LLM generation → Tier enforcement → Structured response with citations

<img width="1024" height="1536" alt="ChatGPT Image Feb 22, 2026, 11_24_22 AM" src="https://github.com/user-attachments/assets/619ce1ca-443b-4964-941b-68dc05b7966d" />


## Tech stack

- FastAPI
- Qdrant (Vector Database)
- OpenAI Embeddings
- Optional OpenAI Generation
- Docker / Docker Compose
- Pytest

---

## Project Structure
.
├── app/
│   ├── main.py
│   ├── retrieval.py
│   ├── recommendation.py
│   └── tier_logic.py
├── scripts/
│   └── ingest_benefits.py
├── assets/
│   ├── architecture.png
│   ├── demo_swagger.png
│   └── demo_recommendation.png
├── docker-compose.yml
├── Dockerfile
└── README.md


## Quickstart (Docker)

### 1) Clone and configure environment

git clone https://github.com/asundar0128/tiered-membership-rag-recommendation-engine
cd tiered-membership-rag-recommendation-engine
cp .env.example .env

Add your OpenAI API key to .env.

### 2) Start services

docker compose up --build -d

### 3) Ingest the benefits knowledge base

docker compose exec api python scripts/ingest_benefits.py

This loads benefit documents into Qdrant with embeddings.

### 4) Open Swagger UI

http://localhost:8000/docs

<img width="1024" height="1536" alt="ChatGPT Image Feb 22, 2026, 11_26_30 AM" src="https://github.com/user-attachments/assets/68421f12-bd46-402d-a597-1a82b4550a68" />

## API Example

- Request

POST /recommend

{
  "tier": "silver",
  "criteria": [
    "childcare support",
    "mental health coverage",
    "remote work flexibility",
    "education reimbursement"
  ]
}

- Response

{
  "tier": "silver",
  "matched_criteria": [...],
  "recommended_benefits": [...],
  "rationale": "...",
  "citations": [
    {
      "source": "benefits_guide.pdf",
      "chunk_id": "chunk_12"
    }
  ]
}

All outputs are grounded in retrieved documents.

## Environment Variables

OPENAI_API_KEY=your_key_here
QDRANT_HOST=qdrant
QDRANT_PORT=6333

## Why This Project Matters

This repository demonstrates:

- Enterprise-style RAG architecture

- Retrieval grounding with citations

- Business rule enforcement (tier constraints)

- Clean API design for production systems

- Dockerized reproducibility

It is intentionally structured to reflect production backend AI systems used in recommendation, eligibility, and benefits platforms.

## Future Enhancements

- Multi-tenant support

- Role-based access controls

- Caching layer (Redis)

- Streaming responses

- Observability (OpenTelemetry)

- Deployment to cloud (AWS/GCP/Azure)



