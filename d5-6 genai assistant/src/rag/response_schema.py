from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceReference:
    """
    Represents one validated source reference.
    """

    chunk_id: str
    source: str
    distance: float
    preview: str


@dataclass
class RAGResponse:
    """
    Standard response structure for the RAG pipeline.
    """

    answer: str
    sources: list[SourceReference] = field(
        default_factory=list
    )
    status: str = "answered"

    def to_dict(self):
        """
        Convert the response into a dictionary.
        """

        return {
            "answer": self.answer,

            "sources": [
                {
                    "chunk_id": source.chunk_id,
                    "source": source.source,
                    "distance": source.distance,
                    "preview": source.preview
                }
                for source in self.sources
            ],

            "status": self.status
        }


def build_response(
    answer,
    retrieved_chunks,
    status="answered"
):
    """
    Build a structured RAG response from
    retrieved database chunks.
    """

    if not answer or not answer.strip():
        answer = (
            "Information is not available "
            "in the provided documents."
        )

    sources = []

    for chunk in retrieved_chunks:

        chunk_id = chunk.get(
            "chunk_id"
        )

        text = chunk.get(
            "text",
            ""
        ).strip()

        metadata = chunk.get(
            "metadata",
            {}
        )

        distance = chunk.get(
            "distance"
        )

        source = metadata.get(
            "source",
            chunk_id
        )

        if not chunk_id:
            continue

        if distance is None:
            continue

        preview = text[:300]

        sources.append(
            SourceReference(
                chunk_id=chunk_id,
                source=source,
                distance=float(distance),
                preview=preview
            )
        )

    return RAGResponse(
        answer=answer,
        sources=sources,
        status=status
    )