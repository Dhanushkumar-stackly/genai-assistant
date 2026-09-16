"""
Day 15 - Task 4
Baseline adversarial behavior runner.

This simulates recording the application's behavior before
new security controls are applied.
"""

from pathlib import Path
import json

from day15.tests.test_day15_task1 import ADVERSARIAL_CASES


OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "baseline_scorecard.json"
)


def classify_baseline_case(case):
    """
    Record a baseline classification for each adversarial case.

    The current project does not yet have the complete production
    RAG endpoint wired into this runner, so cases are marked
    as NOT_RUN rather than inventing application behavior.
    """

    return {
        "id": case["id"],
        "category": case["category"],
        "classification": "NOT_RUN",
        "observation": (
            "Run this case against the existing RAG application "
            "before applying new security controls."
        ),
    }


def create_baseline_scorecard():
    scorecard = [
        classify_baseline_case(case)
        for case in ADVERSARIAL_CASES
    ]

    OUTPUT_FILE.write_text(
        json.dumps(scorecard, indent=2),
        encoding="utf-8",
    )

    return scorecard


def print_scorecard(scorecard):
    print("\nDAY 15 - BASELINE ADVERSARIAL SCORECARD")
    print("=" * 70)

    for result in scorecard:
        print(
            f"{result['id']} | "
            f"{result['category']} | "
            f"{result['classification']}"
        )

    print("=" * 70)
    print(f"Total cases: {len(scorecard)}")
    print(f"Scorecard: {OUTPUT_FILE}")


if __name__ == "__main__":
    results = create_baseline_scorecard()
    print_scorecard(results)