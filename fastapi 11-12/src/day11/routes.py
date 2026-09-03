import time
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from .config import Settings, get_settings
from .database import get_db
from .logging_service import log_request
from .metrics import request_metrics
from .models import (
    AskRequest,
    AskResponse,
    DocumentResponse,
    IngestRequest,
    IngestResponse,
    Source,
)
from .rag import RAGService, get_rag_service


router = APIRouter()


@router.get("/", response_model=dict[str, str])
def root(
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    return {
        "message": "GenAI RAG API is running",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }


@router.post("/ingest", response_model=IngestResponse)
async def ingest(
    request: IngestRequest,
    rag: RAGService = Depends(get_rag_service),
    db=Depends(get_db),
) -> IngestResponse:

    request_id = str(uuid4())
    start_time = datetime.now(timezone.utc)
    start_counter = time.perf_counter()

    result = rag.ingest_document(
        title=request.title,
        content=request.content,
    )

    latency_ms = (time.perf_counter() - start_counter) * 1000

    request_metrics.record_success(latency_ms)

    await log_request(
        db,
        request_id=request_id,
        endpoint="/ingest",
        start_time=start_time,
        total_latency_ms=latency_ms,
        outcome="success",
    )

    return IngestResponse(
        request_id=request_id,
        **result,
    )


@router.post("/ask", response_model=AskResponse)
async def ask(
    request: AskRequest,
    rag: RAGService = Depends(get_rag_service),
    db=Depends(get_db),
) -> AskResponse:

    request_id = str(uuid4())
    start_time = datetime.now(timezone.utc)
    start_counter = time.perf_counter()

    result = rag.ask(
        question=request.question,
        filters=request.filters,
    )

    latency_ms = (time.perf_counter() - start_counter) * 1000

    request_metrics.record_success(latency_ms)

    await log_request(
        db,
        request_id=request_id,
        endpoint="/ask",
        start_time=start_time,
        total_latency_ms=latency_ms,
        outcome="success",
    )

    return AskResponse(
        request_id=request_id,
        answer=result["answer"],
        sources=[
            Source(**source)
            for source in result["sources"]
        ],
    )


@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: str,
    rag: RAGService = Depends(get_rag_service),
    db=Depends(get_db),
) -> DocumentResponse:

    request_id = str(uuid4())
    start_time = datetime.now(timezone.utc)
    start_counter = time.perf_counter()

    document = rag.get_document(document_id)

    latency_ms = (time.perf_counter() - start_counter) * 1000

    if document is None:

        request_metrics.record_failure(latency_ms)

        await log_request(
            db,
            request_id=request_id,
            endpoint="/documents/{document_id}",
            start_time=start_time,
            total_latency_ms=latency_ms,
            outcome="not_found",
            error_category="document_not_found",
        )

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    request_metrics.record_success(latency_ms)

    await log_request(
        db,
        request_id=request_id,
        endpoint="/documents/{document_id}",
        start_time=start_time,
        total_latency_ms=latency_ms,
        outcome="success",
    )

    return DocumentResponse(
        request_id=request_id,
        document_id=document["document_id"],
        title=document["title"],
        chunk_count=len(document["chunks"]),
        status=document["status"],
    )