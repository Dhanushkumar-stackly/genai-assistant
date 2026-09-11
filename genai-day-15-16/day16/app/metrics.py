"""
Day 16 - Task 5

Measure false accepts and false rejects for
adversarial and benign cases.
"""

from dataclasses import dataclass
from typing import Literal


CaseType = Literal["benign", "adversarial"]
Decision = Literal["allow", "block"]


@dataclass(frozen=True)
class EvaluationCase:
    """
    One evaluation case.

    expected_decision represents the safe decision that
    the application should make.
    """

    case_id: str
    case_type: CaseType
    input_text: str
    expected_decision: Decision
    actual_decision: Decision


@dataclass(frozen=True)
class MetricReport:
    """
    Aggregate evaluation metrics.
    """

    total_cases: int
    benign_cases: int
    adversarial_cases: int
    correct_cases: int
    false_accepts: int
    false_rejects: int
    accuracy: float
    false_accept_rate: float
    false_reject_rate: float


def evaluate_case(case: EvaluationCase) -> str:
    """
    Classify the outcome of a single evaluation case.
    """

    if (
        case.expected_decision == "block"
        and case.actual_decision == "allow"
    ):
        return "FALSE_ACCEPT"

    if (
        case.expected_decision == "allow"
        and case.actual_decision == "block"
    ):
        return "FALSE_REJECT"

    return "CORRECT"


def calculate_metrics(
    cases: list[EvaluationCase],
) -> MetricReport:
    """
    Calculate false accepts, false rejects and
    overall accuracy.
    """

    total = len(cases)

    if total == 0:
        raise ValueError(
            "At least one evaluation case is required"
        )

    benign = sum(
        case.case_type == "benign"
        for case in cases
    )

    adversarial = sum(
        case.case_type == "adversarial"
        for case in cases
    )

    false_accepts = sum(
        evaluate_case(case) == "FALSE_ACCEPT"
        for case in cases
    )

    false_rejects = sum(
        evaluate_case(case) == "FALSE_REJECT"
        for case in cases
    )

    correct = total - false_accepts - false_rejects

    return MetricReport(
        total_cases=total,
        benign_cases=benign,
        adversarial_cases=adversarial,
        correct_cases=correct,
        false_accepts=false_accepts,
        false_rejects=false_rejects,
        accuracy=correct / total,
        false_accept_rate=(
            false_accepts / adversarial
            if adversarial
            else 0.0
        ),
        false_reject_rate=(
            false_rejects / benign
            if benign
            else 0.0
        ),
    )


def compare_metrics(
    before: MetricReport,
    after: MetricReport,
) -> dict[str, float]:
    """
    Calculate the metric changes after tuning.
    """

    return {
        "false_accept_change": (
            after.false_accepts - before.false_accepts
        ),
        "false_reject_change": (
            after.false_rejects - before.false_rejects
        ),
        "accuracy_change": (
            after.accuracy - before.accuracy
        ),
        "false_accept_rate_change": (
            after.false_accept_rate
            - before.false_accept_rate
        ),
        "false_reject_rate_change": (
            after.false_reject_rate
            - before.false_reject_rate
        ),
    }