from fastapi.testclient import TestClient

from fastapi_day4.api import app

client = TestClient(app)


def test_basic_health_exists():
    assert client.get("/health").status_code == 200
