import pytest
from sqlalchemy import select
from fastapi.testclient import TestClient
from src.day11.main import app
from src.day11.database import AsyncSessionLocal, init_db
from src.day11.db_models import RequestLog

client = TestClient(app)

@pytest.mark.asyncio
async def test_ingest_request_is_logged_with_metadata():
    await init_db()
    response = client.post('/ingest', json={'title':'Logging Task','content':'Logging content'})
    assert response.status_code == 200
    rid = response.json()['request_id']
    async with AsyncSessionLocal() as session:
        row = (await session.execute(select(RequestLog).where(RequestLog.request_id == rid))).scalar_one()
    assert row.endpoint == '/ingest'
    assert row.outcome == 'success'
    assert row.model_version == 'rag-model-v1'
    assert row.prompt_version == 'prompt-v1'
    assert row.total_latency_ms >= 0
