from eval.regression import (
    calculate_difference,
    compare_scorecards,
    detect_regression,
)


def test_calculate_difference():
    assert calculate_difference(
        0.90,
        0.85,
    ) == -0.05


def test_no_regression_when_score_improves():
    assert detect_regression(
        0.90,
        0.95,
    ) is False


def test_regression_when_score_drops():
    assert detect_regression(
        0.90,
        0.80,
    ) is True


def test_threshold_allows_small_drop():
    assert detect_regression(
        0.90,
        0.89,
        threshold=0.02,
    ) is False


def test_threshold_detects_large_drop():
    assert detect_regression(
        0.90,
        0.85,
        threshold=0.02,
    ) is True


def test_compare_scorecards():
    baseline = {
        "retrieval_score": 0.90,
        "answer_score": 0.95,
        "overall_score": 0.925,
    }

    current = {
        "retrieval_score": 0.85,
        "answer_score": 0.96,
        "overall_score": 0.905,
    }

    result = compare_scorecards(
        baseline,
        current,
        threshold=0.02,
    )

    assert result["regression_detected"] is True
    assert result["metrics"]["retrieval_score"]["regression"] is True
    assert result["metrics"]["answer_score"]["regression"] is False


def test_compare_scorecards_no_regression():
    baseline = {
        "retrieval_score": 0.90,
        "answer_score": 0.90,
        "overall_score": 0.90,
    }

    current = {
        "retrieval_score": 0.92,
        "answer_score": 0.91,
        "overall_score": 0.915,
    }

    result = compare_scorecards(
        baseline,
        current,
    )

    assert result["regression_detected"] is False


def test_missing_metric_defaults_to_zero():
    baseline = {
        "retrieval_score": 0.90,
    }

    current = {
        "retrieval_score": 0.90,
    }

    result = compare_scorecards(
        baseline,
        current,
    )

    assert result["regression_detected"] is False