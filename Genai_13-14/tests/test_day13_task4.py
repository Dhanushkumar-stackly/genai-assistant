from pathlib import Path

from eval.evaluation_runner import (
    evaluate_case,
    load_golden_dataset,
    run_evaluation,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "eval" / "golden_dataset.json"


def test_golden_dataset_can_be_loaded():
    dataset = load_golden_dataset()

    assert "cases" in dataset
    assert len(dataset["cases"]) == 25


def test_evaluate_answerable_case_with_expected_source():
    case = {
        "case_id": "D13-001",
        "question": "What is the leave policy?",
        "answerability": "answerable",
        "expected_source_ids": [
            "doc-leave-policy"
        ],
    }

    response = {
        "answer": "The leave policy allows employees to apply for leave.",
        "sources": [
            {
                "document_id": "doc-leave-policy"
            }
        ],
    }

    result = evaluate_case(case, response)

    assert result["passed"] is True


def test_evaluate_answerable_case_with_missing_source():
    case = {
        "case_id": "D13-001",
        "question": "What is the leave policy?",
        "answerability": "answerable",
        "expected_source_ids": [
            "doc-leave-policy"
        ],
    }

    response = {
        "answer": "Some answer",
        "sources": [],
    }

    result = evaluate_case(case, response)

    assert result["passed"] is False


def test_unanswerable_case_without_sources_passes():
    case = {
        "case_id": "D13-006",
        "question": "What is the policy for an unknown topic?",
        "answerability": "unanswerable",
        "expected_source_ids": [],
    }

    response = {
        "answer": "I do not have enough information.",
        "sources": [],
    }

    result = evaluate_case(case, response)

    assert result["passed"] is True


def test_unanswerable_case_with_sources_fails():
    case = {
        "case_id": "D13-006",
        "question": "What is the policy for an unknown topic?",
        "answerability": "unanswerable",
        "expected_source_ids": [],
    }

    response = {
        "answer": "Some unsupported answer",
        "sources": [
            {
                "document_id": "doc-security-policy"
            }
        ],
    }

    result = evaluate_case(case, response)

    assert result["passed"] is False


def test_evaluation_runner_processes_all_cases():
    def responder(question: str) -> dict:
        return {
            "answer": "Demo answer",
            "sources": [],
        }

    report = run_evaluation(
        responder=responder,
        dataset_path=DATASET_PATH,
    )

    assert report["total_cases"] == 25
    assert len(report["results"]) == 25


def test_evaluation_runner_result_structure():
    def responder(question: str) -> dict:
        return {
            "answer": "Demo answer",
            "sources": [],
        }

    report = run_evaluation(
        responder=responder,
        dataset_path=DATASET_PATH,
    )

    assert "total_cases" in report
    assert "passed" in report
    assert "failed" in report
    assert "results" in report