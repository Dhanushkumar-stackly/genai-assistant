import sqlite3
from pathlib import Path


# ============================================================
# DAY 09 PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# DAY 09 DATABASE
# ============================================================

DB_DIR = PROJECT_ROOT / "db"

DB_PATH = DB_DIR / "day09.sqlite3"


# ============================================================
# CREATE DATABASE DIRECTORY
# ============================================================

DB_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection
    to the Day 09 SQLite database.
    """

    return sqlite3.connect(DB_PATH)


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables() -> None:
    """
    Create all Day 09 tables.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # ========================================================
    # TASK 1 TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS baseline_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            embedding_model TEXT NOT NULL,
            chunk_size INTEGER NOT NULL,
            chunk_overlap INTEGER NOT NULL,
            top_k INTEGER NOT NULL,
            filters TEXT NOT NULL,
            score_threshold REAL,
            prompt_version TEXT NOT NULL,
            frozen_at TEXT NOT NULL
        )
        """
    )

    # ========================================================
    # TASK 2 - RETRIEVAL EVIDENCE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS retrieval_evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question_id TEXT NOT NULL UNIQUE,

            question TEXT NOT NULL,

            expected_source TEXT NOT NULL,

            day6_top1_source TEXT,

            day6_expected_rank INTEGER,

            day6_source_found INTEGER NOT NULL,

            day6_result_quality TEXT NOT NULL,

            day8_status TEXT NOT NULL,

            day8_grounded INTEGER NOT NULL,

            day8_citation_valid INTEGER NOT NULL,

            day8_result_quality TEXT NOT NULL,

            notes TEXT
        )
        """
    )

    # ========================================================
    # TASK 2 - FIVE WEAKEST QUESTIONS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weak_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question_id TEXT NOT NULL UNIQUE,

            question TEXT NOT NULL,

            expected_source TEXT NOT NULL,

            failure_type TEXT NOT NULL,

            weakness_score REAL NOT NULL,

            selection_reason TEXT NOT NULL,

            FOREIGN KEY (question_id)
                REFERENCES retrieval_evidence(question_id)
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE TASK 1 BASELINE
# ============================================================

def save_baseline(config: dict) -> None:
    """
    Save frozen Task 1 configuration.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO baseline_config (
            embedding_model,
            chunk_size,
            chunk_overlap,
            top_k,
            filters,
            score_threshold,
            prompt_version,
            frozen_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            config["embedding_model"],
            config["chunk_size"],
            config["chunk_overlap"],
            config["top_k"],
            config["filters"],
            config["score_threshold"],
            config["prompt_version"],
            config["frozen_at"],
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE RETRIEVAL EVIDENCE
# ============================================================

def save_retrieval_evidence(
    evidence: dict
) -> None:
    """
    Save Day 6 and Day 8 evidence
    into the Day 09 database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO retrieval_evidence (
            question_id,
            question,
            expected_source,
            day6_top1_source,
            day6_expected_rank,
            day6_source_found,
            day6_result_quality,
            day8_status,
            day8_grounded,
            day8_citation_valid,
            day8_result_quality,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            evidence["question_id"],
            evidence["question"],
            evidence["expected_source"],
            evidence["day6_top1_source"],
            evidence["day6_expected_rank"],
            int(evidence["day6_source_found"]),
            evidence["day6_result_quality"],
            evidence["day8_status"],
            int(evidence["day8_grounded"]),
            int(evidence["day8_citation_valid"]),
            evidence["day8_result_quality"],
            evidence["notes"],
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE WEAK QUESTION
# ============================================================

def save_weak_question(
    question: dict
) -> None:
    """
    Save one selected weak question.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO weak_questions (
            question_id,
            question,
            expected_source,
            failure_type,
            weakness_score,
            selection_reason
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            question["question_id"],
            question["question"],
            question["expected_source"],
            question["failure_type"],
            question["weakness_score"],
            question["selection_reason"],
        )
    )

    connection.commit()

    connection.close()