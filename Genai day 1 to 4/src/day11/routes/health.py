from fastapi import APIRouter, Depends

from src.day11.config import Settings, get_settings


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("")
def health(settings: Settings = Depends(get_settings)) -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }