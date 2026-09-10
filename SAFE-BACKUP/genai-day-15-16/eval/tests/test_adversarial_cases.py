import json
from pathlib import Path


CASES_FILE = (
    Path(__file__).resolve().parents[1]
    / "eval"
    / "adversarial_cases.json"
)


REQUIRED_CATEGORIES = {
    "direct_prompt_injection",
    "retrieved_text_injection",
    "restricted_data_request",
    "conflicting_sources",
    "unsupported_request",
    "excessive_input",
    "malformed_payload",
    "instruction_override",
    "prompt_extraction",
    "malformed_query",
}


def load_cases():
    with CASES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_day15_task1_contains_ten_adversarial_cases():
    cases = load_cases()

    assert isinstance(cases, list)
    assert len(cases) == 10


def test_day15_task1_has_unique_case_ids():
    cases = load_cases()

    ids = [case["id"] for case in cases]

    assert len(ids) == len(set(ids))


def test_day15_task1_covers_required_categories():
    cases = load_cases()

    categories = {
        case["category"]
        for case in cases
    }

    assert categories == REQUIRED_CATEGORIES


def test_day15_task1_cases_have_required_fields():
    cases = load_cases()

    for case in cases:
        assert "id" in case
        assert "category" in case
        assert "input" in case
        assert "expected_behavior" in case

        assert isinstance(case["id"], str)
        assert isinstance(case["category"], str)
        assert isinstance(case["input"], str)
        assert isinstance(case["expected_behavior"], str)


def test_day15_task1_expected_behaviors_are_defined():
    cases = load_cases()

    for case in cases:
        assert case["expected_behavior"].strip() != ""