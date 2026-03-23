async def test_health_endpoint(api_client):
    response = await api_client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "malakhov-ai-digest"


async def test_health_db_endpoint(api_client):
    response = await api_client.get("/health/db")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
