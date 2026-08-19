def map_citations(chunks: list[dict]) -> list[dict]:
    """
    Convert retrieved chunks into citation objects.
    """

    citations = []

    for chunk in chunks:
        source = chunk.get("source")
        chunk_id = chunk.get("chunk_id")

        if not source or not chunk_id:
            continue

        citation = {
            "source": source,
            "chunk_id": chunk_id,
        }

        if citation not in citations:
            citations.append(citation)

    return citations