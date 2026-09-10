"""
Day 15 - Task 5
Safe guardrail decision logging.

Only security-relevant metadata is recorded.
Sensitive request content is intentionally excluded.
"""

from datetime import datetime, timezone
import json
from pathlib import Path


LOG_FILE = (
    Path(__file__).resolve().parent.parent
    / "guardrail_decisions.jsonl"
)


ALLOWED_OUTCOMES = {
    "ALLOWED",
    "BLOCKED",
    "REJECTED",
}


ALLOWED_REASON_CODES = {
    "PROMPT_INJECTION_DETECTED",
    "RETRIEVED_INSTRUCTION_DETECTED",
    "INVALID_INPUT",
    "INPUT_TOO_LONG",
    "UNSUPPORTED_CONTENT_TYPE",
    "MALFORMED_PAYLOAD",
    "RESTRICTED_REQUEST",
    "CONFLICTING_INSTRUCTIONS",
}


def log_guardrail_decision(
    control_triggered: str,
    outcome: str,
    reason_code: str,
) -> dict:
    """
    Record a safe guardrail decision.

    Sensitive request content is never written to the log.
    """

    if not control_triggered.strip():
        raise ValueError(
            "control_triggered must not be empty."
        )

    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError(
            f"Unsupported outcome: {outcome}"
        )

    if reason_code not in ALLOWED_REASON_CODES:
        raise ValueError(
            f"Unsupported reason code: {reason_code}"
        )

    decision = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "control_triggered": control_triggered,
        "outcome": outcome,
        "reason_code": reason_code,
    }

    with LOG_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(decision)
            + "\n"
        )

    return decision