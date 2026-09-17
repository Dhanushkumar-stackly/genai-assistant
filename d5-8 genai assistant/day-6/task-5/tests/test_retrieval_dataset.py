import json
from pathlib import Path


DATASET = Path(__file__).resolve().parents[1] / "data" / "retrieval_questions.json"


def load_questions():
    with DATASET.open(encoding="utf-8") as file:
        return json.load(file)


def test_retrieval_dataset_has_at_least_ten_questions():
    questions = load_questions()
    assert len(questions) >= 10


def test_each_question_has_expected_source_document():
    questions = load_questions()
    assert all(item.get("question") for item in questions)
    assert all(item.get("expected_doc_id") for item in questions)


def test_expected_document_ids_are_stable_strings():
    questions = load_questions()
    assert all(isinstance(item["expected_doc_id"], str) for item in questions)
