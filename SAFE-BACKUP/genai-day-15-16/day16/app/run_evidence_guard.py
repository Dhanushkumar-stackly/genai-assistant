"""
Day 16 - Task 1 runtime demonstration.
"""

from day16.app.evidence_guard import check_evidence


def print_result(title: str, sources: list[dict]) -> None:
    result = check_evidence(sources)

    print("=" * 60)
    print(title)
    print("=" * 60)
    print(f"Valid sources : {result.valid_source_count}")
    print(f"Best score    : {result.best_score:.2f}")
    print(f"Status        : {result.status}")
    print(f"Reason        : {result.reason_code}")
    print()


strong_evidence = [
    {
        "source_id": "leave-policy-001",
        "content": "Employees receive 20 days of paid leave per year.",
        "score": 0.91,
    },
    {
        "source_id": "hr-handbook-002",
        "content": "Leave requests must be approved by the manager.",
        "score": 0.82,
    },
]


weak_evidence = [
    {
        "source_id": "random-001",
        "content": "This document discusses office parking.",
        "score": 0.24,
    },
]


no_evidence = []


print_result(
    "CASE 1 - Strong evidence",
    strong_evidence,
)

print_result(
    "CASE 2 - Weak evidence",
    weak_evidence,
)

print_result(
    "CASE 3 - No evidence",
    no_evidence,
)