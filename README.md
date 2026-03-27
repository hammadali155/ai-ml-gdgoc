# AI/ML GDGoC Backend

## Overview

This repository contains a backend learning project that evolves from FastAPI basics into an AI-ready retrieval system using Postgres, Qdrant, and multilingual embeddings.

## Current Scope

The project currently supports:

- FastAPI application with documented routes
- Environment-based settings via Pydantic Settings
- Automated tests with Pytest
- Docker and Docker Compose
- Postgres with SQLAlchemy and Alembic migrations
- Qdrant vector storage
- Multilingual embeddings (paraphrase-multilingual-MiniLM-L12-v2)
- Document chunk ingestion into Qdrant

## Tech Stack

| Layer         | Technology                          |
|---------------|-------------------------------------|
| Language      | Python 3.10+                        |
| Framework     | FastAPI                             |
| Config        | Pydantic Settings                   |
| Testing       | Pytest                              |
| Containers    | Docker / Docker Compose             |
| Database      | Postgres 17                         |
| ORM           | SQLAlchemy + Alembic                |
| Vector DB     | Qdrant                              |
| Embeddings    | Sentence Transformers               |
| Linting       | Ruff + pre-commit                   |

## Repository Structure

```
README.md
Dockerfile
docker-compose.yml
pyproject.toml
.gitignore
.env.example
.pre-commit-config.yaml
alembic.ini
src/
  fastapi_day4/         # Application code
    __init__.py
    api.py              # FastAPI routes
    settings.py         # Pydantic Settings config
    db.py               # SQLAlchemy engine/session
    models.py           # ORM models
    vector_store.py     # Qdrant client helpers
    ingestion.py        # Chunking and record building
tests/                  # Automated tests
scripts/                # Runnable helper scripts
data/
  raw/                  # Source documents for ingestion
  processed/            # Exported processed data
docs/
  screenshots/          # Evidence screenshots by day
alembic/                # Alembic migration files
```

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pip install qdrant-client sentence-transformers
```

## Running the App

```bash
fastapi dev src/fastapi_day4/api.py
```

## Docker Compose Services

```bash
docker compose up -d --build
```

Services:

| Service   | Port  | Description               |
|-----------|-------|---------------------------|
| api       | 8000  | FastAPI application       |
| postgres  | 5432  | PostgreSQL 17 database    |
| qdrant    | 6333  | Qdrant vector database    |

## Ingestion Workflow

Documents are loaded from `data/raw/`, chunked into smaller passages (80 words, 20-word overlap), embedded using a multilingual sentence transformer model, and upserted into a Qdrant collection with metadata.

```bash
export PYTHONPATH=src
python scripts/day13_ingest_chunks.py
```

## Retrieval / Search Workflow

Query the ingested chunks by semantic similarity:

```bash
export PYTHONPATH=src
python scripts/day13_search_chunks.py
```

## Testing and Quality Tools

```bash
# Run tests
pytest

# Lint and format
ruff check .
ruff format .
```

## Environment Variables

| Variable          | Description                     | Default              |
|-------------------|---------------------------------|----------------------|
| `APP_NAME`        | Application display name        | FastAPI App          |
| `ENVIRONMENT`     | Deployment environment          | dev                  |
| `DEBUG`           | Enable debug mode               | false                |
| `HOST`            | API host                        | 127.0.0.1            |
| `PORT`            | API port                        | 8000                 |
| `API_KEY`         | API authentication key          | *(required)*         |
| `DATABASE_URL`    | Postgres connection string      | *(required)*         |
| `QDRANT_URL`      | Qdrant server URL               | http://127.0.0.1:6333|
| `ALLOWED_ORIGINS` | CORS allowed origins (CSV)      | *(empty)*            |

## Progress by Day

- **Day 1–3:** Setup, GitHub workflow, Python project structure
- **Day 4–5:** FastAPI, config, Pydantic Settings
- **Day 6:** Testing with Pytest
- **Day 7:** Week 1 checkpoint
- **Day 8–9:** Docker, Dockerfile, Docker Compose
- **Day 10:** Postgres, SQLAlchemy, Alembic
- **Day 11:** Qdrant basics
- **Day 12:** Multilingual embeddings baseline
- **Day 13:** Ingestion pipeline and repository cleanup

## Known Limitations

- Chunking uses a simple word-count strategy (no sentence-aware splitting)
- No query normalization or preprocessing
- No RAG response generation yet
- No evaluation dataset for retrieval quality

## Next Steps

- Add retrieval API endpoints
- Add query normalization
- Add RAG-style answer generation
- Add evaluation set for retrieval quality
