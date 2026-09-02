from fastapi import APIRouter, Depends

from .config import Settings, get_settings
from .rag import RAGService, rag_service


router = APIRouter()


def get_rag_service() -> RAGService:
    return rag_service


@router.get("/")
def root(
    settings: Settings = Depends(get_settings),
    rag: RAGService = Depends(get_rag_service),
) -> dict[str, str]:
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }