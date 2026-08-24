import sqlite3
from pathlib import Path


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_DIR = PROJECT_ROOT / "db"

DB_PATH = DB_DIR / "day09.sqlite3"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the Day 09 database.
    """

    DB_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database() -> None:
    """
    Create all Day 09 tables if they do not already exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # Evaluation Questions
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS evaluation_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_number INTEGER NOT NULL UNIQUE,
                question TEXT NOT NULL,
                expected_document TEXT NOT NULL,
                source_day TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # Retrieval Results
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS retrieval_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_number INTEGER NOT NULL,
                expected_document TEXT NOT NULL,
                retrieved_documents TEXT NOT NULL,
                top1_match INTEGER NOT NULL,
                top3_match INTEGER NOT NULL,
                source_day TEXT NOT NULL,
                FOREIGN KEY (
                    question_number
                )
                REFERENCES evaluation_questions (
                    question_number
                )
            )
            """
        )

        # ----------------------------------------------------
        # Weak Questions
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weak_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_number INTEGER NOT NULL UNIQUE,
                question TEXT NOT NULL,
                expected_document TEXT NOT NULL,
                weakness_reason TEXT NOT NULL,
                severity TEXT NOT NULL,
                evidence TEXT NOT NULL,
                selected_from TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'SELECTED'
            )
            """
        )

        # ----------------------------------------------------
        # Task Runs
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS task_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                status TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                notes TEXT
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    initialize_database()

    print("=" * 60)
    print("DAY 09 DATABASE INITIALIZATION")
    print("=" * 60)

    print()
    print(f"Database: {DB_PATH}")
    print()
    print("Database initialized successfully.")