def format_source(metadata):
    """Create a stable source label."""

    if not metadata:
        return "Unknown Source"

    doc_id = metadata.get(
        "doc_id",
        "Unknown Document"
    )

    chunk_id = metadata.get(
        "chunk_id",
        "Unknown Chunk"
    )

    return f"{doc_id} | {chunk_id}"


def prepare_context(
    retrieved_chunks,
    max_chunks=5
):
    """Convert retrieved chunks into generation context."""

    selected_chunks = retrieved_chunks[
        :max_chunks
    ]

    context_parts = []

    seen = set()

    for chunk in selected_chunks:

        text = chunk.get(
            "text",
            ""
        ).strip()

        metadata = chunk.get(
            "metadata",
            {}
        )

        source = format_source(
            metadata
        )

        unique_key = (
            source,
            text
        )

        if unique_key in seen:
            continue

        seen.add(unique_key)

        context_parts.append(
            f"[Source: {source}]\n{text}"
        )

    return "\n\n".join(
        context_parts
    )


def generate_context(
    retrieved_chunks,
    max_chunks=5
):
    """Prepare final context for the generation stage."""

    context = prepare_context(
        retrieved_chunks,
        max_chunks=max_chunks
    )

    return context


if __name__ == "__main__":

    sample_results = [
        {
            "text": "Team members are responsible for following documented procedures.",
            "metadata": {
                "doc_id": "document_001",
                "chunk_id": "chunk_001"
            },
            "score": 0.12
        }
    ]

    context = generate_context(
        sample_results
    )

    print(context)