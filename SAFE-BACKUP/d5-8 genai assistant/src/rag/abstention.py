DEFAULT_MAX_DISTANCE = 0.80

ABSTENTION_MESSAGE = (
    "Information is not available in the provided documents."
)


def has_sufficient_evidence(
    retrieved_chunks,
    max_distance=DEFAULT_MAX_DISTANCE,
):
    """
    Check whether retrieved chunks provide sufficient evidence.
    """
    if not retrieved_chunks:
        return False

    for chunk in retrieved_chunks:
        distance = chunk.get("distance")

        # Chunks without distance are still valid retrieved context.
        if distance is None:
            return True

        try:
            if float(distance) <= max_distance:
                return True
        except (TypeError, ValueError):
            continue

    return False


def should_abstain(
    retrieved_chunks,
    max_distance=DEFAULT_MAX_DISTANCE,
):
    return not has_sufficient_evidence(
        retrieved_chunks,
        max_distance,
    )


def get_abstention_message():
    """
    Message used by grounded generation.
    """
    return (
        "The answer cannot be determined "
        "from the provided documents."
    )


def get_abstention_response():
    """
    Safe API-style abstention response.
    """
    return {
        "answer": ABSTENTION_MESSAGE,
        "sources": [],
        "status": "insufficient_evidence",
    }