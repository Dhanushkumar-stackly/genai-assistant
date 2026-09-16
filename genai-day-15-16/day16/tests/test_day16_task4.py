"""
Day 16 - Task 4 tests.
"""

import pytest

from day16.app.fallback import (
    APPROVED_SUPPORT_PATH,
    SAFE_ABSTENTION_MESSAGE,
    SAFE_ESCALATION_MESSAGE,
    build_abstention_response,
    build_escalation_response,
    build_fallback,
    response_to_dict,
)


def test_insufficient_evidence_returns_abstention():
    result = build_abstention_response(
        "INSUFFICIENT_VALID_EVIDENCE"
    )

    assert result.status == "abstained"
    assert result.reason_code == "INSUFFICIENT_VALID_EVIDENCE"
    assert result.escalation_available is False
    assert result.escalation_path is None


def test_abstention_message_is_consistent():
    result = build_abstention_response(
        "EVIDENCE_BELOW_THRESHOLD"
    )

    assert result.message == SAFE_ABSTENTION_MESSAGE


def test_escalation_returns_human_support_path():
    result = build_escalation_response(
        "HUMAN_REVIEW_REQUIRED"
    )

    assert result.status == "escalated"
    assert result.escalation_available is True
    assert result.escalation_path == APPROVED_SUPPORT_PATH


def test_escalation_message_is_consistent():
    result = build_escalation_response(
        "UNSUPPORTED_REQUEST"
    )

    assert result.message == SAFE_ESCALATION_MESSAGE


def test_build_fallback_defaults_to_abstention():
    result = build_fallback(
        "EVIDENCE_BELOW_THRESHOLD"
    )

    assert result.status == "abstained"
    assert result.escalation_available is False


def test_build_fallback_can_escalate():
    result = build_fallback(
        "HUMAN_REVIEW_REQUIRED",
        escalate=True,
    )

    assert result.status == "escalated"
    assert result.escalation_available is True


def test_fallback_contains_no_generated_answer():
    result = response_to_dict(
        build_abstention_response(
            "INSUFFICIENT_VALID_EVIDENCE"
        )
    )

    assert "answer" not in result
    assert "model_output" not in result
    assert "generated_answer" not in result


def test_response_to_dict_returns_expected_fields():
    result = response_to_dict(
        build_abstention_response(
            "INSUFFICIENT_VALID_EVIDENCE"
        )
    )

    assert set(result.keys()) == {
        "status",
        "message",
        "reason_code",
        "escalation_available",
        "escalation_path",
    }


@pytest.mark.parametrize(
    "reason_code",
    [
        "INSUFFICIENT_VALID_EVIDENCE",
        "EVIDENCE_BELOW_THRESHOLD",
        "INVALID_FINAL_OUTPUT",
        "RESTRICTED_OUTPUT",
    ],
)
def test_common_guardrail_reasons_can_abstain(reason_code):
    result = build_fallback(reason_code)

    assert result.status == "abstained"
    assert result.reason_code == reason_code


def test_empty_reason_code_is_rejected():
    with pytest.raises(ValueError):
        build_fallback("")


def test_whitespace_reason_code_is_rejected():
    with pytest.raises(ValueError):
        build_fallback("   ")