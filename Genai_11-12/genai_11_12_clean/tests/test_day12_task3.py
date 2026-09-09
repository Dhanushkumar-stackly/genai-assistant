import pytest
from sqlalchemy import select
from fastapi.testclient import TestClient
from src.day11.main import app
from src.day11.database import AsyncSessionLocal, init_db
from src.day11.db_models import RetrievedSourceLog

client = TestClient(app)

@pytest.mark.asyncio
async def test_ask_logs_retrieved_sources():
    await init_db()
    ingest = client.post('/ingest', json={'title':'Source Log Test','content':'Source content'})
    document_id = ingest.json()['document_id']
    response = client.post('/ask', json={'question':'What is this about?'})
    assert response.status_code == 200
    rid = response.json()['request_id']
    async with AsyncSessionLocal() as session:
        row = (await session.execute(select(RetrievedSourceLog).where(RetrievedSourceLog.request_id == rid))).scalars().first()
    assert row is not None
    returned_source_id = response.json()['sources'][0]['document_id']
    assert row.source_id == returned_source_id
    assert row.score == 1.0
