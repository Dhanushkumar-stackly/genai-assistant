from pydantic import BaseModel, Field


class Citation(BaseModel):
    source: str
    chunk_id: str


class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    grounded: bool = True