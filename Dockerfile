# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Good defaults for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Copy project files first (simple approach for Day 8)
COPY . /app

# Install runtime deps
RUN python -m pip install --upgrade pip \
    && python -m pip install "fastapi[standard]" pydantic-settings

# Expose the port your API will listen on
EXPOSE 8000

# Start the API - bind to 0.0.0.0 so it is reachable outside the container
CMD ["uvicorn", "fastapi_day4.api:app", "--host", "0.0.0.0", "--port", "8000"]
