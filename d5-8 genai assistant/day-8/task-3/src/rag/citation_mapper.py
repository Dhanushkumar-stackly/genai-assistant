from typing import Any, Dict, List


def build_allowed_citations(
    retrieved_chunks: List[Dict[str, Any]]
) -> List[str]:
    """
    Return the chunk IDs that are allowed to be cited.
    """
    return [
        chunk["chunk_id"]
        for chunk in retrieved_chunks
        if chunk.get("chunk_id")
    ]


def validate_citations(
    citations: List[str],
    retrieved_chunks: List[Dict[str, Any]]
) -> List[str]:
    """
    Keep only citations that belong to retrieved chunks.
    Remove duplicates while preserving order.
    """
    allowed_ids = set(
        build_allowed_citations(retrieved_chunks)
    )

    valid = []
    seen = set()

    for citation in citations:
        if citation in allowed_ids and citation not in seen:
            valid.append(citation)
            seen.add(citation)

    return valid


def map_citations_to_sources(
    citations: List[str],
    retrieved_chunks: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Map citation IDs to source and distance information.
    """
    chunk_map = {
        chunk.get("chunk_id"): chunk
        for chunk in retrieved_chunks
    }

    sources = []

    for citation in citations:
        chunk = chunk_map.get(citation)

        if chunk is None:
            continue

        metadata = chunk.get("metadata", {})

        sources.append(
            {
                "chunk_id": citation,
                "source": metadata.get(
                    "source",
                    chunk.get("source", "")
                ),
                "distance": chunk.get("distance"),
            }
        )

    return sources


def map_citations(
    retrieved_chunks: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Convert retrieved chunks into citation dictionaries
    for grounded response generation.
    """
    citations = []

    for chunk in retrieved_chunks:
        chunk_id = chunk.get("chunk_id")

        if not chunk_id:
            continue

        metadata = chunk.get("metadata", {})

        citations.append(
            {
                "chunk_id": chunk_id,
                "source": metadata.get(
                    "source",
                    chunk.get("source", "")
                ),
                "distance": chunk.get("distance"),
                "preview": chunk.get(
                    "text",
                    chunk.get("content", "")
                )[:200],
            }
        )

    return citations