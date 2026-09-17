import sys
from pathlib import Path
TASK_ROOT = Path(__file__).resolve().parents[1]
if str(TASK_ROOT) not in sys.path:
    sys.path.insert(0, str(TASK_ROOT))

from src.rag.grounded_generation import (
    generate_grounded_response,
)


def test_grounded_generation_returns_answer():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a high-level programming language.",
        }
    ]

    response = generate_grounded_response(
        "What is Python?",
        chunks,
    )

    assert response.answer == (
        "Python is a high-level programming language."
    )


def test_grounded_generation_returns_citations():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        }
    ]

    response = generate_grounded_response(
        "What is Python?",
        chunks,
    )

    assert len(response.citations) == 1
    assert response.citations[0].source == "python_guide.pdf"
    assert response.citations[0].chunk_id == "chunk_001"


def test_grounded_generation_is_grounded():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        }
    ]

    response = generate_grounded_response(
        "What is Python?",
        chunks,
    )

    assert response.grounded is True


def test_grounded_generation_abstains_without_context():
    response = generate_grounded_response(
        "What is reinforcement learning?",
        [],
    )

    assert response.grounded is False
    assert "cannot be determined" in response.answer
    assert response.citations == []


def test_grounded_generation_handles_multiple_citations():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        },
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_002",
            "text": "Python supports OOP.",
        },
    ]

    response = generate_grounded_response(
        "What is Python?",
        chunks,
    )

    assert len(response.citations) == 2