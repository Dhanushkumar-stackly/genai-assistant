from src.day10.task3_reranking import (
    rerank_candidates,
)


class FakeReranker:

    def predict(self, pairs):

        return [
            0.10,
            0.90,
            0.50,
        ]


def test_reranker_reorders_candidates():

    candidates = [
        {
            "original_rank": 1,
            "doc_id": "DOC-001",
            "chunk_id": "chunk-001",
            "original_distance": 0.20,
            "text": "first document",
        },
        {
            "original_rank": 2,
            "doc_id": "DOC-002",
            "chunk_id": "chunk-002",
            "original_distance": 0.30,
            "text": "second document",
        },
        {
            "original_rank": 3,
            "doc_id": "DOC-003",
            "chunk_id": "chunk-003",
            "original_distance": 0.40,
            "text": "third document",
        },
    ]

    results = rerank_candidates(
        "test question",
        candidates,
        FakeReranker(),
    )

    assert results[0]["doc_id"] == "DOC-002"

    assert results[0]["reranker_score"] == 0.90

    assert results[0]["final_rank"] == 1


def test_original_retrieval_score_is_preserved():

    candidates = [
        {
            "original_rank": 1,
            "doc_id": "DOC-001",
            "chunk_id": "chunk-001",
            "original_distance": 0.25,
            "text": "document",
        },
    ]

    results = rerank_candidates(
        "test question",
        candidates,
        FakeReranker(),
    )

    assert (
        "original_distance"
        in results[0]
    )

    assert (
        "reranker_score"
        in results[0]
    )

    assert (
        "final_rank"
        in results[0]
    )

    assert (
        results[0]["original_distance"]
        == 0.25
    )


def test_final_rank_is_present():

    candidates = [
        {
            "original_rank": 1,
            "doc_id": "DOC-001",
            "chunk_id": "chunk-001",
            "original_distance": 0.25,
            "text": "document",
        },
    ]

    results = rerank_candidates(
        "test question",
        candidates,
        FakeReranker(),
    )

    assert results[0]["final_rank"] == 1