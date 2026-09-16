from src.day10.task4_choose_best_configuration import (
    choose_configuration,
    evaluate_regressions,
)


def make_result(recall, top1, mrr, questions):
    return {
        "metrics": {
            "retrieval_recall": recall,
            "top1_accuracy": top1,
            "mrr": mrr,
        },
        "details": questions,
    }


def test_candidate_selected_when_improved_without_regression():

    baseline_questions = [
        {
            "question": "Good question",
            "expected_doc_id": "document_001",
            "retrieved_doc_ids": ["document_001"],
        },
        {
            "question": "Weak question",
            "expected_doc_id": "document_002",
            "retrieved_doc_ids": ["document_003"],
        },
    ]

    experiment_questions = [
        {
            "question": "Good question",
            "expected_doc_id": "document_001",
            "retrieved_doc_ids": ["document_001"],
        },
        {
            "question": "Weak question",
            "expected_doc_id": "document_002",
            "retrieved_doc_ids": ["document_002"],
        },
    ]

    baseline = make_result(
        0.5,
        0.5,
        0.5,
        baseline_questions,
    )

    experiment = make_result(
        1.0,
        1.0,
        1.0,
        experiment_questions,
    )

    result = choose_configuration(
        baseline,
        experiment,
    )

    assert result["selected_configuration"] == "experiment"
    assert result["decision"] == "SELECT_CANDIDATE"


def test_candidate_rejected_when_good_question_regresses():

    baseline_questions = [
        {
            "question": "Good question",
            "expected_doc_id": "document_001",
            "retrieved_doc_ids": ["document_001"],
        }
    ]

    experiment_questions = [
        {
            "question": "Good question",
            "expected_doc_id": "document_001",
            "retrieved_doc_ids": ["document_002"],
        }
    ]

    baseline = make_result(
        1.0,
        1.0,
        1.0,
        baseline_questions,
    )

    experiment = make_result(
        0.5,
        0.5,
        0.5,
        experiment_questions,
    )

    result = choose_configuration(
        baseline,
        experiment,
    )

    assert result["selected_configuration"] == "baseline"
    assert result["decision"] == "KEEP_BASELINE"


def test_regression_detection():

    baseline = [
        {
            "question": "Q1",
            "expected_doc_id": "document_001",
            "retrieved_doc_ids": ["document_001"],
        }
    ]

    experiment = [
        {
            "question": "Q1",
            "expected_doc_id": "document_001",
            "retrieved_doc_ids": ["document_002"],
        }
    ]

    result = evaluate_regressions(
        baseline,
        experiment,
    )

    assert result["previously_good_questions"] == 1
    assert result["regressions"] == 1