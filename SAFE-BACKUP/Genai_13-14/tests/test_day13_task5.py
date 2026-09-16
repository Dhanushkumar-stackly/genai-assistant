import json
from pathlib import Path

from eval.evaluation_runner import (
    create_timestamped_result_path,
    load_config,
    run_configured_evaluation,
    save_evaluation_result,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = (
    PROJECT_ROOT
    / "eval"
    / "config"
    / "evaluation_config.json"
)


def test_named_configuration_file_exists():
    assert CONFIG_PATH.exists()


def test_named_configuration_contains_required_values():
    config = load_config(CONFIG_PATH)

    assert config["runner_version"] == "1.0.0"
    assert config["dataset_version"] == "day13-v1"
    assert config["dataset_path"]
    assert config["results_dir"]


def test_timestamped_result_paths_are_different():
    results_dir = PROJECT_ROOT / "eval" / "results"

    first_path = create_timestamped_result_path(
        results_dir
    )

    second_path = create_timestamped_result_path(
        results_dir
    )

    assert first_path != second_path


def test_save_result_creates_json_artifact(tmp_path):
    report = {
        "total_cases": 25,
        "passed": 20,
        "failed": 5,
        "results": [],
    }

    config = {
        "runner_version": "1.0.0",
        "dataset_version": "day13-v1",
        "dataset_path": "eval/golden_dataset.json",
        "results_dir": "eval/results",
        "_config_path": str(CONFIG_PATH),
    }

    output_path = tmp_path / "evaluation_test.json"

    save_evaluation_result(
        report=report,
        config=config,
        output_path=output_path,
    )

    assert output_path.exists()

    with output_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        artifact = json.load(file)

    assert "run_metadata" in artifact
    assert "configuration" in artifact
    assert "report" in artifact


def test_result_artifact_contains_version_information(tmp_path):
    report = {
        "total_cases": 25,
        "passed": 20,
        "failed": 5,
        "results": [],
    }

    config = {
        "runner_version": "1.0.0",
        "dataset_version": "day13-v1",
        "dataset_path": "eval/golden_dataset.json",
        "results_dir": "eval/results",
        "_config_path": str(CONFIG_PATH),
    }

    output_path = tmp_path / "version_test.json"

    save_evaluation_result(
        report=report,
        config=config,
        output_path=output_path,
    )

    with output_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        artifact = json.load(file)

    metadata = artifact["run_metadata"]

    assert metadata["runner_version"] == "1.0.0"
    assert metadata["dataset_version"] == "day13-v1"


def test_configured_evaluation_uses_dataset():
    def responder(question: str) -> dict:
        return {
            "answer": "Demo answer",
            "sources": [],
        }

    report, output_path = run_configured_evaluation(
        responder=responder,
        config_path=CONFIG_PATH,
    )

    assert report["total_cases"] == 25
    assert output_path.exists()


def test_configured_evaluation_creates_timestamped_artifact():
    def responder(question: str) -> dict:
        return {
            "answer": "Demo answer",
            "sources": [],
        }

    _, first_path = run_configured_evaluation(
        responder=responder,
        config_path=CONFIG_PATH,
    )

    _, second_path = run_configured_evaluation(
        responder=responder,
        config_path=CONFIG_PATH,
    )

    assert first_path.exists()
    assert second_path.exists()
    assert first_path != second_path