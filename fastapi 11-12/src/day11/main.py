from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI

from .database import init_db
from .rag import rag_service
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(
        "Starting GenAI RAG API v0.1.0 "
        "in development environment"
    )

    await init_db()

    rag_service.startup()

    yield

    rag_service.shutdown()


app = FastAPI(
    title="GenAI RAG API",
    version="0.1.0",
    description="GenAI Retrieval-Augmented Generation API",
    lifespan=lifespan,
)


app.include_router(router)


@app.get("/health")
async def health():
    request_id = str(uuid4())

    return {
        "status": "ok",
        "service": "GenAI RAG API",
        "version": "0.1.0",
        "request_id": request_id,
    }