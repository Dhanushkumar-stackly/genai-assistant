from src.rag.response_schema import AnswerResponse, Citation


def test_answer_response_contains_answer():
    response = AnswerResponse(
        answer="Python is a high-level programming language."
    )

    assert response.answer == "Python is a high-level programming language."


def test_answer_response_contains_citation():
    response = AnswerResponse(
        answer="Python is a high-level programming language.",
        citations=[
            Citation(
                source="python_guide.pdf",
                chunk_id="chunk_001",
            )
        ],
    )

    assert len(response.citations) == 1
    assert response.citations[0].source == "python_guide.pdf"
    assert response.citations[0].chunk_id == "chunk_001"


def test_answer_response_grounded_defaults_to_true():
    response = AnswerResponse(
        answer="Python is a programming language."
    )

    assert response.grounded is True


def test_answer_response_supports_multiple_citations():
    response = AnswerResponse(
        answer="Python supports object-oriented programming.",
        citations=[
            Citation(
                source="python_guide.pdf",
                chunk_id="chunk_001",
            ),
            Citation(
                source="python_guide.pdf",
                chunk_id="chunk_002",
            ),
        ],
    )

    assert len(response.citations) == 2