# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

RUN python -m pip install --upgrade pip && \
    python -m pip install torch --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install \
      "fastapi[standard]" pydantic-settings "psycopg[binary]" \
      sqlalchemy alembic qdrant-client sentence-transformers groq

EXPOSE 8000
CMD ["uvicorn", "fastapi_day4.api:app", "--host", "0.0.0.0", "--port", "8000"]
