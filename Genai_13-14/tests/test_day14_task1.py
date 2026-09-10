from eval.graders.retrieval_grader import (
    grade_retrieval_case,
    hit_at_k,
    mean_reciprocal_rank,
    recall_at_k,
    reciprocal_rank,
)


def test_hit_at_k_when_expected_source_is_present():
    assert (
        hit_at_k(
            ["doc-A"],
            ["doc-B", "doc-A", "doc-C"],
            3,
        )
        == 1.0
    )


def test_hit_at_k_when_expected_source_is_missing():
    assert (
        hit_at_k(
            ["doc-A"],
            ["doc-B", "doc-C"],
            2,
        )
        == 0.0
    )


def test_recall_at_k_for_multiple_expected_sources():
    assert (
        recall_at_k(
            ["doc-A", "doc-B"],
            ["doc-A", "doc-C", "doc-B"],
            3,
        )
        == 1.0
    )


def test_recall_at_k_for_partial_retrieval():
    assert (
        recall_at_k(
            ["doc-A", "doc-B"],
            ["doc-A", "doc-C"],
            2,
        )
        == 0.5
    )


def test_reciprocal_rank_for_rank_one():
    assert (
        reciprocal_rank(
            ["doc-A"],
            ["doc-A", "doc-B"],
        )
        == 1.0
    )


def test_reciprocal_rank_for_rank_two():
    assert (
        reciprocal_rank(
            ["doc-A"],
            ["doc-B", "doc-A", "doc-C"],
        )
        == 0.5
    )


def test_reciprocal_rank_is_zero_when_not_retrieved():
    assert (
        reciprocal_rank(
            ["doc-A"],
            ["doc-B", "doc-C"],
        )
        == 0.0
    )


def test_mean_reciprocal_rank():
    cases = [
        (["doc-A"], ["doc-A"]),
        (["doc-B"], ["doc-C", "doc-B"]),
        (["doc-C"], ["doc-D", "doc-E", "doc-C"]),
    ]

    assert (
        mean_reciprocal_rank(cases)
        == (1.0 + 0.5 + (1.0 / 3.0)) / 3
    )


def test_grade_retrieval_case_returns_all_metrics():
    result = grade_retrieval_case(
        expected_source_ids=["doc-A"],
        retrieved_source_ids=[
            "doc-B",
            "doc-A",
            "doc-C",
        ],
        k=3,
    )

    assert result == {
        "hit_at_k": 1.0,
        "recall_at_k": 1.0,
        "reciprocal_rank": 0.5,
    } 