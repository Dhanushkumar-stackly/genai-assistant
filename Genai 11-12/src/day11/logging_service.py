from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import RequestLog, RetrievedSourceLog


MODEL_VERSION = "rag-model-v1"
PROMPT_VERSION = "prompt-v1"


async def log_request(
    session: AsyncSession,
    *,
    request_id: str,
    endpoint: str,
    start_time: datetime,
    total_latency_ms: float,
    outcome: str,
    error_category: str | None = None,
) -> None:
    session.add(
        RequestLog(
            request_id=request_id,
            endpoint=endpoint,
            start_time=start_time,
            total_latency_ms=total_latency_ms,
            model_version=MODEL_VERSION,
            prompt_version=PROMPT_VERSION,
            outcome=outcome,
            error_category=error_category,
        )
    )
    await session.commit()


async def log_retrieved_sources(
    session: AsyncSession,
    *,
    request_id: str,
    sources: list[dict],
) -> None:
    for source in sources:
        session.add(
            RetrievedSourceLog(
                request_id=request_id,
                source_id=str(source["document_id"]),
                score=source.get("score"),
                created_at=datetime.utcnow(),
            )
        )
    await session.commit()
