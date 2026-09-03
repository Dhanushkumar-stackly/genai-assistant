"""
DAY 10 - TASK 4
Choose the Best Configuration

Select the candidate configuration when it improves weak-case retrieval
without causing unacceptable regressions on previously good questions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs"

BASELINE_FILE = OUTPUT_DIR / "day10_task1_baseline_results.json"
EXPERIMENT_FILE = OUTPUT_DIR / "day10_task1_experiment_results.json"
OUTPUT_FILE = OUTPUT_DIR / "day10_task4_best_configuration.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_metric(data: dict[str, Any], name: str) -> float:
    metrics = data.get("metrics", data)

    value = metrics.get(name)

    if value is None:
        raise KeyError(f"Metric '{name}' not found")

    return float(value)


def get_details(data: dict[str, Any]) -> list[dict[str, Any]]:
    details = data.get("details")

    if isinstance(details, list):
        return details

    results = data.get("results")

    if isinstance(results, list):
        return results

    return []


def get_question_id(record: dict[str, Any]) -> str:
    return str(
        record.get(
            "question",
            record.get("query", ""),
        )
    )


def get_retrieved_ids(record: dict[str, Any]) -> list[str]:
    value = record.get("retrieved_doc_ids", [])

    if isinstance(value, list):
        return [str(x) for x in value]

    return []


def get_expected_id(record: dict[str, Any]) -> str | None:
    value = record.get("expected_doc_id")

    if value is None:
        return None

    return str(value)


def is_success(record: dict[str, Any]) -> bool:
    expected = get_expected_id(record)

    if expected is None:
        return False

    retrieved = get_retrieved_ids(record)

    return expected in retrieved


def evaluate_regressions(
    baseline_details: list[dict[str, Any]],
    experiment_details: list[dict[str, Any]],
) -> dict[str, Any]:
    baseline_map = {
        get_question_id(item): item
        for item in baseline_details
        if get_question_id(item)
    }

    experiment_map = {
        get_question_id(item): item
        for item in experiment_details
        if get_question_id(item)
    }

    previously_good = 0
    regressed = 0
    improved = 0

    regression_questions: list[str] = []
    improved_questions: list[str] = []

    for question, baseline in baseline_map.items():

        if not is_success(baseline):
            continue

        previously_good += 1

        experiment = experiment_map.get(question)

        if experiment is None:
            regressed += 1
            regression_questions.append(question)
            continue

        if is_success(experiment):
            continue

        regressed += 1
        regression_questions.append(question)

    for question, experiment in experiment_map.items():

        if question not in baseline_map:
            continue

        baseline = baseline_map[question]

        if not is_success(baseline) and is_success(experiment):
            improved += 1
            improved_questions.append(question)

    return {
        "previously_good_questions": previously_good,
        "regressions": regressed,
        "improvements": improved,
        "regression_questions": regression_questions,
        "improved_questions": improved_questions,
    }


def choose_configuration(
    baseline: dict[str, Any],
    experiment: dict[str, Any],
) -> dict[str, Any]:

    baseline_recall = get_metric(
        baseline,
        "retrieval_recall",
    )

    experiment_recall = get_metric(
        experiment,
        "retrieval_recall",
    )

    baseline_top1 = get_metric(
        baseline,
        "top1_accuracy",
    )

    experiment_top1 = get_metric(
        experiment,
        "top1_accuracy",
    )

    baseline_mrr = get_metric(
        baseline,
        "mrr",
    )

    experiment_mrr = get_metric(
        experiment,
        "mrr",
    )

    baseline_details = get_details(baseline)
    experiment_details = get_details(experiment)

    regression_info = evaluate_regressions(
        baseline_details,
        experiment_details,
    )

    recall_improved = experiment_recall > baseline_recall

    top1_not_worse = experiment_top1 >= baseline_top1
    mrr_not_worse = experiment_mrr >= baseline_mrr

    no_unacceptable_regression = (
        regression_info["regressions"] == 0
    )

    candidate_selected = (
        recall_improved
        and top1_not_worse
        and mrr_not_worse
        and no_unacceptable_regression
    )

    if candidate_selected:
        selected = "experiment"
        decision = "SELECT_CANDIDATE"
        reason = (
            "The candidate configuration improved retrieval "
            "performance without regressing previously good questions."
        )
    else:
        selected = "baseline"
        decision = "KEEP_BASELINE"
        reason = (
            "The candidate configuration did not satisfy all "
            "selection criteria."
        )

    return {
        "selected_configuration": selected,
        "decision": decision,
        "reason": reason,
        "metrics": {
            "baseline": {
                "retrieval_recall": baseline_recall,
                "top1_accuracy": baseline_top1,
                "mrr": baseline_mrr,
            },
            "experiment": {
                "retrieval_recall": experiment_recall,
                "top1_accuracy": experiment_top1,
                "mrr": experiment_mrr,
            },
        },
        "regression_analysis": regression_info,
        "criteria": {
            "recall_improved": recall_improved,
            "top1_not_worse": top1_not_worse,
            "mrr_not_worse": mrr_not_worse,
            "no_unacceptable_regression": no_unacceptable_regression,
        },
        "configuration": {
            "baseline": {
                "chunk_size": 1000,
                "overlap": 200,
                "top_k": 5,
            },
            "experiment": {
                "chunk_size": 500,
                "overlap": 100,
                "top_k": 5,
            },
        },
    }


def save_result(result: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=2,
            ensure_ascii=False,
        )


def main() -> None:

    print("=" * 70)
    print("DAY 10 - TASK 4")
    print("CHOOSE THE BEST CONFIGURATION")
    print("=" * 70)

    baseline = load_json(BASELINE_FILE)
    experiment = load_json(EXPERIMENT_FILE)

    result = choose_configuration(
        baseline,
        experiment,
    )

    save_result(result)

    print()
    print("BASELINE")
    print("-" * 70)
    print("Chunk Size : 1000")
    print("Overlap    : 200")
    print("Top K      : 5")
    print(
        f"Recall     : "
        f"{result['metrics']['baseline']['retrieval_recall']:.4f}"
    )

    print()
    print("CANDIDATE")
    print("-" * 70)
    print("Chunk Size : 500")
    print("Overlap    : 100")
    print("Top K      : 5")
    print(
        f"Recall     : "
        f"{result['metrics']['experiment']['retrieval_recall']:.4f}"
    )

    print()
    print("REGRESSION ANALYSIS")
    print("-" * 70)

    info = result["regression_analysis"]

    print(
        "Previously Good :",
        info["previously_good_questions"],
    )

    print(
        "Regressions     :",
        info["regressions"],
    )

    print(
        "Improvements    :",
        info["improvements"],
    )

    print()
    print("DECISION")
    print("-" * 70)

    if result["decision"] == "SELECT_CANDIDATE":
        print("Selected : CANDIDATE")
        print("Config   : chunk_size=500, overlap=100, top_k=5")
    else:
        print("Selected : BASELINE")
        print("Config   : chunk_size=1000, overlap=200, top_k=5")

    print()
    print("Reason:")
    print(result["reason"])

    print()
    print("=" * 70)
    print("DAY 10 - TASK 4 COMPLETE")
    print("=" * 70)
    print()
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()