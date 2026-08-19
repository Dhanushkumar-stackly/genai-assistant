def format_source(metadata):
    """Create a readable source label."""

    if not metadata:
        return "Unknown Source"

    chunk_id = metadata.get(
        "chunk_id",
        "Unknown Chunk"
    )

    chunk_index = metadata.get(
        "chunk_index",
        "Unknown Index"
    )

    return (
        f"{chunk_id} "
        f"(index: {chunk_index})"
    )


def prepare_context(
    retrieved_chunks,
    max_chunks=5
):
    """
    Convert retrieved chunks into
    LLM-ready context.
    """

    if not retrieved_chunks:
        return ""

    selected_chunks = retrieved_chunks[
        :max_chunks
    ]

    context_parts = []

    seen_chunks = set()

    for rank, chunk in enumerate(
        selected_chunks,
        start=1
    ):

        chunk_id = chunk.get(
            "chunk_id",
            f"unknown_{rank}"
        )

        text = chunk.get(
            "text",
            ""
        ).strip()

        metadata = chunk.get(
            "metadata",
            {}
        )

        # Support source directly from chunk
        # as well as metadata.
        source = chunk.get(
            "source"
        )

        if source and not metadata.get("source"):
            metadata = {
                **metadata,
                "source": source
            }

        distance = chunk.get(
            "distance",
            None
        )

        if not text:
            continue

        # Prevent duplicate chunks
        if chunk_id in seen_chunks:
            continue

        seen_chunks.add(chunk_id)

        source_label = format_source(
            metadata
        )

        context_parts.append(
            f"""
[Retrieved Context {rank}]
Chunk ID: {chunk_id}
Source: {source_label}
Distance: {distance}

{text}
""".strip()
        )

    return "\n\n".join(
        context_parts
    )


def build_generation_input(
    question,
    retrieved_chunks,
    max_chunks=5
):
    """
    Build the grounded generation prompt.
    """

    context = prepare_context(
        retrieved_chunks,
        max_chunks=max_chunks
    )

    if not context:
        context = (
            "No relevant context was retrieved."
        )

    prompt = f"""
You are a grounded AI assistant.

Answer the user's question using ONLY
the provided context.

Grounding rules:

1. Do not use outside knowledge.
2. Do not invent or assume facts.
3. Every factual statement must be supported
   by the retrieved context.
4. After each factual statement, include the
   corresponding chunk ID in square brackets.
5. Use citations exactly in this format:
   [chunk_id]
6. Only cite chunk IDs that appear in the
   retrieved context.
7. Do not create or modify chunk IDs.
8. If the answer cannot be found in the
   retrieved context, say:
   "The information is not available in
   the provided documents."

User Question:
{question}

Retrieved Context:
{context}

Answer:
""".strip()

    return prompt


def generate_context(
    question,
    retrieved_chunks,
    max_chunks=5
):
    """
    Public generation-stage function.

    This function is used by the RAG pipeline
    tests and returns the grounded generation input.
    """

    return build_generation_input(
        question=question,
        retrieved_chunks=retrieved_chunks,
        max_chunks=max_chunks
    )


if __name__ == "__main__":

    sample_results = [
        {
            "chunk_id": "document_006_chunk_000",

            "text": (
                "Reinforcement Learning "
                "allows agents to learn by "
                "interacting with an environment."
            ),

            "metadata": {
                "chunk_id":
                    "document_006_chunk_000",
                "chunk_index": 5
            },

            "distance": 0.25
        }
    ]

    question = (
        "What is reinforcement learning?"
    )

    prompt = generate_context(
        question,
        sample_results
    )

    print("=" * 60)
    print("GROUNDED GENERATION INPUT")
    print("=" * 60)
    print(prompt)