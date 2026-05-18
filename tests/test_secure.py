from fastapi_day4.settings import get_settings


def test_secure_data_401_without_key(client):
    r = client.get("/secure-data")
    assert r.status_code == 401


def test_secure_data_200_with_key(client):
    settings = get_settings()
    r = client.get("/secure-data", headers={"X-API-Key": settings.api_key})
    assert r.status_code == 200
    assert r.json()["secret_data"] == "approved"
