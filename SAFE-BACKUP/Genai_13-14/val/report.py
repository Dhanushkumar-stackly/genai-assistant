from typing import Any


def build_evaluation_report(
    *,
    scorecard: dict[str, float],
    regression: dict[str, Any],
) -> dict[str, Any]:
    """Build a consolidated evaluation report."""

    regression_detected = bool(
        regression.get(
            "regression_detected",
            False,
        )
    )

    status = (
        "REGRESSION"
        if regression_detected
        else "PASS"
    )

    return {
        "status": status,
        "scorecard": scorecard,
        "regression": regression,
    }


def is_evaluation_passed(
    report: dict[str, Any],
) -> bool:
    """Return True when the evaluation report passes."""

    return report.get("status") == "PASS"


def get_overall_score(
    report: dict[str, Any],
) -> float:
    """Return the overall score from an evaluation report."""

    scorecard = report.get(
        "scorecard",
        {},
    )

    return float(
        scorecard.get(
            "overall_score",
            0.0,
        )
    )