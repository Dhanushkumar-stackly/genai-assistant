from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "outputs"

BASELINE_FILE = (
    OUTPUT_DIR / "day10_task1_baseline_results.json"
)

EXPERIMENT_FILE = (
    OUTPUT_DIR / "day10_task1_experiment_results.json"
)

REPORT_JSON = (
    OUTPUT_DIR / "day10_task5_before_after_report.json"
)

REPORT_TXT = (
    OUTPUT_DIR / "day10_task5_before_after_report.txt"
)


# ============================================================
# CONFIGURATION
# ============================================================

BASELINE_CONFIG = {
    "chunk_size": 1000,
    "overlap": 200,
    "top_k": 5,
}

EXPERIMENT_CONFIG = {
    "chunk_size": 500,
    "overlap": 100,
    "top_k": 5,
}

# Maximum allowed question-level regressions.
MAX_REGRESSIONS = 0


# ============================================================
# GENERIC HELPERS
# ============================================================

def _safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """Safely convert value to float."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """Safely convert value to int."""

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _get_first(
    record: dict,
    keys: list[str],
    default: Any = None,
) -> Any:
    """Return the first available value."""

    for key in keys:
        if key in record:
            return record[key]

    return default


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path: Path) -> Any:
    """Load JSON file."""

    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_json(
    path: Path,
    data: Any,
) -> None:
    """Save JSON file."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


# ============================================================
# METRICS
# ============================================================

def get_metrics(data: dict) -> dict:
    """
    Extract aggregate metrics.

    Supports both direct and nested 'metrics' structures.
    """

    metrics = data.get("metrics")

    if not isinstance(metrics, dict):
        metrics = data

    return {
        "total_questions": _safe_int(
            _get_first(
                metrics,
                [
                    "total_questions",
                    "num_questions",
                ],
                0,
            )
        ),

        "retrieval_recall": _safe_float(
            _get_first(
                metrics,
                [
                    "retrieval_recall",
                    "recall",
                ],
                0.0,
            )
        ),

        "top1_accuracy": _safe_float(
            _get_first(
                metrics,
                [
                    "top1_accuracy",
                    "top1",
                ],
                0.0,
            )
        ),

        "mrr": _safe_float(
            _get_first(
                metrics,
                ["mrr"],
                0.0,
            )
        ),

        "average_latency_ms": _safe_float(
            _get_first(
                metrics,
                [
                    "average_latency_ms",
                    "latency_ms",
                ],
                0.0,
            )
        ),
    }


# ============================================================
# QUESTION RESULTS
# ============================================================

def get_question_results(data: dict) -> list[dict]:
    """
    Extract question-level results.
    """

    possible_keys = [
        "details",
        "results",
        "question_results",
        "experiment_results",
        "per_question_results",
    ]

    for key in possible_keys:

        value = data.get(key)

        if isinstance(value, list):
            return value

    return []


def get_question_text(
    item: dict,
) -> str:
    """Get question text."""

    return str(
        _get_first(
            item,
            [
                "question",
                "query",
            ],
            "",
        )
    )


def get_retrieved_doc_ids(
    item: dict,
) -> list[str]:
    """Get retrieved document IDs."""

    value = _get_first(
        item,
        [
            "retrieved_doc_ids",
            "retrieved_documents",
            "documents",
        ],
        [],
    )

    if isinstance(value, list):
        return [
            str(value_item)
            for value_item in value
        ]

    return []


def get_expected_doc_id(
    item: dict,
) -> str | None:
    """Get expected document ID."""

    value = _get_first(
        item,
        [
            "expected_doc_id",
            "expected_document_id",
        ],
        None,
    )

    if value is None:
        return None

    return str(value)


def retrieval_success(
    item: dict,
) -> bool:
    """
    Determine retrieval success.

    Prefer explicit values.
    Otherwise compare expected document against retrieved IDs.
    """

    explicit = _get_first(
        item,
        [
            "retrieval_success",
            "success",
            "recovered",
        ],
        None,
    )

    if explicit is not None:
        return bool(explicit)

    expected = get_expected_doc_id(item)

    retrieved = get_retrieved_doc_ids(item)

    if expected is None:
        return False

    return expected in retrieved


def top1_success(
    item: dict,
) -> bool:
    """Determine Top-1 success."""

    explicit = _get_first(
        item,
        [
            "top1",
            "top1_correct",
            "top1_success",
        ],
        None,
    )

    if explicit is not None:
        return bool(explicit)

    expected = get_expected_doc_id(item)

    retrieved = get_retrieved_doc_ids(item)

    if expected is None:
        return False

    return (
        bool(retrieved)
        and retrieved[0] == expected
    )


def get_rank(
    item: dict,
) -> int | None:
    """Get expected document rank."""

    explicit = _get_first(
        item,
        [
            "rank",
            "expected_rank",
            "correct_rank",
        ],
        None,
    )

    if explicit is not None:

        try:
            return int(explicit)
        except (
            TypeError,
            ValueError,
        ):
            return None

    expected = get_expected_doc_id(item)

    retrieved = get_retrieved_doc_ids(item)

    if expected is None:
        return None

    try:
        return (
            retrieved.index(expected)
            + 1
        )
    except ValueError:
        return None


def get_latency(
    item: dict,
) -> float:
    """Get question-level latency."""

    return _safe_float(
        _get_first(
            item,
            [
                "latency_ms",
                "average_latency_ms",
                "latency",
            ],
            0.0,
        )
    )


# ============================================================
# BEFORE / AFTER QUESTION COMPARISON
# ============================================================

def compare_questions(
    baseline_questions: list[dict],
    experiment_questions: list[dict],
) -> list[dict]:
    """
    Compare every question before and after the experiment.
    """

    if not isinstance(
        baseline_questions,
        list,
    ):
        raise TypeError(
            "baseline_questions must be a list"
        )

    if not isinstance(
        experiment_questions,
        list,
    ):
        raise TypeError(
            "experiment_questions must be a list"
        )

    # Match by question text where possible.
    experiment_map = {
        get_question_text(item): item
        for item in experiment_questions
        if isinstance(item, dict)
    }

    results = []

    for index, baseline in enumerate(
        baseline_questions
    ):

        if not isinstance(
            baseline,
            dict,
        ):
            continue

        question = get_question_text(
            baseline
        )

        experiment = experiment_map.get(
            question
        )

        # Fallback to positional matching.
        if experiment is None:

            if index < len(
                experiment_questions
            ):
                experiment = (
                    experiment_questions[index]
                )
            else:
                experiment = {}

        baseline_retrieval = retrieval_success(
            baseline
        )

        experiment_retrieval = retrieval_success(
            experiment
        )

        baseline_top1 = top1_success(
            baseline
        )

        experiment_top1 = top1_success(
            experiment
        )

        baseline_rank = get_rank(
            baseline
        )

        experiment_rank = get_rank(
            experiment
        )

        baseline_latency = get_latency(
            baseline
        )

        experiment_latency = get_latency(
            experiment
        )

        # ----------------------------------------------------
        # Outcome
        # ----------------------------------------------------

        baseline_quality = (
            int(baseline_retrieval),
            int(baseline_top1),
        )

        experiment_quality = (
            int(experiment_retrieval),
            int(experiment_top1),
        )

        if (
            experiment_quality
            > baseline_quality
        ):

            outcome = "improved"

        elif (
            experiment_quality
            < baseline_quality
        ):

            outcome = "regressed"

        else:

            # Same retrieval and Top-1.
            # Compare rank as secondary signal.
            if (
                baseline_rank is not None
                and experiment_rank is not None
            ):

                if (
                    experiment_rank
                    < baseline_rank
                ):
                    outcome = "improved"

                elif (
                    experiment_rank
                    > baseline_rank
                ):
                    outcome = "regressed"

                else:
                    outcome = "unchanged"

            else:
                outcome = "unchanged"

        results.append(
            {
                "question_number": (
                    index + 1
                ),

                "question": question,

                "baseline_retrieval_success":
                    baseline_retrieval,

                "experiment_retrieval_success":
                    experiment_retrieval,

                "baseline_top1":
                    baseline_top1,

                "experiment_top1":
                    experiment_top1,

                "baseline_rank":
                    baseline_rank,

                "experiment_rank":
                    experiment_rank,

                "baseline_latency_ms":
                    baseline_latency,

                "experiment_latency_ms":
                    experiment_latency,

                "outcome":
                    outcome,
            }
        )

    return results


# ============================================================
# METRIC CHANGE
# ============================================================

def build_metric_summary(
    baseline: dict,
    experiment: dict,
) -> dict:
    """
    Build before/after aggregate metric summary.
    """

    baseline_metrics = get_metrics(
        baseline
    )

    experiment_metrics = get_metrics(
        experiment
    )

    change = {}

    for metric in [
        "retrieval_recall",
        "top1_accuracy",
        "mrr",
        "average_latency_ms",
    ]:

        change[metric] = round(
            experiment_metrics[metric]
            - baseline_metrics[metric],
            4,
        )

    return {
        "baseline": baseline_metrics,
        "experiment": experiment_metrics,
        "change": change,
    }


# ============================================================
# CONFIGURATION DECISION
# ============================================================

def choose_configuration(
    metric_summary: dict,
    comparison: list[dict],
) -> dict:
    """
    Choose the best configuration.

    Candidate is selected ONLY when:

        - Recall improves
        - Top-1 does not regress
        - MRR does not regress
        - Question-level regressions are acceptable

    This prevents a small recall gain from hiding
    a significant ranking-quality regression.
    """

    change = metric_summary["change"]

    recall_change = _safe_float(
        change.get(
            "retrieval_recall",
            0.0,
        )
    )

    top1_change = _safe_float(
        change.get(
            "top1_accuracy",
            0.0,
        )
    )

    mrr_change = _safe_float(
        change.get(
            "mrr",
            0.0,
        )
    )

    latency_change = _safe_float(
        change.get(
            "average_latency_ms",
            0.0,
        )
    )

    improved_questions = sum(
        1
        for item in comparison
        if item.get("outcome") == "improved"
    )

    regressed_questions = sum(
        1
        for item in comparison
        if item.get("outcome") == "regressed"
    )

    unchanged_questions = sum(
        1
        for item in comparison
        if item.get("outcome") == "unchanged"
    )

    # --------------------------------------------------------
    # Selection criteria
    # --------------------------------------------------------

    recall_improved = (
        recall_change > 0
    )

    top1_not_regressed = (
        top1_change >= 0
    )

    mrr_not_regressed = (
        mrr_change >= 0
    )

    question_regressions_acceptable = (
        regressed_questions
        <= MAX_REGRESSIONS
    )

    accepted = (
        recall_improved
        and top1_not_regressed
        and mrr_not_regressed
        and question_regressions_acceptable
    )

    # --------------------------------------------------------
    # Decision
    # --------------------------------------------------------

    if accepted:

        selected_configuration = (
            "experiment"
        )

        reason = (
            "Experiment selected because "
            "retrieval recall improved, Top-1 "
            "accuracy and MRR did not regress, "
            "and there were no unacceptable "
            "question-level regressions."
        )

    else:

        selected_configuration = (
            "baseline"
        )

        rejection_reasons = []

        if not recall_improved:
            rejection_reasons.append(
                "retrieval recall did not improve"
            )

        if not top1_not_regressed:
            rejection_reasons.append(
                "Top-1 accuracy regressed"
            )

        if not mrr_not_regressed:
            rejection_reasons.append(
                "MRR regressed"
            )

        if not question_regressions_acceptable:
            rejection_reasons.append(
                "question-level regressions exceeded "
                "the acceptable limit"
            )

        reason = (
            "Baseline retained because "
            + "; ".join(
                rejection_reasons
            )
            + "."
        )

    return {
        "selected_configuration":
            selected_configuration,

        "accepted":
            accepted,

        "improved_questions":
            improved_questions,

        "regressed_questions":
            regressed_questions,

        "unchanged_questions":
            unchanged_questions,

        "latency_change_ms":
            latency_change,

        "retrieval_recall_change":
            recall_change,

        "top1_accuracy_change":
            top1_change,

        "mrr_change":
            mrr_change,

        "criteria": {
            "recall_improved":
                recall_improved,

            "top1_not_regressed":
                top1_not_regressed,

            "mrr_not_regressed":
                mrr_not_regressed,

            "question_regressions_acceptable":
                question_regressions_acceptable,
        },

        "reason":
            reason,
    }


# ============================================================
# REJECTED APPROACHES
# ============================================================

def build_rejected_approaches() -> list[dict]:
    """
    Document approaches that were not selected.
    """

    return [
        {
            "approach":
                "top_k = 10",

            "status":
                "rejected",

            "configuration": {
                "top_k": 10,
                "chunk_size": 1000,
                "overlap": 200,
            },

            "reason":
                "No retrieval improvement was observed "
                "in the earlier controlled top-k experiment.",
        }
    ]


# ============================================================
# TEXT REPORT
# ============================================================

def create_text_report(
    metric_summary: dict,
    comparison: list[dict],
    decision: dict,
    rejected: list[dict],
) -> str:
    """
    Create complete before-and-after report.
    """

    baseline = metric_summary[
        "baseline"
    ]

    experiment = metric_summary[
        "experiment"
    ]

    change = metric_summary[
        "change"
    ]

    lines = []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    lines.append("=" * 70)
    lines.append("DAY 10 - TASK 5")
    lines.append(
        "BEFORE-AND-AFTER EXPERIMENT REPORT"
    )
    lines.append("=" * 70)

    # --------------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------------

    lines.append("")
    lines.append(
        "EXPERIMENT CONFIGURATION"
    )
    lines.append("-" * 70)

    lines.append(
        "Baseline Chunk Size      : "
        f"{BASELINE_CONFIG['chunk_size']}"
    )

    lines.append(
        "Baseline Overlap         : "
        f"{BASELINE_CONFIG['overlap']}"
    )

    lines.append(
        "Experiment Chunk Size    : "
        f"{EXPERIMENT_CONFIG['chunk_size']}"
    )

    lines.append(
        "Experiment Overlap       : "
        f"{EXPERIMENT_CONFIG['overlap']}"
    )

    lines.append(
        "Top K                    : "
        f"{BASELINE_CONFIG['top_k']}"
    )

    # --------------------------------------------------------
    # AGGREGATE METRICS
    # --------------------------------------------------------

    lines.append("")
    lines.append(
        "AGGREGATE METRICS"
    )
    lines.append("-" * 70)

    lines.append(
        f"{'Metric':<25}"
        f"{'Before':>12}"
        f"{'After':>12}"
        f"{'Change':>12}"
    )

    lines.append(
        f"{'Retrieval Recall':<25}"
        f"{baseline['retrieval_recall']:>12.4f}"
        f"{experiment['retrieval_recall']:>12.4f}"
        f"{change['retrieval_recall']:+12.4f}"
    )

    lines.append(
        f"{'Top-1 Accuracy':<25}"
        f"{baseline['top1_accuracy']:>12.4f}"
        f"{experiment['top1_accuracy']:>12.4f}"
        f"{change['top1_accuracy']:+12.4f}"
    )

    lines.append(
        f"{'MRR':<25}"
        f"{baseline['mrr']:>12.4f}"
        f"{experiment['mrr']:>12.4f}"
        f"{change['mrr']:+12.4f}"
    )

    lines.append(
        f"{'Average Latency (ms)':<25}"
        f"{baseline['average_latency_ms']:>12.2f}"
        f"{experiment['average_latency_ms']:>12.2f}"
        f"{change['average_latency_ms']:+12.2f}"
    )

    # --------------------------------------------------------
    # PER QUESTION
    # --------------------------------------------------------

    lines.append("")
    lines.append(
        "PER-QUESTION RESULTS"
    )
    lines.append("-" * 70)

    if not comparison:

        lines.append(
            "No per-question comparison records found."
        )

    else:

        for item in comparison:

            lines.append("")

            lines.append(
                f"Question {item.get('question_number')}"
            )

            lines.append(
                "Question      : "
                f"{item.get('question', '')}"
            )

            lines.append(
                "Before        : "
                f"retrieval="
                f"{item.get('baseline_retrieval_success')}, "
                f"top1="
                f"{item.get('baseline_top1')}, "
                f"rank="
                f"{item.get('baseline_rank')}"
            )

            lines.append(
                "After         : "
                f"retrieval="
                f"{item.get('experiment_retrieval_success')}, "
                f"top1="
                f"{item.get('experiment_top1')}, "
                f"rank="
                f"{item.get('experiment_rank')}"
            )

            lines.append(
                "Latency       : "
                f"{_safe_float(item.get('baseline_latency_ms')):.2f} ms"
                f" -> "
                f"{_safe_float(item.get('experiment_latency_ms')):.2f} ms"
            )

            lines.append(
                "Outcome       : "
                f"{item.get('outcome', 'unchanged')}"
            )

    # --------------------------------------------------------
    # TRADE-OFF
    # --------------------------------------------------------

    lines.append("")
    lines.append(
        "TRADE-OFF ANALYSIS"
    )
    lines.append("-" * 70)

    lines.append(
        "Improved Questions : "
        f"{decision.get('improved_questions', 0)}"
    )

    lines.append(
        "Regressed Questions: "
        f"{decision.get('regressed_questions', 0)}"
    )

    lines.append(
        "Unchanged Questions: "
        f"{decision.get('unchanged_questions', 0)}"
    )

    lines.append(
        "Latency Change     : "
        f"{decision.get('latency_change_ms', 0.0):+.2f} ms"
    )

    # --------------------------------------------------------
    # SELECTED CONFIGURATION
    # --------------------------------------------------------

    lines.append("")
    lines.append(
        "SELECTED CONFIGURATION"
    )
    lines.append("-" * 70)

    selected = decision.get(
        "selected_configuration",
        "baseline",
    )

    if selected == "experiment":

        lines.append(
            "Selected            : experiment"
        )

        lines.append(
            "Chunk Size          : 500"
        )

        lines.append(
            "Overlap             : 100"
        )

        lines.append(
            "Top K               : 5"
        )

    else:

        lines.append(
            "Selected            : baseline"
        )

        lines.append(
            "Chunk Size          : 1000"
        )

        lines.append(
            "Overlap             : 200"
        )

        lines.append(
            "Top K               : 5"
        )

    lines.append(
        "Decision            : "
        f"{decision.get('reason', '')}"
    )

    # --------------------------------------------------------
    # REJECTED APPROACHES
    # --------------------------------------------------------

    lines.append("")
    lines.append(
        "REJECTED APPROACHES"
    )
    lines.append("-" * 70)

    if not rejected:

        lines.append(
            "No rejected approaches recorded."
        )

    else:

        for item in rejected:

            if not isinstance(item, dict):
                continue

            lines.append(
                f"{item.get('approach', 'Unknown approach')} "
                f"[{item.get('status', 'rejected')}]"
            )

            lines.append(
                "Configuration : "
                f"{item.get('configuration', 'Not specified')}"
            )

            lines.append(
                "Reason        : "
                f"{item.get('reason', 'No reason specified')}"
            )

    # --------------------------------------------------------
    # CONCLUSION
    # --------------------------------------------------------

    lines.append("")
    lines.append(
        "CONCLUSION"
    )
    lines.append("-" * 70)

    if selected == "experiment":

        lines.append(
            "The experiment configuration was selected "
            "because it improved retrieval performance "
            "without unacceptable regression."
        )

    else:

        lines.append(
            "The baseline configuration was retained "
            "because the experiment did not provide "
            "an acceptable trade-off."
        )

    lines.append(
        "Latency impact and question-level results "
        "were included in the final decision."
    )

    lines.append("")
    lines.append(
        "Generated at       : "
        f"{datetime.now().isoformat(timespec='seconds')}"
    )

    lines.append("=" * 70)

    return "\n".join(lines)


# ============================================================
# JSON REPORT
# ============================================================

def create_json_report(
    metric_summary: dict,
    comparison: list[dict],
    decision: dict,
    rejected: list[dict],
) -> dict:
    """
    Build machine-readable report.
    """

    return {
        "task":
            "DAY 10 - TASK 5",

        "report_type":
            "before_and_after",

        "generated_at":
            datetime.now().isoformat(
                timespec="seconds"
            ),

        "experiment_configuration": {
            "baseline":
                BASELINE_CONFIG,

            "experiment":
                EXPERIMENT_CONFIG,
        },

        "metric_summary":
            metric_summary,

        "per_question_results":
            comparison,

        "tradeoff_decision":
            decision,

        "rejected_approaches":
            rejected,

        "selected_configuration":
            decision.get(
                "selected_configuration"
            ),
    }


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("=" * 70)
    print("DAY 10 - TASK 5")
    print(
        "BEFORE-AND-AFTER EXPERIMENT REPORT"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print(
        "\nLoading baseline results..."
    )

    baseline_data = load_json(
        BASELINE_FILE
    )

    print(
        "Loading experiment results..."
    )

    experiment_data = load_json(
        EXPERIMENT_FILE
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    metric_summary = build_metric_summary(
        baseline_data,
        experiment_data,
    )

    # --------------------------------------------------------
    # Question-level data
    # --------------------------------------------------------

    baseline_questions = (
        get_question_results(
            baseline_data
        )
    )

    experiment_questions = (
        get_question_results(
            experiment_data
        )
    )

    comparison = compare_questions(
        baseline_questions,
        experiment_questions,
    )

    # --------------------------------------------------------
    # Decision
    # --------------------------------------------------------

    decision = choose_configuration(
        metric_summary,
        comparison,
    )

    # --------------------------------------------------------
    # Rejected approaches
    # --------------------------------------------------------

    rejected = (
        build_rejected_approaches()
    )

    # --------------------------------------------------------
    # Reports
    # --------------------------------------------------------

    text_report = create_text_report(
        metric_summary,
        comparison,
        decision,
        rejected,
    )

    json_report = create_json_report(
        metric_summary,
        comparison,
        decision,
        rejected,
    )

    REPORT_TXT.write_text(
        text_report,
        encoding="utf-8",
    )

    save_json(
        REPORT_JSON,
        json_report,
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print()
    print(text_report)

    print()
    print("=" * 70)
    print(
        "TASK 5 REPORT GENERATED SUCCESSFULLY"
    )
    print("=" * 70)

    print(
        f"Text report : {REPORT_TXT}"
    )

    print(
        f"JSON report : {REPORT_JSON}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()