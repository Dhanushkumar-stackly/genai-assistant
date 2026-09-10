"""
Day 08 - Grounded Answer Generation

This module converts retrieved evidence into a concise answer.

Important:
- It does NOT retrieve data.
- It does NOT modify ChromaDB.
- It uses ONLY retrieved chunks.
- It does NOT add outside knowledge.
"""

import re


def prepare_context(retrieved_chunks):
    """
    Convert retrieved chunks into grounded context text.
    """

    if not retrieved_chunks:
        return "No supporting evidence was retrieved."

    context_parts = []

    for chunk in retrieved_chunks:
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk.get("text", "")

        if not text:
            continue

        context_parts.append(
            f"[{chunk_id}]\n{text}"
        )

    if not context_parts:
        return "No supporting evidence was retrieved."

    return "\n\n".join(context_parts)


def build_generation_input(question, retrieved_chunks):
    """
    Build the input used for grounded answer generation.
    """

    context = prepare_context(retrieved_chunks)

    return f"""
You are a grounded question-answering assistant.

Answer the user's question using ONLY the supplied evidence.

Rules:
1. Use only information present in the evidence.
2. Do not use outside knowledge.
3. Do not guess.
4. Do not invent facts.
5. Give a direct answer to the user's question.
6. Do not copy the entire retrieved documents.
7. Summarize only the information relevant to the question.
8. Add the supporting chunk ID after factual statements.
9. If the evidence is insufficient, say:
   "The answer cannot be determined from the provided evidence."

EVIDENCE:
{context}

USER QUESTION:
{question}

ANSWER:
""".strip()


def _extract_relevant_sections(text):
    """
    Extract useful sections from retrieved Markdown documents.

    Preference:
    - Process
    - Requirements
    - Model Evaluation
    """

    sections = []

    patterns = [
        r"## Process\s*(.*?)(?=\n## |\Z)",
        r"## Requirements\s*(.*?)(?=\n## |\Z)",
        r"## Model Evaluation\s*(.*?)(?=\n## |\Z)",
    ]

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        for match in matches:
            cleaned = " ".join(match.split())

            if cleaned:
                sections.append(cleaned)

    return sections


def generate_answer(question, retrieved_chunks):
    """
    Generate a concise grounded answer.

    This implementation creates the answer directly from retrieved
    evidence, so it does not introduce outside knowledge.
    """

    if not retrieved_chunks:
        return (
            "The answer cannot be determined from the provided evidence."
        )

    answer_parts = []

    for chunk in retrieved_chunks:
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk.get("text", "")

        if not text:
            continue

        relevant_sections = _extract_relevant_sections(text)

        for section in relevant_sections:
            answer_parts.append(
                f"{section} [{chunk_id}]"
            )

    if not answer_parts:
        return (
            "The answer cannot be determined from the provided evidence."
        )

    # Remove duplicate statements while preserving order.
    unique_parts = []

    for part in answer_parts:
        normalized = part.lower().strip()

        if not any(
            normalized == existing.lower().strip()
            for existing in unique_parts
        ):
            unique_parts.append(part)

    # Limit the answer to the most relevant evidence.
    selected_parts = unique_parts[:3]

    return " ".join(selected_parts)


def generate_context(question, retrieved_chunks):
    """
    Backward-compatible helper.

    Existing Day-08 code can continue calling this function.
    """

    return build_generation_input(
        question,
        retrieved_chunks
    )