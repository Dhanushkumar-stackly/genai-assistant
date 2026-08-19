from src.rag.grounded_prompt import build_grounded_prompt


def test_grounded_prompt_contains_question():
    question = "What is Python?"

    chunks = [
        {
            "chunk_id": "chunk_001",
            "source": "python_guide.pdf",
            "text": "Python is a high-level programming language.",
        }
    ]

    prompt = build_grounded_prompt(question, chunks)

    assert question in prompt


def test_grounded_prompt_contains_context():
    chunks = [
        {
            "chunk_id": "chunk_001",
            "source": "python_guide.pdf",
            "text": "Python is a high-level programming language.",
        }
    ]

    prompt = build_grounded_prompt(
        "What is Python?",
        chunks,
    )

    assert "Python is a high-level programming language." in prompt


def test_grounded_prompt_contains_source_label():
    chunks = [
        {
            "chunk_id": "chunk_001",
            "source": "python_guide.pdf",
            "text": "Python is a high-level programming language.",
        }
    ]

    prompt = build_grounded_prompt(
        "What is Python?",
        chunks,
    )

    assert "python_guide.pdf" in prompt
    assert "chunk_001" in prompt


def test_grounded_prompt_prevents_unsupported_answers():
    chunks = [
        {
            "chunk_id": "chunk_001",
            "source": "python_guide.pdf",
            "text": "Python is a high-level programming language.",
        }
    ]

    prompt = build_grounded_prompt(
        "What is Python?",
        chunks,
    )

    assert "ONLY the provided context" in prompt
    assert "Do NOT use outside knowledge" in prompt
    assert "unsupported assumptions" in prompt


def test_grounded_prompt_handles_insufficient_evidence():
    chunks = [
        {
            "chunk_id": "chunk_001",
            "source": "python_guide.pdf",
            "text": "Python is a high-level programming language.",
        }
    ]

    prompt = build_grounded_prompt(
        "Who created Python?",
        chunks,
    )

    assert "cannot be determined" in prompt
    assert "provided evidence" in prompt