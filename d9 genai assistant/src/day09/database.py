import sqlite3
from pathlib import Path


# ============================================================
# DAY-09 PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_DIR = PROJECT_ROOT / "db"

DB_PATH = DB_DIR / "day09.sqlite3"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """
    Create a connection to the Day-09 SQLite database.
    """

    DB_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DB_PATH)

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database() -> None:
    """
    Create the Day-09 baseline table.
    """

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS baseline_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                embedding_model TEXT NOT NULL,

                chunk_size INTEGER NOT NULL,

                chunk_overlap INTEGER NOT NULL,

                top_k INTEGER NOT NULL,

                metadata_filters TEXT NOT NULL,

                score_threshold REAL NOT NULL,

                prompt_version TEXT NOT NULL,

                config_hash TEXT NOT NULL UNIQUE,

                frozen_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# CHECK EXISTING BASELINE
# ============================================================

def baseline_exists() -> bool:
    """
    Check whether a frozen baseline already exists.
    """

    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT COUNT(*)
            FROM baseline_config
            """
        ).fetchone()

        return result[0] > 0

    finally:
        connection.close()