import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "eval" / "golden_dataset.json"
REVIEW_PATH = PROJECT_ROOT / "eval" / "dataset_review.md"


def load_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_review_notes_exist():
    assert REVIEW_PATH.exists()


def test_review_notes_contain_required_sections():
    review = REVIEW_PATH.read_text(encoding="utf-8")

    assert "# Day 13 Golden Dataset Review" in review
    assert "Review Objective" in review
    assert "Category Review" in review
    assert "Review Findings" in review
    assert "Dataset Consistency Checks" in review


def test_all_cases_have_scoreable_metadata():
    dataset = load_dataset()

    for case in dataset["cases"]:
        assert case["case_id"]
        assert case["question"]
        assert case["category"]
        assert case["answerability"]


def test_answerable_cases_are_scoreable():
    dataset = load_dataset()

    for case in dataset["cases"]:
        if case["answerability"] == "answerable":
            assert len(case["expected_source_ids"]) >= 1


def test_unanswerable_cases_are_scoreable():
    dataset = load_dataset()

    for case in dataset["cases"]:
        if case["answerability"] == "unanswerable":
            assert case["expected_source_ids"] == []


def test_multi_document_cases_have_multiple_sources():
    dataset = load_dataset()

    multi_document_cases = [
        case
        for case in dataset["cases"]
        if case["category"] == "multi_document"
    ]

    assert multi_document_cases

    for case in multi_document_cases:
        assert len(case["expected_source_ids"]) >= 2


def test_ambiguous_cases_are_labelled_correctly():
    dataset = load_dataset()

    ambiguous_cases = [
        case
        for case in dataset["cases"]
        if case["category"] == "ambiguous"
    ]

    assert ambiguous_cases

    for case in ambiguous_cases:
        assert case["answerability"] == "ambiguous"
        assert case["expected_source_ids"] == []


def test_adversarial_cases_have_source_grounding():
    dataset = load_dataset()

    adversarial_cases = [
        case
        for case in dataset["cases"]
        if case["category"] == "adversarial"
    ]

    assert adversarial_cases

    for case in adversarial_cases:
        assert len(case["expected_source_ids"]) >= 1
        assert case["answerability"] == "answerable"