def build_grounded_prompt(
    question,
    retrieved_chunks,
    max_chunks=5
):
    """
    Build a strict grounded-generation prompt.

    The model must:
    - use only the supplied context
    - avoid unsupported assumptions
    - cite the supplied chunk IDs
    - abstain when evidence is insufficient
    """

    if not retrieved_chunks:
        context = "No relevant context was retrieved."
    else:
        selected_chunks = retrieved_chunks[:max_chunks]

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

            distance = chunk.get(
                "distance",
                None
            )

            if not text:
                continue

            if chunk_id in seen_chunks:
                continue

            seen_chunks.add(chunk_id)

            context_parts.append(
                f"""
[CHUNK {rank}]
Chunk ID: {chunk_id}
Distance: {distance}
Metadata: {metadata}

{text}
""".strip()
            )

        context = "\n\n".join(context_parts)

        if not context:
            context = "No relevant context was retrieved."

    prompt = f"""
You are a grounded question-answering assistant.

Your task is to answer the user's question using ONLY
the retrieved context provided below.

GROUNDING RULES:
1. Use only information present in the supplied context.
2. Do not use outside knowledge.
3. Do not make unsupported assumptions.
4. Do not invent facts, sources, or citations.
5. Every factual claim must be supported by a supplied chunk.
6. Cite the chunk ID that supports each factual claim.
7. Only cite chunk IDs that actually appear in the supplied context.
8. If the context does not contain enough evidence to answer,
   clearly state that the information is not available.
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