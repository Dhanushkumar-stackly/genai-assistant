from src.rag.response_schema import (
    build_response
)


def test_answered_response_contains_sources():

    retrieved_chunks = [
        {
            "chunk_id":
                "document_006_chunk_000",

            "text":
                "Reinforcement Learning "
                "uses agents, states, "
                "actions, and rewards.",

            "metadata": {
                "source":
                    "document_006"
            },

            "distance": 0.25
        }
    ]

    response = build_response(
        answer=(
            "Reinforcement learning "
            "uses rewards to guide learning."
        ),
        retrieved_chunks=retrieved_chunks,
        status="answered"
    )

    assert response.status == "answered"

    assert response.answer

    assert len(response.sources) == 1

    assert (
        response.sources[0].chunk_id
        == "document_006_chunk_000"
    )

    assert (
        response.sources[0].source
        == "document_006"
    )

    assert (
        response.sources[0].distance
        == 0.25
    )


def test_empty_retrieval_creates_no_sources():

    response = build_response(
        answer=(
            "Information is not available "
            "in the provided documents."
        ),
        retrieved_chunks=[],
        status="insufficient_evidence"
    )

    assert (
        response.status
        == "insufficient_evidence"
    )

    assert response.answer

    assert response.sources == []


def test_response_can_be_converted_to_dict():

    retrieved_chunks = [
        {
            "chunk_id":
                "document_006_chunk_000",

            "text":
                "Reinforcement Learning "
                "uses rewards.",

            "metadata": {
                "source":
                    "document_006"
            },

            "distance": 0.30
        }
    ]

    response = build_response(
        answer="Reinforcement learning uses rewards.",
        retrieved_chunks=retrieved_chunks
    )

    result = response.to_dict()

    assert "answer" in result
    assert "sources" in result
    assert "status" in result

    assert (
        result["sources"][0]["chunk_id"]
        == "document_006_chunk_000"
    )