import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONFIG_PATH = (
    PROJECT_ROOT
    / "eval"
    / "config"
    / "evaluation_config.json"
)

DEFAULT_DATASET_PATH = (
    PROJECT_ROOT
    / "eval"
    / "golden_dataset.json"
)

DEFAULT_RESULTS_DIR = (
    PROJECT_ROOT
    / "eval"
    / "results"
)


def load_config(
    config_path: Path | None = None,
) -> dict[str, Any]:
    """Load evaluation configuration from a named file or environment."""

    if config_path is None:
        environment_config = os.getenv("EVAL_CONFIG")

        if environment_config:
            config_path = Path(environment_config)
        else:
            config_path = DEFAULT_CONFIG_PATH

    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    config["_config_path"] = str(config_path)

    return config


def resolve_path(
    path_value: str | None,
    default_path: Path,
) -> Path:
    """Resolve a project-relative or absolute path."""

    if not path_value:
        return default_path

    path = Path(path_value)

    if not path.is_absolute():
        path = PROJECT_ROOT / path

    return path


def load_golden_dataset(
    dataset_path: Path = DEFAULT_DATASET_PATH,
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
    dataset_path: Path = DEFAULT_DATASET_PATH,
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


def create_timestamped_result_path(
    results_dir: Path,
) -> Path:
    """Create a unique timestamped result path."""

    results_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%dT%H%M%S_%fZ"
    )

    result_path = (
        results_dir
        / f"evaluation_{timestamp}.json"
    )

    return result_path


def save_evaluation_result(
    report: dict[str, Any],
    config: dict[str, Any],
    output_path: Path,
) -> Path:
    """Save evaluation report with reproducibility metadata."""

    artifact = {
        "run_metadata": {
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "runner_version": config.get(
                "runner_version",
                "unknown",
            ),
            "dataset_version": config.get(
                "dataset_version",
                "unknown",
            ),
            "config_path": config.get(
                "_config_path",
            ),
        },
        "configuration": {
            key: value
            for key, value in config.items()
            if not key.startswith("_")
        },
        "report": report,
    }

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            artifact,
            file,
            indent=2,
        )

    return output_path


def run_configured_evaluation(
    responder: Callable[[str], dict[str, Any]],
    config_path: Path | None = None,
) -> tuple[dict[str, Any], Path]:
    """Run evaluation using the configured dataset and save a result artifact."""

    config = load_config(config_path)

    dataset_path = resolve_path(
        config.get("dataset_path"),
        DEFAULT_DATASET_PATH,
    )

    results_dir = resolve_path(
        config.get("results_dir"),
        DEFAULT_RESULTS_DIR,
    )

    report = run_evaluation(
        responder=responder,
        dataset_path=dataset_path,
    )

    output_path = create_timestamped_result_path(
        results_dir
    )

    save_evaluation_result(
        report=report,
        config=config,
        output_path=output_path,
    )

    return report, output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Day 13 evaluation runner."
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to evaluation configuration JSON.",
    )

    args = parser.parse_args()

    def demo_responder(
        question: str,
    ) -> dict[str, Any]:
        """Demo responder for local runner execution."""

        return {
            "answer": "Demo response",
            "sources": [],
        }

    report, output_path = run_configured_evaluation(
        responder=demo_responder,
        config_path=args.config,
    )

    print(f"Total cases: {report['total_cases']}")
    print(f"Passed: {report['passed']}")
    print(f"Failed: {report['failed']}")
    print(f"Result artifact: {output_path}")


if __name__ == "__main__":
    main()