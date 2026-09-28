
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .database import AsyncSessionLocal, init_db
from .logging_service import log_request
from .metrics import request_metrics
from .models import ErrorResponse, HealthResponse, MetricsResponse
from .rag import NoEvidenceError, rag_service
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting GenAI RAG API v0.1.0 in development environment")

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


# ============================================================
# DAY 11 / DAY 12 API ROUTES
# ============================================================
#
# routes.py contains:
#
# GET  /
# POST /ingest
# POST /ask
# GET  /documents/{document_id}
#
# Register all of them with the main FastAPI application.
#
app.include_router(router)


# ============================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id

    start_time = datetime.now(timezone.utc)
    start_counter = perf_counter()

    status_code = 500
    outcome = "error"
    error_category = "internal_error"

    try:
        response = await call_next(request)

        status_code = response.status_code

        if status_code < 400:
            outcome = "success"
            error_category = None

        elif status_code == 404:
            outcome = "not_found"
            error_category = "not_found"

        elif status_code == 422:
            outcome = "validation_error"
            error_category = "validation"

        else:
            outcome = "error"
            error_category = "internal_error"

        return response

    except Exception:
        status_code = 500
        outcome = "error"
        error_category = "internal_error"
        raise

    finally:
        latency_ms = (perf_counter() - start_counter) * 1000

        if status_code < 400:
            request_metrics.record_success(latency_ms)
        else:
            request_metrics.record_failure(latency_ms)

        try:
            async with AsyncSessionLocal() as session:
                await log_request(
                    session,
                    request_id=request_id,
                    endpoint=request.url.path,
                    start_time=start_time,
                    total_latency_ms=latency_ms,
                    outcome=outcome,
                    error_category=error_category,
                )

        except Exception:
            # Logging failure must never break the API response.
            pass


# ============================================================
# HEALTH API
# ============================================================

@app.get("/health", response_model=HealthResponse)
async def health(request: Request):
    database_status = "ready"

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))

    except Exception:
        database_status = "unavailable"

    rag_status = "ready" if rag_service.ready else "not_ready"

    status = (
        "ok"
        if database_status == "ready" and rag_status == "ready"
        else "degraded"
    )

    return HealthResponse(
        status=status,
        service="GenAI RAG API",
        version="0.1.0",
        request_id=request.state.request_id,
        dependencies={
            "database": database_status,
            "rag": rag_status,
        },
    )


# ============================================================
# METRICS API
# ============================================================

@app.get("/metrics", response_model=MetricsResponse)
async def metrics():
    return request_metrics.get_metrics()


# ============================================================
# HTTP EXCEPTION HANDLER
# ============================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    error_code = (
        "DOCUMENT_NOT_FOUND"
        if exc.detail == "Document not found"
        else "HTTP_ERROR"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            request_id=request.state.request_id,
            error_code=error_code,
            message=str(exc.detail),
        ).model_dump(),
    )


# ============================================================
# REQUEST VALIDATION ERROR HANDLER
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            request_id=request.state.request_id,
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            detail=exc.errors(),
        ).model_dump(),
    )


# ============================================================
# RAG NO-EVIDENCE ERROR HANDLER
# ============================================================

@app.exception_handler(NoEvidenceError)
async def no_evidence_exception_handler(
    request: Request,
    exc: NoEvidenceError,
):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            request_id=request.state.request_id,
            error_code="NO_EVIDENCE",
            message="No evidence is available for this question",
        ).model_dump(),
    )


# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            request_id=request.state.request_id,
            error_code="INTERNAL_ERROR",
            message="An internal server error occurred",
        ).model_dump(),
    )
