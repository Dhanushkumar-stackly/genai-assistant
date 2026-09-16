from typing import Iterable


def _normalise_ids(
    source_ids: Iterable[str],
) -> list[str]:
    """Convert source IDs to a clean list while preserving order."""

    return [
        source_id
        for source_id in source_ids
        if source_id
    ]


def hit_at_k(
    expected_source_ids: Iterable[str],
    retrieved_source_ids: Iterable[str],
    k: int,
) -> float:
    """Return 1.0 when an expected source appears in the top-k results."""

    if k <= 0:
        return 0.0

    expected = set(
        _normalise_ids(expected_source_ids)
    )

    retrieved = _normalise_ids(
        retrieved_source_ids
    )[:k]

    if not expected:
        return 0.0

    return 1.0 if expected.intersection(retrieved) else 0.0


def recall_at_k(
    expected_source_ids: Iterable[str],
    retrieved_source_ids: Iterable[str],
    k: int,
) -> float:
    """Calculate the fraction of expected sources found in top-k results."""

    if k <= 0:
        return 0.0

    expected = set(
        _normalise_ids(expected_source_ids)
    )

    retrieved = set(
        _normalise_ids(retrieved_source_ids)[:k]
    )

    if not expected:
        return 0.0

    found = expected.intersection(retrieved)

    return len(found) / len(expected)


def reciprocal_rank(
    expected_source_ids: Iterable[str],
    retrieved_source_ids: Iterable[str],
) -> float:
    """Return the reciprocal rank of the first expected source."""

    expected = set(
        _normalise_ids(expected_source_ids)
    )

    retrieved = _normalise_ids(
        retrieved_source_ids
    )

    if not expected:
        return 0.0

    for rank, source_id in enumerate(
        retrieved,
        start=1,
    ):
        if source_id in expected:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    cases: Iterable[
        tuple[
            Iterable[str],
            Iterable[str],
        ]
    ],
) -> float:
    """Calculate MRR across multiple evaluation cases."""

    reciprocal_ranks = [
        reciprocal_rank(
            expected_source_ids,
            retrieved_source_ids,
        )
        for expected_source_ids, retrieved_source_ids in cases
    ]

    if not reciprocal_ranks:
        return 0.0

    return sum(reciprocal_ranks) / len(
        reciprocal_ranks
    )


def grade_retrieval_case(
    expected_source_ids: Iterable[str],
    retrieved_source_ids: Iterable[str],
    k: int = 3,
) -> dict[str, float]:
    """Calculate retrieval metrics for one evaluation case."""

    return {
        "hit_at_k": hit_at_k(
            expected_source_ids,
            retrieved_source_ids,
            k,
        ),
        "recall_at_k": recall_at_k(
            expected_source_ids,
            retrieved_source_ids,
            k,
        ),
        "reciprocal_rank": reciprocal_rank(
            expected_source_ids,
            retrieved_source_ids,
        ),
    }