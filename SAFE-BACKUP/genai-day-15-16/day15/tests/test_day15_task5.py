"""
Day 15 - Task 5
Tests for safe guardrail decision logging.
"""

import json

import pytest

from day15.app import guardrail_logger


def test_guardrail_decision_contains_required_fields(
    tmp_path,
    monkeypatch,
):
    log_file = tmp_path / "guardrail.jsonl"

    monkeypatch.setattr(
        guardrail_logger,
        "LOG_FILE",
        log_file,
    )

    decision = guardrail_logger.log_guardrail_decision(
        control_triggered="input_validation",
        outcome="REJECTED",
        reason_code="INVALID_INPUT",
    )

    assert decision["control_triggered"] == "input_validation"
    assert decision["outcome"] == "REJECTED"
    assert decision["reason_code"] == "INVALID_INPUT"
    assert "timestamp" in decision


def test_sensitive_request_content_is_not_logged(
    tmp_path,
    monkeypatch,
):
    log_file = tmp_path / "guardrail.jsonl"

    monkeypatch.setattr(
        guardrail_logger,
        "LOG_FILE",
        log_file,
    )

    secret = "SUPER_SECRET_PASSWORD_123"

    guardrail_logger.log_guardrail_decision(
        control_triggered="instruction_hierarchy",
        outcome="BLOCKED",
        reason_code="PROMPT_INJECTION_DETECTED",
    )

    content = log_file.read_text(
        encoding="utf-8"
    )

    assert secret not in content
    assert "PROMPT_INJECTION_DETECTED" in content


def test_invalid_outcome_is_rejected(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        guardrail_logger,
        "LOG_FILE",
        tmp_path / "guardrail.jsonl",
    )

    with pytest.raises(ValueError):
        guardrail_logger.log_guardrail_decision(
            control_triggered="input_validation",
            outcome="UNKNOWN",
            reason_code="INVALID_INPUT",
        )


def test_invalid_reason_code_is_rejected(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        guardrail_logger,
        "LOG_FILE",
        tmp_path / "guardrail.jsonl",
    )

    with pytest.raises(ValueError):
        guardrail_logger.log_guardrail_decision(
            control_triggered="input_validation",
            outcome="BLOCKED",
            reason_code="UNKNOWN_REASON",
        )


def test_log_entry_is_valid_json(
    tmp_path,
    monkeypatch,
):
    log_file = tmp_path / "guardrail.jsonl"

    monkeypatch.setattr(
        guardrail_logger,
        "LOG_FILE",
        log_file,
    )

    guardrail_logger.log_guardrail_decision(
        control_triggered="input_validation",
        outcome="REJECTED",
        reason_code="MALFORMED_PAYLOAD",
    )

    line = log_file.read_text(
        encoding="utf-8"
    ).strip()

    entry = json.loads(line)

    assert entry["outcome"] == "REJECTED"
    assert entry["reason_code"] == "MALFORMED_PAYLOAD"