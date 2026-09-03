from src.rag.abstention import (
    has_sufficient_evidence,
    should_abstain,
    get_abstention_response
)


def test_sufficient_evidence_passes():

    chunks = [
        {
            "chunk_id":
                "document_006_chunk_000",

            "distance": 0.25
        }
    ]

    assert has_sufficient_evidence(
        chunks,
        max_distance=0.80
    )


def test_insufficient_evidence_fails():

    chunks = [
        {
            "chunk_id":
                "document_029_chunk_000",

            "distance": 1.35
        }
    ]

    assert not has_sufficient_evidence(
        chunks,
        max_distance=0.80
    )


def test_empty_retrieval_requires_abstention():

    assert should_abstain(
        [],
        max_distance=0.80
    )


def test_high_distance_requires_abstention():

    chunks = [
        {
            "chunk_id":
                "document_029_chunk_000",

            "distance": 1.50
        },
        {
            "chunk_id":
                "document_026_chunk_000",

            "distance": 1.40
        }
    ]

    assert should_abstain(
        chunks,
        max_distance=0.80
    )


def test_low_distance_does_not_abstain():

    chunks = [
        {
            "chunk_id":
                "document_006_chunk_000",

            "distance": 0.30
        }
    ]

    assert not should_abstain(
        chunks,
        max_distance=0.80
    )


def test_abstention_response_is_safe():

    response = get_abstention_response()

    assert (
        response["status"]
        == "insufficient_evidence"
    )

    assert (
        response["answer"]
        == (
            "Information is not available "
            "in the provided documents."
        )
    )

    assert response["sources"] == []