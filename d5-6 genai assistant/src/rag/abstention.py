DEFAULT_MAX_DISTANCE = 0.80

ABSTENTION_MESSAGE = (
    "Information is not available in the "
    "provided documents."
)


def has_sufficient_evidence(
    retrieved_chunks,
    max_distance=DEFAULT_MAX_DISTANCE
):
    """
    Check whether at least one retrieved chunk
    passes the configured evidence threshold.
    """

    if not retrieved_chunks:
        return False

    for chunk in retrieved_chunks:

        distance = chunk.get("distance")

        if distance is None:
            continue

        if float(distance) <= max_distance:
            return True

    return False


def should_abstain(
    retrieved_chunks,
    max_distance=DEFAULT_MAX_DISTANCE
):
    """
    Return True when the system should abstain
    instead of generating an answer.
    """

    return not has_sufficient_evidence(
        retrieved_chunks,
        max_distance=max_distance
    )


def get_abstention_response():
    """
    Return the standard safe fallback response.
    """

    return {
        "answer": ABSTENTION_MESSAGE,
        "sources": [],
        "status": "insufficient_evidence"
    }