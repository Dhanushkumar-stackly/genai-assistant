from pydantic import BaseModel, Field


class HealthDependencies(BaseModel):
    database: str
    rag: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    request_id: str
    dependencies: HealthDependencies


class IngestRequest(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class IngestResponse(BaseModel):
    request_id: str
    document_id: str
    chunk_count: int
    status: str


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    filters: dict | None = None


class Source(BaseModel):
    document_id: str
    title: str
    score: float | None = None


class AskResponse(BaseModel):
    request_id: str
    answer: str
    sources: list[Source]


class DocumentResponse(BaseModel):
    request_id: str
    document_id: str
    title: str
    chunk_count: int
    status: str


class MetricsResponse(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_latency_ms: float


class ErrorResponse(BaseModel):
    request_id: str
    error_code: str
    message: str
    detail: object | None = None
