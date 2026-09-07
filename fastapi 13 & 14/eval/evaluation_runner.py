import json
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "eval" / "golden_dataset.json"


def load_golden_dataset(
    dataset_path: Path = DATASET_PATH,
) -> dict[str, Any]:
    """Load the Day 13 golden evaluation dataset."""

    with dataset_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_case(
    case: dict[str, Any],
    response: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate one golden dataset case against an actual response."""

    expected_sources = set(
        case.get("expected_source_ids", [])
    )

    actual_sources = {
        source.get("document_id")
        for source in response.get("sources", [])
        if source.get("document_id")
    }

    answerability = case["answerability"]

    if answerability == "unanswerable":
        passed = len(actual_sources) == 0

    elif answerability == "ambiguous":
        passed = len(actual_sources) == 0

    else:
        passed = expected_sources.issubset(actual_sources)

    return {
        "case_id": case["case_id"],
        "question": case["question"],
        "expected_source_ids": sorted(expected_sources),
        "actual_source_ids": sorted(actual_sources),
        "answerability": answerability,
        "passed": passed,
    }


def run_evaluation(
    responder: Callable[[str], dict[str, Any]],
    dataset_path: Path = DATASET_PATH,
) -> dict[str, Any]:
    """Run evaluation against every case in the golden dataset."""

    dataset = load_golden_dataset(dataset_path)

    results: list[dict[str, Any]] = []

    for case in dataset["cases"]:
        response = responder(case["question"])

        result = evaluate_case(
            case=case,
            response=response,
        )

        results.append(result)

    passed_count = sum(
        1
        for result in results
        if result["passed"]
    )

    failed_count = len(results) - passed_count

    return {
        "total_cases": len(results),
        "passed": passed_count,
        "failed": failed_count,
        "results": results,
    }


if __name__ == "__main__":

    def demo_responder(
        question: str,
    ) -> dict[str, Any]:
        """Demo responder for local runner testing."""

        return {
            "answer": "Demo response",
            "sources": [],
        }

    report = run_evaluation(
        responder=demo_responder,
    )

    print(f"Total cases: {report['total_cases']}")
    print(f"Passed: {report['passed']}")
    print(f"Failed: {report['failed']}")