import json
from pathlib import Path

from day09.database import (
    create_tables,
    save_retrieval_evidence,
    save_weak_question,
    get_connection
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "outputs"

OUTPUT_FILE = (
    OUTPUT_DIR / "task2_weak_questions.json"
)


# ============================================================
# INPUT HELPERS
# ============================================================

def ask_text(
    label: str,
    allow_empty: bool = False
) -> str:

    while True:

        value = input(
            label
        ).strip()

        if value or allow_empty:

            return value

        print(
            "Value cannot be empty."
        )


def ask_integer(
    label: str
) -> int:

    while True:

        value = input(
            label
        ).strip()

        try:

            return int(value)

        except ValueError:

            print(
                "Enter a valid integer."
            )


def ask_yes_no(
    label: str
) -> bool:

    while True:

        value = input(
            label
        ).strip().lower()

        if value in (
            "y",
            "yes"
        ):

            return True

        if value in (
            "n",
            "no"
        ):

            return False

        print(
            "Enter y or n."
        )


# ============================================================
# DAY 6 QUALITY
# ============================================================

def get_day6_quality(
    source_found: bool,
    expected_rank: int | None
) -> str:

    if not source_found:

        return "missing_source"

    if expected_rank == 1:

        return "correct_top_rank"

    if expected_rank is not None:

        return "wrong_ranking"

    return "unknown"


# ============================================================
# DAY 8 QUALITY
# ============================================================

def get_day8_quality(
    status: str,
    grounded: bool,
    citation_valid: bool
) -> str:

    status = status.lower()

    if (
        status == "insufficient_evidence"
        and grounded
    ):

        return "possible_unnecessary_abstention"

    if (
        status == "answered"
        and not grounded
    ):

        return "ungrounded_answer"

    if (
        status == "answered"
        and not citation_valid
    ):

        return "invalid_citation"

    if status == "insufficient_evidence":

        return "correct_abstention"

    if (
        status == "answered"
        and grounded
        and citation_valid
    ):

        return "good"

    return "unknown"


# ============================================================
# WEAKNESS SCORE
# ============================================================

def calculate_weakness_score(
    day6_quality: str,
    day6_rank: int | None,
    day8_quality: str
) -> float:

    score = 0.0

    # --------------------------------------------------------
    # Day 6 retrieval failure
    # --------------------------------------------------------

    if day6_quality == "missing_source":

        score += 5.0

    elif day6_quality == "wrong_ranking":

        if day6_rank == 2:

            score += 2.0

        elif day6_rank == 3:

            score += 3.0

        elif day6_rank is not None:

            score += 4.0

    # --------------------------------------------------------
    # Day 8 failures
    # --------------------------------------------------------

    if day8_quality == (
        "possible_unnecessary_abstention"
    ):

        score += 4.0

    elif day8_quality == (
        "ungrounded_answer"
    ):

        score += 5.0

    elif day8_quality == (
        "invalid_citation"
    ):

        score += 3.0

    # --------------------------------------------------------
    # Combined retrieval + generation failure
    # --------------------------------------------------------

    if (
        day6_quality == "missing_source"
        and
        day8_quality in (
            "ungrounded_answer",
            "possible_unnecessary_abstention"
        )
    ):

        score += 2.0

    return score


# ============================================================
# FAILURE TYPE
# ============================================================

def get_failure_type(
    day6_quality: str,
    day8_quality: str
) -> str:

    failures = []

    if day6_quality == "missing_source":

        failures.append(
            "missing_source"
        )

    elif day6_quality == "wrong_ranking":

        failures.append(
            "wrong_ranking"
        )

    if day8_quality == (
        "possible_unnecessary_abstention"
    ):

        failures.append(
            "unnecessary_abstention"
        )

    elif day8_quality == "ungrounded_answer":

        failures.append(
            "ungrounded_answer"
        )

    elif day8_quality == "invalid_citation":

        failures.append(
            "invalid_citation"
        )

    if not failures:

        return "weak_retrieval"

    return " + ".join(
        failures
    )


# ============================================================
# SELECTION REASON
# ============================================================

def get_selection_reason(
    day6_quality: str,
    day6_rank: int | None,
    day8_quality: str
) -> str:

    reasons = []

    if day6_quality == "missing_source":

        reasons.append(
            "Expected source was not retrieved."
        )

    elif day6_quality == "wrong_ranking":

        reasons.append(
            "Expected source was retrieved "
            f"at rank {day6_rank}, not rank 1."
        )

    if day8_quality == (
        "possible_unnecessary_abstention"
    ):

        reasons.append(
            "Evidence was available but "
            "the system returned insufficient_evidence."
        )

    elif day8_quality == "ungrounded_answer":

        reasons.append(
            "Answer was produced without "
            "sufficient grounding."
        )

    elif day8_quality == "invalid_citation":

        reasons.append(
            "Answer citation did not satisfy "
            "the expected citation requirement."
        )

    return " ".join(reasons)


# ============================================================
# COLLECT ONE QUESTION
# ============================================================

def collect_question(
    question_number: int
) -> dict:

    print()
    print("-" * 60)
    print(
        f"QUESTION {question_number}"
    )
    print("-" * 60)

    question_id = ask_text(
        "Question ID: "
    )

    question = ask_text(
        "Question: "
    )

    expected_source = ask_text(
        "Expected source/document: "
    )

    # ========================================================
    # DAY 6
    # ========================================================

    print()
    print("DAY 6 RETRIEVAL EVIDENCE")

    day6_top1_source = ask_text(
        "Day 6 top-1 retrieved source "
        "(enter 'none' if empty): "
    )

    if day6_top1_source.lower() == "none":

        day6_top1_source = None

    day6_source_found = ask_yes_no(
        "Was expected source retrieved? (y/n): "
    )

    if day6_source_found:

        day6_expected_rank = ask_integer(
            "Expected source rank: "
        )

    else:

        day6_expected_rank = None

    day6_quality = get_day6_quality(
        day6_source_found,
        day6_expected_rank
    )

    # ========================================================
    # DAY 8
    # ========================================================

    print()
    print("DAY 8 RESULT")

    day8_status = ask_text(
        "Day 8 status "
        "(answered/insufficient_evidence): "
    ).lower()

    day8_grounded = ask_yes_no(
        "Was the answer grounded? (y/n): "
    )

    day8_citation_valid = ask_yes_no(
        "Was citation valid? (y/n): "
    )

    day8_quality = get_day8_quality(
        day8_status,
        day8_grounded,
        day8_citation_valid
    )

    # ========================================================
    # NOTES
    # ========================================================

    notes = ask_text(
        "Notes "
        "(optional, press Enter to skip): ",
        allow_empty=True
    )

    return {
        "question_id": question_id,
        "question": question,
        "expected_source": expected_source,

        "day6_top1_source": day6_top1_source,
        "day6_expected_rank": day6_expected_rank,
        "day6_source_found": day6_source_found,
        "day6_result_quality": day6_quality,

        "day8_status": day8_status,
        "day8_grounded": day8_grounded,
        "day8_citation_valid": day8_citation_valid,
        "day8_result_quality": day8_quality,

        "notes": notes
    }


# ============================================================
# LOAD ALL EVIDENCE FROM DAY 09 DB
# ============================================================

def load_evidence():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            question_id,
            question,
            expected_source,
            day6_result_quality,
            day6_expected_rank,
            day8_result_quality
        FROM retrieval_evidence
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# BUILD WEAK QUESTION
# ============================================================

def build_weak_question(
    row
) -> dict:

    (
        question_id,
        question,
        expected_source,
        day6_quality,
        day6_rank,
        day8_quality
    ) = row

    score = calculate_weakness_score(
        day6_quality,
        day6_rank,
        day8_quality
    )

    failure_type = get_failure_type(
        day6_quality,
        day8_quality
    )

    reason = get_selection_reason(
        day6_quality,
        day6_rank,
        day8_quality
    )

    return {
        "question_id": question_id,
        "question": question,
        "expected_source": expected_source,
        "failure_type": failure_type,
        "weakness_score": score,
        "selection_reason": reason
    }


# ============================================================
# SAVE FINAL OUTPUT
# ============================================================

def save_output(
    selected: list
) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    payload = {
        "task": "DAY 09 - TASK 2",
        "description": (
            "Five weakest baseline questions"
        ),
        "count": len(selected),
        "selected_questions": selected
    }

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            payload,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("DAY 09 - TASK 2")
    print("SELECT FIVE WEAKEST QUESTIONS")
    print("=" * 60)

    # --------------------------------------------------------
    # Create Day 09 tables
    # --------------------------------------------------------

    create_tables()

    # --------------------------------------------------------
    # Collect Day 6 + Day 8 evidence
    # --------------------------------------------------------

    print()
    print(
        "Enter evidence from your existing "
        "Day 6 and Day 8 evaluation results."
    )

    print()
    print(
        "IMPORTANT:"
    )

    print(
        "Only evidence is being recorded."
    )

    print(
        "No Day 6 or Day 8 database is accessed."
    )

    print()

    number_of_questions = ask_integer(
        "How many baseline questions? "
    )

    for index in range(
        1,
        number_of_questions + 1
    ):

        evidence = collect_question(
            index
        )

        save_retrieval_evidence(
            evidence
        )

    # --------------------------------------------------------
    # Read evidence from Day 09 DB
    # --------------------------------------------------------

    rows = load_evidence()

    # --------------------------------------------------------
    # Calculate weakness
    # --------------------------------------------------------

    candidates = []

    for row in rows:

        question = build_weak_question(
            row
        )

        candidates.append(
            question
        )

    # --------------------------------------------------------
    # Sort weakest first
    # --------------------------------------------------------

    candidates.sort(
        key=lambda item: item[
            "weakness_score"
        ],
        reverse=True
    )

    # --------------------------------------------------------
    # Select top 5
    # --------------------------------------------------------

    selected = candidates[:5]

    # --------------------------------------------------------
    # Clear previous Task 2 selections
    # --------------------------------------------------------

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM weak_questions"
    )

    connection.commit()

    connection.close()

    # --------------------------------------------------------
    # Save selected questions
    # --------------------------------------------------------

    for question in selected:

        save_weak_question(
            question
        )

    # --------------------------------------------------------
    # Save JSON
    # --------------------------------------------------------

    save_output(
        selected
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("FIVE WEAKEST QUESTIONS")
    print("=" * 60)

    for index, question in enumerate(
        selected,
        start=1
    ):

        print()
        print(
            f"{index}. "
            f"{question['question_id']}"
        )

        print(
            f"Question: "
            f"{question['question']}"
        )

        print(
            f"Failure: "
            f"{question['failure_type']}"
        )

        print(
            f"Weakness score: "
            f"{question['weakness_score']}"
        )

        print(
            f"Reason: "
            f"{question['selection_reason']}"
        )

    print()
    print("=" * 60)

    print(
        "Saved in:"
    )

    print(
        "db/day09.sqlite3"
    )

    print(
        "outputs/task2_weak_questions.json"
    )

    print()
    print(
        "DAY 09 TASK 2 COMPLETED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()