import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_FILE = (
    PROJECT_ROOT
    / "eval"
    / "baseline_results.json"
)


def test_baseline_results_file_exists():
    assert RESULTS_FILE.exists()


def test_baseline_contains_ten_cases():
    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    assert data["total_cases"] == 10
    assert len(data["results"]) == 10


def test_all_case_ids_are_unique():
    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    ids = [
        result["id"]
        for result in data["results"]
    ]

    assert len(ids) == len(set(ids))


def test_required_baseline_fields_exist():
    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    required_fields = {
        "id",
        "category",
        "input",
        "expected_behavior",
        "status_code",
        "actual_response",
        "classification",
        "latency_ms",
        "error",
    }

    for result in data["results"]:
        assert required_fields.issubset(
            result.keys()
        )