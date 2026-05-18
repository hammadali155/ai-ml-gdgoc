# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip \
    && python -m pip install \
    "fastapi[standard]" \
    pydantic-settings \
    "psycopg[binary]" \
    sqlalchemy \
    alembic \
    qdrant-client

EXPOSE 8000

CMD ["uvicorn", "fastapi_day4.api:app", "--host", "0.0.0.0", "--port", "8000"]
