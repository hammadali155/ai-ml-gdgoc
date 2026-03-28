from fastapi.testclient import TestClient

from fastapi_day4.api import app

client = TestClient(app)


def test_rag_endpoint_returns_success() -> None:
    response = client.post(
        "/rag",
        json={"question": "What does Qdrant do?", "limit": 3},
    )
    assert response.status_code == 200
    body = response.json()
    assert "question" in body
    assert "answer" in body
    assert "sources" in body


def test_rag_endpoint_rejects_empty_question() -> None:
    response = client.post(
        "/rag",
        json={"question": "", "limit": 3},
    )
    assert response.status_code == 400
