import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "eval" / "golden_dataset.json"


def load_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_golden_dataset_exists():
    assert DATASET_PATH.exists()


def test_dataset_contains_at_least_25_cases():
    dataset = load_dataset()

    assert len(dataset["cases"]) >= 25


def test_case_ids_are_unique():
    dataset = load_dataset()

    case_ids = [case["case_id"] for case in dataset["cases"]]

    assert len(case_ids) == len(set(case_ids))


def test_all_required_categories_are_represented():
    dataset = load_dataset()

    categories = {
        case["category"]
        for case in dataset["cases"]
    }

    required_categories = {
        "answerable",
        "unanswerable",
        "ambiguous",
        "multi_document",
        "adversarial",
    }

    assert required_categories.issubset(categories)


def test_answerable_cases_have_expected_sources():
    dataset = load_dataset()

    answerable_cases = [
        case
        for case in dataset["cases"]
        if case["answerability"] == "answerable"
    ]

    assert answerable_cases

    for case in answerable_cases:
        assert len(case["expected_source_ids"]) >= 1


def test_unanswerable_cases_have_no_expected_sources():
    dataset = load_dataset()

    unanswerable_cases = [
        case
        for case in dataset["cases"]
        if case["answerability"] == "unanswerable"
    ]

    assert unanswerable_cases

    for case in unanswerable_cases:
        assert case["expected_source_ids"] == []


def test_every_case_has_required_fields():
    dataset = load_dataset()

    required_fields = {
        "case_id",
        "question",
        "category",
        "expected_source_ids",
        "answerability",
    }

    for case in dataset["cases"]:
        assert required_fields.issubset(case.keys())


def test_case_categories_have_expected_distribution():
    dataset = load_dataset()

    categories = [
        case["category"]
        for case in dataset["cases"]
    ]

    assert categories.count("answerable") == 5
    assert categories.count("unanswerable") == 5
    assert categories.count("ambiguous") == 5
    assert categories.count("multi_document") == 5
    assert categories.count("adversarial") == 5


def test_dataset_has_optional_review_fields():
    dataset = load_dataset()

    for case in dataset["cases"]:
        assert "expected_facts" in case
        assert "answer_notes" in case