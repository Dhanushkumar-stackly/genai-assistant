"""
Day 16 - Task 1
Tests for evidence requirements.
"""

import pytest

from day16.app.evidence_guard import (
    MIN_EVIDENCE_SCORE,
    check_evidence,
)


def test_strong_evidence_allows_answer():
    sources = [
        {
            "source_id": "source-001",
            "content": "Employees receive 20 days of paid leave.",
            "score": 0.91,
        }
    ]

    result = check_evidence(sources)

    assert result.status == "answered"
    assert result.reason_code == "SUFFICIENT_EVIDENCE"
    assert result.valid_source_count == 1
    assert result.best_score == 0.91


def test_weak_evidence_abstains():
    sources = [
        {
            "source_id": "source-001",
            "content": "This document is unrelated to the question.",
            "score": 0.30,
        }
    ]

    result = check_evidence(sources)

    assert result.status == "abstained"
    assert result.reason_code == "EVIDENCE_BELOW_THRESHOLD"


def test_no_evidence_abstains():
    result = check_evidence([])

    assert result.status == "abstained"
    assert result.reason_code == "INSUFFICIENT_VALID_EVIDENCE"
    assert result.valid_source_count == 0


def test_invalid_source_is_not_counted():
    sources = [
        {
            "source_id": "",
            "content": "Invalid source",
            "score": 0.95,
        }
    ]

    result = check_evidence(sources)

    assert result.status == "abstained"
    assert result.valid_source_count == 0


def test_empty_content_is_invalid():
    sources = [
        {
            "source_id": "source-001",
            "content": "",
            "score": 0.95,
        }
    ]

    result = check_evidence(sources)

    assert result.status == "abstained"


def test_score_above_threshold_allows_answer():
    sources = [
        {
            "source_id": "source-001",
            "content": "Supported evidence.",
            "score": MIN_EVIDENCE_SCORE,
        }
    ]

    result = check_evidence(sources)

    assert result.status == "answered"


def test_multiple_sources_use_best_score():
    sources = [
        {
            "source_id": "source-001",
            "content": "Weak evidence.",
            "score": 0.20,
        },
        {
            "source_id": "source-002",
            "content": "Strong evidence.",
            "score": 0.88,
        },
    ]

    result = check_evidence(sources)

    assert result.status == "answered"
    assert result.best_score == 0.88


@pytest.mark.parametrize(
    "source",
    [
        None,
        {},
        {"source_id": "source-001"},
        {"content": "Evidence", "score": 0.8},
        {"source_id": "source-001", "content": "Evidence"},
        {
            "source_id": "source-001",
            "content": "Evidence",
            "score": 1.5,
        },
    ],
)
def test_malformed_sources_are_rejected(source):
    result = check_evidence([source])

    assert result.status == "abstained"