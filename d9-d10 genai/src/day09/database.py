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

    connection = sqlite3.connect(
        DB_PATH
    )

    return connection


# ============================================================
# CREATE TABLE
# ============================================================

def create_tables() -> None:
    """
    Create the baseline configuration table.
    """

    connection = get_connection()

    cursor = connection.cursor()

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

    connection.commit()

    connection.close()


# ============================================================
# INSERT BASELINE
# ============================================================

def save_baseline(config: dict) -> None:
    """
    Save one frozen baseline configuration
    into the Day 09 database.
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