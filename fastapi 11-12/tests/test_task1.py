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


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "GenAI RAG API",
        "version": "0.1.0",
    }
def test_ingest_endpoint():
    response = client.post(
        "/ingest",
        json={
            "title": "FastAPI Document",
            "content": "FastAPI is a Python web framework.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "document_id" in data
    assert data["chunk_count"] == 1
    assert data["status"] == "processed"


def test_ingest_rejects_empty_title():
    response = client.post(
        "/ingest",
        json={
            "title": "",
            "content": "Some content",
        },
    )

    assert response.status_code == 422


def test_ingest_rejects_empty_content():
    response = client.post(
        "/ingest",
        json={
            "title": "Test",
            "content": "",
        },
    )

    assert response.status_code == 422

def test_ask_endpoint():
    client.post(
        "/ingest",
        json={
            "title": "Python Guide",
            "content": "Python is a programming language.",
        },
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is Python?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)


def test_ask_rejects_empty_question():
    response = client.post(
        "/ask",
        json={
            "question": "",
        },
    )

    assert response.status_code == 422

def test_get_document_endpoint():
    ingest_response = client.post(
        "/ingest",
        json={
            "title": "Document Metadata",
            "content": "First paragraph.\n\nSecond paragraph.",
        },
    )

    assert ingest_response.status_code == 200

    document_id = ingest_response.json()["document_id"]

    response = client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == document_id
    assert data["title"] == "Document Metadata"
    assert data["chunk_count"] == 2
    assert data["status"] == "processed"


def test_unknown_document_returns_404():
    response = client.get(
        "/documents/does-not-exist"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Document not found"
    }