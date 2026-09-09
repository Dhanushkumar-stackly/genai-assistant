"""
Day 15 - Task 3
Tests for input validation.
"""

import pytest
from pydantic import ValidationError

from day15.app.validation import (
    MAX_QUESTION_LENGTH,
    validate_query,
)


def test_valid_question_is_accepted():
    payload = {
        "question": "What is the leave policy?"
    }

    result = validate_query(payload)

    assert result.question == "What is the leave policy?"


def test_empty_question_is_rejected():
    payload = {
        "question": ""
    }

    with pytest.raises(ValidationError):
        validate_query(payload)


def test_missing_question_is_rejected():
    payload = {}

    with pytest.raises(ValidationError):
        validate_query(payload)


def test_wrong_question_type_is_rejected():
    payload = {
        "question": 12345
    }

    with pytest.raises(ValidationError):
        validate_query(payload)


def test_excessive_question_is_rejected():
    payload = {
        "question": "A" * (MAX_QUESTION_LENGTH + 1)
    }

    with pytest.raises(ValidationError):
        validate_query(payload)


def test_extra_fields_are_rejected():
    payload = {
        "question": "What is the leave policy?",
        "ignore_security": True,
    }

    with pytest.raises(ValidationError):
        validate_query(payload)


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        "not a json object",
        12345,
    ],
)
def test_malformed_payloads_are_rejected(payload):
    with pytest.raises(ValidationError):
        validate_query(payload)