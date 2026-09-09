from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .database import init_db
from .metrics import request_metrics
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

    request_metrics.record_success(0.0)

    return {
        "status": "ok",
        "service": "GenAI RAG API",
        "version": "0.1.0",
        "request_id": request_id,
    }


@app.get("/metrics")
async def metrics():
    return request_metrics.get_metrics()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    request_id = str(uuid4())

    request_metrics.record_failure(0.0)

    return JSONResponse(
        status_code=422,
        content={
            "request_id": request_id,
            "error_code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "detail": exc.errors(),
        },
    )