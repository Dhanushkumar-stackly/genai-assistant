from typing import Iterable


RETRIEVAL_METRICS = (
    "hit_at_k",
    "recall_at_k",
    "reciprocal_rank",
)

ANSWER_METRICS = (
    "answerability_correct",
    "citation_present",
    "citation_valid",
    "required_facts_correct",
    "abstention_correct",
)


def _average(values: Iterable[float]) -> float:
    """Return the average of numeric values."""

    values = list(values)

    if not values:
        return 0.0

    return sum(values) / len(values)


def calculate_retrieval_score(
    retrieval_results: Iterable[dict[str, float]],
) -> float:
    """Calculate the average retrieval score."""

    results = list(retrieval_results)

    if not results:
        return 0.0

    case_scores = []

    for result in results:
        metric_values = [
            float(result.get(metric, 0.0))
            for metric in RETRIEVAL_METRICS
        ]

        case_scores.append(
            _average(metric_values)
        )

    return _average(case_scores)


def calculate_answer_score(
    answer_results: Iterable[dict[str, bool]],
) -> float:
    """Calculate the average answer-quality score."""

    results = list(answer_results)

    if not results:
        return 0.0

    case_scores = []

    for result in results:
        metric_values = [
            1.0
            if result.get(metric, False)
            else 0.0
            for metric in ANSWER_METRICS
        ]

        case_scores.append(
            _average(metric_values)
        )

    return _average(case_scores)


def calculate_overall_score(
    retrieval_score: float,
    answer_score: float,
) -> float:
    """Calculate the overall evaluation score."""

    return _average(
        [
            retrieval_score,
            answer_score,
        ]
    )


def build_scorecard(
    retrieval_results: Iterable[dict[str, float]],
    answer_results: Iterable[dict[str, bool]],
) -> dict[str, float]:
    """Build a consolidated evaluation scorecard."""

    retrieval_results = list(retrieval_results)
    answer_results = list(answer_results)

    retrieval_score = calculate_retrieval_score(
        retrieval_results
    )

    answer_score = calculate_answer_score(
        answer_results
    )

    overall_score = calculate_overall_score(
        retrieval_score,
        answer_score,
    )

    return {
        "retrieval_score": retrieval_score,
        "answer_score": answer_score,
        "overall_score": overall_score,
    }