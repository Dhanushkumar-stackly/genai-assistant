from fastapi.testclient import TestClient

from src.day11.main import app


client = TestClient(app)


def test_application_starts():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "GenAI RAG API"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "development"
    assert data["status"] == "running"


def test_openapi_documentation_is_available():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert data["info"]["title"] == "GenAI RAG API"
    assert data["info"]["version"] == "0.1.0"


def test_application_has_lifespan():
    assert app.router.lifespan_context is not None