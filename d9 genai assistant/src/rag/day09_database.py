import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_DIR = PROJECT_ROOT / "db"

DB_PATH = DB_DIR / "day09.sqlite3"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the Day 09 database.
    """

    DB_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database() -> None:
    """
    Create the Day 09 tables if they do not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluation_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id TEXT UNIQUE NOT NULL,
            question TEXT NOT NULL,
            expected_source TEXT NOT NULL,
            weakness_reason TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# INSERT QUESTION
# ============================================================

def insert_question(
    question_id: str,
    question: str,
    expected_source: str,
    weakness_reason: str
) -> None:
    """
    Insert one evaluation question into Day 09 DB.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO evaluation_questions
        (
            question_id,
            question,
            expected_source,
            weakness_reason
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            question_id,
            question,
            expected_source,
            weakness_reason
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# INSERT FIVE WEAK QUESTIONS
# ============================================================

def seed_weak_questions() -> None:
    """
    Insert the five Day 09 weak evaluation questions.
    """

    questions = [
        (
            "Q001",
            "REPLACE_WITH_QUESTION_1",
            "document_001",
            "missing_source"
        ),
        (
            "Q002",
            "REPLACE_WITH_QUESTION_2",
            "document_002",
            "wrong_ranking"
        ),
        (
            "Q003",
            "REPLACE_WITH_QUESTION_3",
            "document_003",
            "incomplete_context"
        ),
        (
            "Q004",
            "REPLACE_WITH_QUESTION_4",
            "document_004",
            "unnecessary_abstention"
        ),
        (
            "Q005",
            "REPLACE_WITH_QUESTION_5",
            "document_005",
            "irrelevant_retrieval"
        )
    ]

    for question in questions:
        insert_question(
            question_id=question[0],
            question=question[1],
            expected_source=question[2],
            weakness_reason=question[3]
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    initialize_database()

    seed_weak_questions()

    print("=" * 60)
    print("DAY 09 DATABASE INITIALIZED")
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print("Table: evaluation_questions")
    print("Questions inserted: 5")
    print("=" * 60)