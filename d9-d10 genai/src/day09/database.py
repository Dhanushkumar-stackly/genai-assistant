import sqlite3
from pathlib import Path
from typing import Optional


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

    DB_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database() -> None:
    """
    Create the baseline table if it does not exist.
    """

    connection = get_connection()

    try:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS baseline (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day INTEGER NOT NULL,
                embedding_model TEXT NOT NULL,
                chunk_size INTEGER NOT NULL,
                overlap INTEGER NOT NULL,
                top_k INTEGER NOT NULL,
                filters TEXT,
                score_threshold REAL,
                prompt_version TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:

        connection.close()


# ============================================================
# SAVE BASELINE
# ============================================================

def save_baseline(
    day: int,
    embedding_model: str,
    chunk_size: int,
    overlap: int,
    top_k: int,
    filters: str,
    score_threshold: Optional[float],
    prompt_version: str,
    created_at: str,
) -> None:
    """
    Save a baseline configuration to SQLite.
    """

    initialize_database()

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO baseline (
                day,
                embedding_model,
                chunk_size,
                overlap,
                top_k,
                filters,
                score_threshold,
                prompt_version,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                day,
                embedding_model,
                chunk_size,
                overlap,
                top_k,
                filters,
                score_threshold,
                prompt_version,
                created_at,
            ),
        )

        connection.commit()

    finally:

        connection.close()


# ============================================================
# GET LATEST BASELINE
# ============================================================

def get_latest_baseline():
    """
    Return the latest saved baseline.
    """

    initialize_database()

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            SELECT *
            FROM baseline
            ORDER BY id DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:

        connection.close()