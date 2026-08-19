ABSTENTION_MESSAGE = (
    "The answer cannot be determined from the provided evidence."
)


def should_abstain(chunks: list[dict]) -> bool:
    """
    Return True when there is no usable evidence.
    """

    if not chunks:
        return True

    for chunk in chunks:
        text = chunk.get("text", chunk.get("content", ""))

        if text and text.strip():
            return False

    return True


def get_abstention_message() -> str:
    """
    Return the standard abstention message.
    """

    return ABSTENTION_MESSAGE