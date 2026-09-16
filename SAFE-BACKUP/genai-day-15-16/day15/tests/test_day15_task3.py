"""
Day 15 - Task 3
Tests for strict input validation.
"""

import pytest
from pydantic import ValidationError

from day15.app.validation import (
    MAX_QUESTION_LENGTH,
    validate_query,
)


def test_valid_question_is_accepted():
    result = validate_query(
        {"question": "What is the leave policy?"}
    )

    assert result.question == "What is the leave policy?"


def test_empty_question_is_rejected():
    with pytest.raises(ValidationError):
        validate_query({"question": ""})


def test_whitespace_question_is_rejected():
    with pytest.raises(ValidationError):
        validate_query({"question": "   "})


def test_missing_question_is_rejected():
    with pytest.raises(ValidationError):
        validate_query({})


def test_wrong_type_is_rejected():
    with pytest.raises(ValidationError):
        validate_query({"question": 12345})


def test_excessive_input_is_rejected():
    with pytest.raises(ValidationError):
        validate_query(
            {
                "question": "A"
                * (MAX_QUESTION_LENGTH + 1)
            }
        )


def test_extra_fields_are_rejected():
    with pytest.raises(ValidationError):
        validate_query(
            {
                "question": "What is the policy?",
                "ignore_security": True,
            }
        )


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        "invalid payload",
        12345,
    ],
)
def test_malformed_payload_is_rejected(payload):
    with pytest.raises(ValidationError):
        validate_query(payload)