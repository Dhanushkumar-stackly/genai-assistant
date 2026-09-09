"""
Day 16 - Task 1

Evidence requirements and abstention routing for RAG responses.
"""

from dataclasses import dataclass
from typing import Any


MIN_VALID_SOURCES = 1
MIN_EVIDENCE_SCORE = 0.60


@dataclass(frozen=True)
class EvidenceDecision:
    """
    Result of the evidence validation step.
    """

    status: str
    reason_code: str
    valid_source_count: int
    best_score: float


def _is_valid_source(source: Any) -> bool:
    """
    Check whether a retrieved source contains the minimum
    information required for evidence validation.
    """

    if not isinstance(source, dict):
        return False

    source_id = source.get("source_id")
    content = source.get("content")
    score = source.get("score")

    if not isinstance(source_id, str) or not source_id.strip():
        return False

    if not isinstance(content, str) or not content.strip():
        return False

    if not isinstance(score, (int, float)):
        return False

    if isinstance(score, bool):
        return False

    if not 0.0 <= float(score) <= 1.0:
        return False

    return True


def check_evidence(
    sources: list[dict[str, Any]],
    min_sources: int = MIN_VALID_SOURCES,
    min_score: float = MIN_EVIDENCE_SCORE,
) -> EvidenceDecision:
    """
    Validate retrieved evidence before allowing an answered status.

    The request is allowed to continue only when:
    1. The minimum number of valid sources exists.
    2. At least one valid source reaches the minimum evidence score.

    Weak or invalid evidence is routed to abstention.
    """

    if min_sources < 1:
        raise ValueError("min_sources must be at least 1")

    if not 0.0 <= min_score <= 1.0:
        raise ValueError("min_score must be between 0.0 and 1.0")

    valid_sources = [
        source
        for source in sources
        if _is_valid_source(source)
    ]

    if len(valid_sources) < min_sources:
        return EvidenceDecision(
            status="abstained",
            reason_code="INSUFFICIENT_VALID_EVIDENCE",
            valid_source_count=len(valid_sources),
            best_score=0.0,
        )

    best_score = max(
        float(source["score"])
        for source in valid_sources
    )

    if best_score < min_score:
        return EvidenceDecision(
            status="abstained",
            reason_code="EVIDENCE_BELOW_THRESHOLD",
            valid_source_count=len(valid_sources),
            best_score=best_score,
        )

    return EvidenceDecision(
        status="answered",
        reason_code="SUFFICIENT_EVIDENCE",
        valid_source_count=len(valid_sources),
        best_score=best_score,
    )