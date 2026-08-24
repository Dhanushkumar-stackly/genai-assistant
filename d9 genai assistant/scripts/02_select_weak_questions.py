import json
import sqlite3
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "db" / "day09.sqlite3"

DAY6_QUESTIONS_FILE = (
    PROJECT_ROOT.parent
    / "d5-6 genai assistant"
    / "data"
    / "retrieval_questions.json"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# LOAD DAY 6 QUESTIONS
# ============================================================

def load_day6_questions():
    if not DAY6_QUESTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Day 6 questions file not found:\n"
            f"{DAY6_QUESTIONS_FILE}"
        )

    with DAY6_QUESTIONS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ============================================================
# INSERT QUESTIONS
# ============================================================

def insert_questions(
    connection,
    questions
):
    cursor = connection.cursor()

    for number, item in enumerate(
        questions,
        start=1
    ):
        question = item["question"]
        expected_document = item["expected_doc_id"]

        cursor.execute(
            """
            INSERT OR REPLACE INTO evaluation_questions (
                question_number,
                question,
                expected_document,
                source_day
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                number,
                question,
                expected_document,
                "day06"
            )
        )

    connection.commit()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("DAY 09 - TASK 2")
    print("LOAD DAY 06 EVALUATION QUESTIONS")
    print("=" * 70)

    print()
    print(
        f"Database      : {DB_PATH}"
    )

    print(
        f"Day 6 source  : {DAY6_QUESTIONS_FILE}"
    )

    # --------------------------------------------------------
    # Load Day 6 questions
    # --------------------------------------------------------

    questions = load_day6_questions()

    print()
    print(
        f"Questions loaded: {len(questions)}"
    )

    # --------------------------------------------------------
    # Insert into Day 09 database
    # --------------------------------------------------------

    connection = get_connection()

    try:
        insert_questions(
            connection,
            questions
        )

        cursor = connection.cursor()

        count = cursor.execute(
            """
            SELECT COUNT(*)
            FROM evaluation_questions
            WHERE source_day = 'day06'
            """
        ).fetchone()[0]

    finally:
        connection.close()

    print(
        f"Questions stored: {count}"
    )

    print()
    print("=" * 70)
    print("DAY 6 QUESTIONS LOADED INTO DAY 09 DATABASE")
    print("=" * 70)


if __name__ == "__main__":
    main()