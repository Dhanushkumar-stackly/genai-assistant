from fastapi import APIRouter, Depends

from .config import Settings, get_settings
from .database import get_db
from .models import (
    AskRequest,
    AskResponse,
    DocumentResponse,
    HealthResponse,
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
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }


@router.get("/health", response_model=HealthResponse)
def health(
    settings: Settings = Depends(get_settings),
    rag: RAGService = Depends(get_rag_service),
) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.post("/ingest", response_model=IngestResponse)
def ingest(
    request: IngestRequest,
    rag: RAGService = Depends(get_rag_service),
) -> IngestResponse:
    result = rag.ingest_document(
        title=request.title,
        content=request.content,
    )

    return IngestResponse(**result)


@router.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest,
    rag: RAGService = Depends(get_rag_service),
) -> AskResponse:
    result = rag.ask(
        question=request.question,
        filters=request.filters,
    )

    return AskResponse(
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
def get_document(
    document_id: str,
    rag: RAGService = Depends(get_rag_service),
) -> DocumentResponse:
    document = rag.get_document(document_id)

    if document is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return DocumentResponse(
        document_id=document["document_id"],
        title=document["title"],
        chunk_count=len(document["chunks"]),
        status=document["status"],
    )