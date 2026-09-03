from src.rag.grounded_prompt import build_grounded_prompt
from src.rag.citation_mapper import map_citations
from src.rag.abstention import (
    should_abstain,
    get_abstention_message,
)
from src.rag.response_schema import AnswerResponse, Citation


def generate_grounded_response(
    question: str,
    chunks: list[dict],
) -> AnswerResponse:
    """
    Build a grounded generation response.

    This stage prepares the prompt, checks evidence,
    and attaches citations.

    Actual LLM generation will be connected later.
    """

    if should_abstain(chunks):
        return AnswerResponse(
            answer=get_abstention_message(),
            citations=[],
            grounded=False,
        )

    prompt = build_grounded_prompt(
        question,
        chunks,
    )

    citations_data = map_citations(chunks)

    citations = [
        Citation(**citation)
        for citation in citations_data
    ]

    # Temporary deterministic answer for pipeline testing.
    first_chunk = chunks[0]

    answer = first_chunk.get(
        "text",
        first_chunk.get("content", ""),
    )

    return AnswerResponse(
        answer=answer,
        citations=citations,
        grounded=True,
    )