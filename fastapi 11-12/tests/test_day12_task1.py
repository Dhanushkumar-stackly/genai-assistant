import pytest
from sqlalchemy import inspect, text

from src.day11.database import AsyncSessionLocal, engine, init_db


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