def build_grounded_prompt(
    question,
    retrieved_chunks,
):
    """
    Build a strict grounded prompt using
    only the retrieved context.
    """

    context_parts = []

    for index, chunk in enumerate(
        retrieved_chunks or [],
        start=1
    ):
        chunk_id = chunk.get(
            "chunk_id",
            f"unknown_{index}"
        )

        source = chunk.get(
            "source",
            "Unknown Source"
        )

        text = chunk.get(
            "text",
            ""
        ).strip()

        distance = chunk.get(
            "distance",
            None
        )

        context_parts.append(
            f"""
[CHUNK {index}]
Chunk ID: {chunk_id}
Source: {source}
Distance: {distance}

{text}
""".strip()
        )

    context = "\n\n".join(
        context_parts
    )

    if not context:
        context = (
            "No relevant context was retrieved."
        )

    prompt = f"""
You are a grounded question-answering assistant.

Your task is to answer the user's question using ONLY the provided context.

GROUNDING RULES:

1. Use ONLY information present in the provided context.
2. Do NOT use outside knowledge.
3. Do not make unsupported assumptions.
4. Do not invent facts, sources, or citations.
5. Every factual claim must be supported by a supplied chunk.
6. Cite the chunk ID that supports each factual claim.
7. Only cite chunk IDs that actually appear in the supplied context.
8. If the context does not contain enough evidence to answer,
   clearly state that the answer cannot be determined from the
   provided evidence.
9. If only part of the question can be answered, answer only
   the supported part and clearly identify what is unsupported.
10. Never guess.

CITATION FORMAT:

Use this format when citing evidence:

[chunk_id]

Example:
Reinforcement learning allows an agent to learn through
interaction with an environment. [document_006_chunk_000]

RETRIEVED CONTEXT:

{context}

USER QUESTION:
{question}

ANSWER:
""".strip()

    return prompt