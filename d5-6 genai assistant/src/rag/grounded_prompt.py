def build_grounded_prompt(question, retrieved_chunks):
    """
    Build a grounded prompt using only retrieved context.

    Args:
        question (str): User's question.
        retrieved_chunks (list): Retrieved context chunks.

    Returns:
        str: Grounded prompt.
    """

    # Handle empty retrieval
    if not retrieved_chunks:
        context_text = "No supporting evidence was retrieved."
    else:
        context_parts = []

        for chunk in retrieved_chunks:
            chunk_id = chunk.get("chunk_id", "unknown")
            text = chunk.get("text", "")

            context_parts.append(
                f"[{chunk_id}]\n{text}"
            )

        context_text = "\n\n".join(context_parts)

    prompt = f"""You are a grounded question-answering assistant.

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

{context_text}

USER QUESTION:
{question}

ANSWER:"""

    return prompt