from fastapi.testclient import TestClient

from src.day11.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "GenAI RAG API"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "development"
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "GenAI RAG API"
    assert data["version"] == "0.1.0"

    # Day 12 requirement
    assert "request_id" in data
    assert len(data["request_id"]) > 0


def test_health_request_id_is_unique():
    response1 = client.get("/health")
    response2 = client.get("/health")

    assert response1.status_code == 200
    assert response2.status_code == 200

    request_id_1 = response1.json()["request_id"]
    request_id_2 = response2.json()["request_id"]

    assert request_id_1 != request_id_2


def test_ingest_endpoint():
    payload = {
        "title": "Test Document",
        "content": "This is test content.",
    }

    response = client.post(
        "/ingest",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "request_id" in data
    assert len(data["request_id"]) > 0

    assert "document_id" in data
    assert "chunk_count" in data
    assert "status" in data


def test_ingest_empty_content():
    payload = {
        "title": "Empty Document",
        "content": "",
    }

    response = client.post(
        "/ingest",
        json=payload,
    )

    assert response.status_code in [200, 400, 422]