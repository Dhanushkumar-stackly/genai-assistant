from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import get_settings
from .rag import rag_service
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    print(
        f"Starting {settings.app_name} "
        f"v{settings.app_version} "
        f"in {settings.environment} environment"
    )

    rag_service.startup()

    yield

    print("Shutting down GenAI RAG API")


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(router)