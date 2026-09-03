from typing import Any


def build_allowed_citations(
    retrieved_chunks: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """
    Build a lookup containing only citations
    from chunks actually retrieved and supplied
    to the model.
    """

    allowed = {}

    for chunk in retrieved_chunks:

        chunk_id = chunk.get("chunk_id")

        if not chunk_id:
            continue

        metadata = chunk.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            chunk_id
        )

        distance = chunk.get(
            "distance"
        )

        text = chunk.get(
            "text",
            ""
        )

        allowed[chunk_id] = {
            "chunk_id": chunk_id,
            "source": source,
            "distance": distance,
            "preview": text[:300]
        }

    return allowed


def validate_citations(
    citations: list[str],
    retrieved_chunks: list[dict[str, Any]]
) -> list[str]:
    """
    Keep only citations that refer to chunks
    actually supplied to the model.
    """

    allowed = build_allowed_citations(
        retrieved_chunks
    )

    valid_citations = []

    for citation in citations:

        if citation in allowed:

            if citation not in valid_citations:
                valid_citations.append(
                    citation
                )

    return valid_citations


def map_citations_to_sources(
    citations: list[str],
    retrieved_chunks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Convert valid chunk IDs into structured
    source information.
    """

    allowed = build_allowed_citations(
        retrieved_chunks
    )

    mapped_sources = []

    for citation in citations:

        source = allowed.get(
            citation
        )

        if source is not None:
            mapped_sources.append(
                source
            )

    return mapped_sources