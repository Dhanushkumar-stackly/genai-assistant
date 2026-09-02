from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class IngestRequest(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class IngestResponse(BaseModel):
    document_id: str
    chunk_count: int
    status: str


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    filters: dict | None = None


class Source(BaseModel):
    document_id: str
    title: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class DocumentResponse(BaseModel):
    document_id: str
    title: str
    chunk_count: int
    status: str