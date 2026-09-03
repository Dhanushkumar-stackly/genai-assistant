from fastapi.testclient import TestClient

from src.day11.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "GenAI RAG API is running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "GenAI RAG API"
    assert data["version"] == "0.1.0"
    assert "request_id" in data


def test_ingest_and_get_document():
    response = client.post(
        "/ingest",
        json={
            "title": "Task 5 Document",
            "content": (
                "This is the first paragraph.\n\n"
                "This is the second paragraph."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "request_id" in data
    assert "document_id" in data
    assert data["chunk_count"] == 2
    assert data["status"] == "processed"

    document_id = data["document_id"]

    get_response = client.get(
        f"/documents/{document_id}"
    )

    assert get_response.status_code == 200

    document = get_response.json()

    assert document["document_id"] == document_id
    assert document["title"] == "Task 5 Document"
    assert document["chunk_count"] == 2
    assert document["status"] == "processed"
    assert "request_id" in document


def test_ask_endpoint():
    client.post(
        "/ingest",
        json={
            "title": "RAG Test",
            "content": "GenAI RAG testing document.",
        },
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is this document about?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "request_id" in data
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)


def test_validation_error():
    response = client.post(
        "/ingest",
        json={
            "title": "",
            "content": "",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert "request_id" in data
    assert data["error_code"] == "VALIDATION_ERROR"
    assert data["message"] == "Request validation failed"


def test_document_not_found():
    response = client.get(
        "/documents/does-not-exist"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Document not found"


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "total_requests" in data
    assert "successful_requests" in data
    assert "failed_requests" in data
    assert "average_latency_ms" in data

    assert data["total_requests"] >= 0
    assert data["successful_requests"] >= 0
    assert data["failed_requests"] >= 0
    assert data["average_latency_ms"] >= 0