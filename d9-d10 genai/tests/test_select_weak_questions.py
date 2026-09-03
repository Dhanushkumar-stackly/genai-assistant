from src.select_weak_questions import (
    calculate_failure_score,
    select_weak_questions,
)


def test_missing_source_is_weak():

    day6 = {
        "question": "Test question",
        "expected_doc_id": "document_001",
        "retrieved_doc_ids": [
            "document_002",
            "document_003",
            "document_004",
        ],
        "distances": [
            0.5,
            0.6,
            0.7,
        ],
    }

    day8 = {
        "question": "Test question",
        "status": "answered",
        "citations": [],
    }

    score, reasons = (
        calculate_failure_score(
            day6,
            day8
        )
    )

    assert score >= 5
    assert (
        "missing_expected_source"
        in reasons
    )


def test_rank_three_is_weaker_than_rank_two():

    day6_rank_three = {
        "question": "Test",
        "expected_doc_id": "document_001",
        "retrieved_doc_ids": [
            "document_002",
            "document_003",
            "document_001",
        ],
        "distances": [
            0.4,
            0.5,
            0.6,
        ],
    }

    day8 = {
        "question": "Test",
        "status": "answered",
        "citations": ["document_001"],
    }

    score, reasons = (
        calculate_failure_score(
            day6_rank_three,
            day8
        )
    )

    assert score >= 3
    assert "low_ranking" in reasons


def test_selects_only_five():

    day6 = []

    day8 = []

    for i in range(10):

        day6.append(
            {
                "question":
                    f"Question {i}",

                "expected_doc_id":
                    f"document_{i}",

                "retrieved_doc_ids": [],

                "distances": [],
            }
        )

        day8.append(
            {
                "question":
                    f"Question {i}",

                "status":
                    "insufficient_evidence",

                "citations": [],
            }
        )

    result = select_weak_questions(
        day6,
        day8
    )

    assert len(result) == 5