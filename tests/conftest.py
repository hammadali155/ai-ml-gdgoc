import os
from pathlib import Path

# Load real .env first so that its values aren't shadowed by setdefault
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    from dotenv import load_dotenv

    load_dotenv(env_path)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

# Required by Day 5 Settings (API_KEY has no default).
os.environ.setdefault("API_KEY", "test-key")
os.environ.setdefault("APP_NAME", "Test API")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("QDRANT_URL", "http://127.0.0.1:6333")
os.environ.setdefault("GROQ_API_KEY", "test-groq-key")

from fastapi_day4.api import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    Create one TestClient for the test session.
    Also sets required env vars so pydantic-settings doesn't fail.
    """
    return TestClient(app)
