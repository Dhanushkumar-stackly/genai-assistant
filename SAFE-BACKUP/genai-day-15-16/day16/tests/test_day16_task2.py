"""
Day 16 - Task 2 tests.
"""

import pytest

from day16.app.output_guard import validate_final_output


def valid_payload():
    return {
        "status": "answered",
        "answer": (
            "Employees receive 20 days of paid leave per year."
        ),
        "sources": [
            {
                "source_id": "leave-policy-001",
                "score": 0.91,
            }
        ],
        "reason_code": "SUFFICIENT_EVIDENCE",
    }


def test_valid_answered_response_is_returned():
    result = validate_final_output(valid_payload())

    assert result["status"] == "answered"
    assert (
        result["sources"][0]["source_id"]
        == "leave-policy-001"
    )


def test_abstained_response_can_have_no_sources():
    payload = {
        "status": "abstained",
        "answer": (
            "The available documents do not support this request."
        ),
        "sources": [],
        "reason_code": "INSUFFICIENT_VALID_EVIDENCE",
    }

    result = validate_final_output(payload)

    assert result["status"] == "abstained"
    assert result["sources"] == []


def test_invalid_status_is_rejected():
    payload = valid_payload()
    payload["status"] = "maybe"

    with pytest.raises(
        ValueError,
        match="INVALID_FINAL_OUTPUT",
    ):
        validate_final_output(payload)


def test_invalid_source_reference_is_rejected():
    payload = valid_payload()

    payload["sources"] = [
        {
            "source_id": "",
            "score": 1.2,
        }
    ]

    with pytest.raises(
        ValueError,
        match="INVALID_FINAL_OUTPUT",
    ):
        validate_final_output(payload)


def test_missing_required_field_is_rejected():
    payload = valid_payload()

    del payload["sources"]

    with pytest.raises(
        ValueError,
        match="INVALID_FINAL_OUTPUT",
    ):
        validate_final_output(payload)


def test_answered_response_requires_source():
    payload = valid_payload()
    payload["sources"] = []

    with pytest.raises(
        ValueError,
        match="INVALID_FINAL_OUTPUT",
    ):
        validate_final_output(payload)


def test_unexpected_fields_are_rejected():
    payload = valid_payload()

    payload["raw_model_text"] = (
        "unvalidated model output"
    )

    with pytest.raises(
        ValueError,
        match="INVALID_FINAL_OUTPUT",
    ):
        validate_final_output(payload)