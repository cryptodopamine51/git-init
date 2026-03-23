from fastapi.testclient import TestClient

from app.api.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "malakhov-ai-digest"


def test_health_db_endpoint(monkeypatch):
    async def fake_check_db_connection() -> bool:
        return True

    monkeypatch.setattr("app.api.main.check_db_connection", fake_check_db_connection)

    with TestClient(app) as client:
        response = client.get("/health/db")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
