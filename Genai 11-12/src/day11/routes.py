from fastapi import APIRouter, Depends, HTTPException, Request

from .config import Settings, get_settings
from .database import get_db
from .logging_service import log_retrieved_sources
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


def request_id(request: Request) -> str:
    return request.state.request_id


@router.get("/", response_model=dict[str, str])
def root(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "message": "GenAI RAG API is running",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }


@router.post("/ingest", response_model=IngestResponse)
async def ingest(
    request: Request,
    payload: IngestRequest,
    rag: RAGService = Depends(get_rag_service),
) -> IngestResponse:
    result = rag.ingest_document(title=payload.title, content=payload.content)
    return IngestResponse(request_id=request_id(request), **result)


@router.post("/ask", response_model=AskResponse)
async def ask(
    request: Request,
    payload: AskRequest,
    rag: RAGService = Depends(get_rag_service),
    db=Depends(get_db),
) -> AskResponse:
    result = rag.ask(question=payload.question, filters=payload.filters)

    await log_retrieved_sources(
        db,
        request_id=request_id(request),
        sources=result["sources"],
    )

    return AskResponse(
        request_id=request_id(request),
        answer=result["answer"],
        sources=[Source(**source) for source in result["sources"]],
    )


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    request: Request,
    document_id: str,
    rag: RAGService = Depends(get_rag_service),
) -> DocumentResponse:
    document = rag.get_document(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentResponse(
        request_id=request_id(request),
        document_id=document["document_id"],
        title=document["title"],
        chunk_count=len(document["chunks"]),
        status=document["status"],
    )
