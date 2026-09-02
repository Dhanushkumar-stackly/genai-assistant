import pytest
from sqlalchemy import inspect, select, text

from src.day11.database import (
    AsyncSessionLocal,
    engine,
    init_db,
)
from src.day11.db_models import RequestLog
from src.day11.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


@pytest.mark.asyncio
async def test_database_tables_are_created():
    await init_db()

    async with engine.begin() as connection:
        tables = await connection.run_sync(
            lambda sync_connection: inspect(
                sync_connection
            ).get_table_names()
        )

    assert "request_logs" in tables
    assert "retrieved_source_logs" in tables


@pytest.mark.asyncio
async def test_request_log_table_columns():
    await init_db()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("PRAGMA table_info(request_logs)")
        )

        columns = {
            row[1]
            for row in result.fetchall()
        }

    expected_columns = {
        "id",
        "request_id",
        "endpoint",
        "start_time",
        "total_latency_ms",
        "model_version",
        "prompt_version",
        "outcome",
        "error_category",
    }

    assert expected_columns.issubset(columns)


@pytest.mark.asyncio
async def test_retrieved_source_table_columns():
    await init_db()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text(
                "PRAGMA table_info(retrieved_source_logs)"
            )
        )

        columns = {
            row[1]
            for row in result.fetchall()
        }

    expected_columns = {
        "id",
        "request_id",
        "source_id",
        "score",
        "created_at",
    }

    assert expected_columns.issubset(columns)


def test_health_returns_request_id():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "request_id" in data
    assert len(data["request_id"]) > 0


def test_ingest_returns_request_id():
    response = client.post(
        "/ingest",
        json={
            "title": "Logging Test",
            "content": "This tests request logging.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "request_id" in data
    assert len(data["request_id"]) > 0
    assert data["status"] == "processed"


@pytest.mark.asyncio
async def test_request_id_is_stored_in_sql():
    response = client.post(
        "/ingest",
        json={
            "title": "SQL Logging Test",
            "content": "Testing SQL request logging.",
        },
    )

    assert response.status_code == 200

    request_id = response.json()["request_id"]

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RequestLog).where(
                RequestLog.request_id == request_id
            )
        )

        record = result.scalar_one_or_none()

    assert record is not None
    assert record.request_id == request_id
    assert record.endpoint == "/ingest"
    assert record.outcome == "success"
    assert record.total_latency_ms >= 0
    assert record.model_version == "rag-model-v1"
    assert record.prompt_version == "prompt-v1"