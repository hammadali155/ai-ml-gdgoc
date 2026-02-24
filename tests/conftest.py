import os
import pytest
from fastapi.testclient import TestClient
from fastapi_day4.api import app

@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    Create one TestClient for the test session.
    Also sets required env vars so pydantic-settings doesn't fail.
    """
    # Required by Day 5 Settings (API_KEY has no default).
    os.environ.setdefault("API_KEY", "test-key")
    os.environ.setdefault("APP_NAME", "Test API")
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("DEBUG", "false")
    return TestClient(app)
