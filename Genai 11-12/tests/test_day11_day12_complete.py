import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect, select, text

from src.day11.database import AsyncSessionLocal, engine, init_db
from src.day11.db_models import RequestLog, RetrievedSourceLog
from src.day11.main import app
from src.day11.metrics import request_metrics
from src.day11.rag import rag_service


def test_day11_root_and_health():
    with TestClient(app) as client:
        root = client.get("/")
        assert root.status_code == 200
        assert root.json()["status"] == "running"
        health = client.get("/health")
        assert health.status_code == 200
        data = health.json()
        assert data["status"] == "ok"
        assert data["dependencies"] == {"database": "ready", "rag": "ready"}
        assert data["request_id"]


def test_day11_ingest_and_document_lookup():
    with TestClient(app) as client:
        response = client.post(
            "/ingest",
            json={"title": "Demo", "content": "one\n\ntwo"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["document_id"]
        assert data["chunk_count"] == 2
        assert data["status"] == "processed"

        document = client.get(f"/documents/{data['document_id']}")
        assert document.status_code == 200
        assert document.json()["chunk_count"] == 2
        assert document.json()["title"] == "Demo"


def test_day11_ask_returns_validated_answer_and_sources():
    with TestClient(app) as client:
        client.post("/ingest", json={"title": "RAG", "content": "evidence"})
        response = client.post("/ask", json={"question": "What is this?"})
        assert response.status_code == 200
        data = response.json()
        assert data["answer"]
        assert isinstance(data["sources"], list)
        assert data["sources"][0]["document_id"]
        assert "score" in data["sources"][0]


def test_openapi_has_required_endpoints_and_schemas():
    schema = app.openapi()
    assert {"/health", "/ingest", "/ask", "/documents/{document_id}"}.issubset(schema["paths"])
    schemas = schema["components"]["schemas"]
    assert {"IngestRequest", "IngestResponse", "AskRequest", "AskResponse", "DocumentResponse", "HealthResponse"}.issubset(schemas)


@pytest.mark.asyncio
async def test_day12_database_tables_and_columns():
    await init_db()
    async with engine.begin() as connection:
        tables = await connection.run_sync(lambda conn: inspect(conn).get_table_names())
    assert "request_logs" in tables
    assert "retrieved_source_logs" in tables

    async with AsyncSessionLocal() as session:
        request_columns = {row[1] for row in (await session.execute(text("PRAGMA table_info(request_logs)"))).fetchall()}
        source_columns = {row[1] for row in (await session.execute(text("PRAGMA table_info(retrieved_source_logs)"))).fetchall()}
    assert {"request_id", "endpoint", "start_time", "total_latency_ms", "model_version", "prompt_version", "outcome", "error_category"}.issubset(request_columns)
    assert {"request_id", "source_id", "score", "created_at"}.issubset(source_columns)


def test_day12_successful_request_is_traced_in_sql():
    with TestClient(app) as client:
        response = client.post("/ingest", json={"title": "Trace", "content": "content"})
        request_id = response.json()["request_id"]

    async def read_log():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(RequestLog).where(RequestLog.request_id == request_id))
            return result.scalar_one_or_none()

    record = asyncio.run(read_log())
    assert record is not None
    assert record.endpoint == "/ingest"
    assert record.outcome == "success"
    assert record.total_latency_ms >= 0
    assert record.model_version == "rag-model-v1"
    assert record.prompt_version == "prompt-v1"


def test_day12_retrieved_sources_are_logged():
    with TestClient(app) as client:
        client.post("/ingest", json={"title": "Source", "content": "evidence"})
        response = client.post("/ask", json={"question": "question"})
        request_id = response.json()["request_id"]
        source_id = response.json()["sources"][0]["document_id"]

    async def read_source_log():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(RetrievedSourceLog).where(RetrievedSourceLog.request_id == request_id))
            return result.scalar_one_or_none()

    record = asyncio.run(read_source_log())
    assert record is not None
    assert record.source_id == source_id
    assert record.score == 1.0


def test_day12_validation_error_is_consistent_and_traced():
    with TestClient(app) as client:
        response = client.post("/ingest", json={"title": "", "content": ""})
        data = response.json()
        assert response.status_code == 422
        assert data["error_code"] == "VALIDATION_ERROR"
        assert data["message"] == "Request validation failed"
        request_id = data["request_id"]

    async def read_log():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(RequestLog).where(RequestLog.request_id == request_id))
            return result.scalar_one_or_none()

    record = asyncio.run(read_log())
    assert record is not None
    assert record.outcome == "validation_error"
    assert record.error_category == "validation"


def test_day12_unknown_document_has_safe_error_and_trace():
    with TestClient(app) as client:
        response = client.get("/documents/unknown")
        data = response.json()
        assert response.status_code == 404
        assert data["error_code"] == "DOCUMENT_NOT_FOUND"
        assert data["message"] == "Document not found"
        assert "Traceback" not in response.text
        request_id = data["request_id"]

    async def read_log():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(RequestLog).where(RequestLog.request_id == request_id))
            return result.scalar_one_or_none()

    record = asyncio.run(read_log())
    assert record is not None
    assert record.outcome == "not_found"
    assert record.error_category == "not_found"


def test_day12_missing_evidence_is_safe_error():
    rag_service.documents.clear()
    with TestClient(app) as client:
        response = client.post("/ask", json={"question": "question"})
        assert response.status_code == 404
        data = response.json()
        assert data["error_code"] == "NO_EVIDENCE"
        assert data["message"] == "No evidence is available for this question"
        assert "Traceback" not in response.text


def test_day12_simulated_dependency_failure_is_500_and_safe(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("simulated provider failure")

    monkeypatch.setattr(rag_service, "ingest_document", fail)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.post("/ingest", json={"title": "x", "content": "y"})
        assert response.status_code == 500
        data = response.json()
        assert data["error_code"] == "INTERNAL_ERROR"
        assert data["message"] == "An internal server error occurred"
        assert "simulated provider failure" not in response.text
        assert "Traceback" not in response.text


def test_day12_metrics_are_updated():
    with TestClient(app) as client:
        client.get("/health")
        client.get("/documents/unknown")
        response = client.get("/metrics")
        data = response.json()
        assert data["total_requests"] >= 2
        assert data["successful_requests"] >= 1
        assert data["failed_requests"] >= 1
        assert data["average_latency_ms"] >= 0
