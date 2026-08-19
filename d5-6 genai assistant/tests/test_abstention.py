from src.rag.abstention import (
    should_abstain,
    get_abstention_message,
)


def test_abstain_when_chunks_are_empty():
    assert should_abstain([]) is True


def test_do_not_abstain_when_evidence_exists():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        }
    ]

    assert should_abstain(chunks) is False


def test_abstain_when_chunk_text_is_empty():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "",
        }
    ]

    assert should_abstain(chunks) is True


def test_abstain_when_chunk_text_is_only_whitespace():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "   ",
        }
    ]

    assert should_abstain(chunks) is True


def test_abstention_message_is_available():
    message = get_abstention_message()

    assert message
    assert "cannot be determined" in message