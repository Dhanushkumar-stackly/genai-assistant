from typing import Iterable


def _normalise_ids(source_ids: Iterable[str]) -> list[str]:
    """Return non-empty source IDs as a clean list."""

    return [
        source_id.strip()
        for source_id in source_ids
        if isinstance(source_id, str) and source_id.strip()
    ]


def _normalise_text(text: str) -> str:
    """Normalise text for simple case-insensitive comparisons."""

    return " ".join(text.lower().split())


def check_answerability(
    expected_answerable: bool,
    answer: str,
) -> bool:
    """
    Check whether the answer matches the expected answerability.

    For answerable cases, a non-empty answer is required.
    For unanswerable cases, an abstaining answer is expected.
    """

    answer = answer.strip()

    if expected_answerable:
        return bool(answer)

    return is_abstention(answer)


def has_citation(
    answer: str,
    citation_ids: Iterable[str],
) -> bool:
    """Return True when the answer contains at least one citation ID."""

    if not answer.strip():
        return False

    return bool(_normalise_ids(citation_ids))


def validate_citations(
    citation_ids: Iterable[str],
    retrieved_source_ids: Iterable[str],
) -> bool:
    """Check that every cited source exists in retrieved sources."""

    citations = set(_normalise_ids(citation_ids))
    retrieved = set(_normalise_ids(retrieved_source_ids))

    if not citations:
        return False

    return citations.issubset(retrieved)


def check_required_facts(
    answer: str,
    required_facts: Iterable[str],
) -> bool:
    """
    Check whether every required fact appears in the answer.

    Matching is case-insensitive and whitespace-normalised.
    """

    facts = [
        fact.strip()
        for fact in required_facts
        if isinstance(fact, str) and fact.strip()
    ]

    if not facts:
        return True

    normalised_answer = _normalise_text(answer)

    return all(
        _normalise_text(fact) in normalised_answer
        for fact in facts
    )


def is_abstention(answer: str) -> bool:
    """
    Detect whether an answer correctly indicates that the system
    cannot answer from the available information.
    """

    normalised_answer = _normalise_text(answer)

    abstention_phrases = (
        "i don't know",
        "i do not know",
        "i don't have enough information",
        "i do not have enough information",
        "not enough information",
        "cannot answer",
        "can't answer",
        "unable to answer",
        "insufficient information",
        "no information available",
        "not available in the provided documents",
        "not supported by the provided documents",
    )

    return any(
        phrase in normalised_answer
        for phrase in abstention_phrases
    )


def check_correct_abstention(
    expected_answerable: bool,
    answer: str,
) -> bool:
    """
    Check abstention behavior.

    Unanswerable cases must abstain.
    Answerable cases should not be treated as abstentions.
    """

    if expected_answerable:
        return not is_abstention(answer)

    return is_abstention(answer)


def grade_answer_case(
    *,
    expected_answerable: bool,
    answer: str,
    citation_ids: Iterable[str],
    retrieved_source_ids: Iterable[str],
    required_facts: Iterable[str] = (),
) -> dict[str, bool]:
    """Return all answer-quality metrics for one evaluation case."""

    citation_present = has_citation(
        answer,
        citation_ids,
    )

    citation_valid = validate_citations(
        citation_ids,
        retrieved_source_ids,
    )

    facts_correct = check_required_facts(
        answer,
        required_facts,
    )

    answerability_correct = check_answerability(
        expected_answerable,
        answer,
    )

    abstention_correct = check_correct_abstention(
        expected_answerable,
        answer,
    )

    return {
        "answerability_correct": answerability_correct,
        "citation_present": citation_present,
        "citation_valid": citation_valid,
        "required_facts_correct": facts_correct,
        "abstention_correct": abstention_correct,
    }