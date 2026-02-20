#!/usr/bin/env bash
set -e

echo "Starting Qdrant + API..."
docker compose up --build -d

echo "Waiting for services..."
sleep 3

echo "Ingesting benefits..."
docker compose exec api python scripts/ingest_benefits.py

echo "Open Swagger: http://localhost:8000/docs"
