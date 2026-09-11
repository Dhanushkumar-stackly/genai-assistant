"""
Day 16 - Task 4 runtime demonstration.
"""

from day16.app.fallback import (
    build_fallback,
    response_to_dict,
)


cases = [
    (
        "CASE 1 - No supporting evidence",
        "INSUFFICIENT_VALID_EVIDENCE",
        False,
    ),
    (
        "CASE 2 - Evidence below threshold",
        "EVIDENCE_BELOW_THRESHOLD",
        False,
    ),
    (
        "CASE 3 - Human review required",
        "HUMAN_REVIEW_REQUIRED",
        True,
    ),
    (
        "CASE 4 - Unsupported request requiring escalation",
        "UNSUPPORTED_REQUEST",
        True,
    ),
]


for title, reason_code, escalate in cases:
    response = build_fallback(
        reason_code=reason_code,
        escalate=escalate,
    )

    print("=" * 64)
    print(title)
    print("=" * 64)

    result = response_to_dict(response)

    for key, value in result.items():
        print(f"{key}: {value}")

    print()