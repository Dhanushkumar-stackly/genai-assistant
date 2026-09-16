from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Citation(BaseModel):
    chunk_id: str
    source: str
    distance: Optional[float] = None
    preview: str = ""


class Source(BaseModel):
    chunk_id: str
    source: str
    distance: Optional[float] = None


class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    grounded: bool = False
    status: str = "answered"
    sources: List[Source] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


def build_response(
    answer: str,
    retrieved_chunks: Optional[List[Dict[str, Any]]] = None,
    status: str = "answered",
) -> AnswerResponse:

    retrieved_chunks = retrieved_chunks or []

    citations = []
    sources = []

    for chunk in retrieved_chunks:
        chunk_id = chunk.get("chunk_id")

        if not chunk_id:
            continue

        metadata = chunk.get("metadata", {})

        source = metadata.get(
            "source",
            chunk.get("source", "")
        )

        distance = chunk.get("distance")

        preview = chunk.get(
            "text",
            chunk.get("content", "")
        )[:200]

        citations.append(
            Citation(
                chunk_id=chunk_id,
                source=source,
                distance=distance,
                preview=preview,
            )
        )

        sources.append(
            Source(
                chunk_id=chunk_id,
                source=source,
                distance=distance,
            )
        )

    grounded = (
        bool(retrieved_chunks)
        and status != "insufficient_evidence"
    )

    return AnswerResponse(
        answer=answer,
        citations=citations,
        grounded=grounded,
        status=status,
        sources=sources,
    )