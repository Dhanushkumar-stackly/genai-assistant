from fastapi.testclient import TestClient

from src.day11.main import app


client = TestClient(app)


def test_application_starts():
    response = client.get("/health")

    assert response.status_code == 200


def test_health_response_shape():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "GenAI Assistant API"
    assert data["version"] == "1.0.0"