import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# DAY 09 DATABASE CONFIGURATION
# ============================================================

DB_DIR = PROJECT_ROOT / "db"

DB_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = DB_DIR / "day09.sqlite3"


# ============================================================
# BASELINE CONFIGURATION
# ============================================================

CONFIG_DIR = PROJECT_ROOT / "config"

CONFIG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FROZEN_BASELINE_PATH = (
    CONFIG_DIR / "frozen_baseline.json"
)


# ============================================================
# BASELINE VALUES
# ============================================================
# These values represent the configuration that Day 09
# considers frozen.
#
# Replace the values ONLY with the actual configuration
# currently used by your Day 09 retrieval pipeline.
# ============================================================

BASELINE_CONFIG = {
    "embedding_model": "all-MiniLM-L6-v2",
    "chunk_size": 500,
    "chunk_overlap": 50,
    "top_k": 5,
    "filters": None,
    "score_threshold": 0.0,
    "prompt_version": "day09_v1"
}


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database() -> None:
    """
    Create the Day 09 baseline table if it does not exist.
    """

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS baseline_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            embedding_model TEXT NOT NULL,
            chunk_size INTEGER NOT NULL,
            chunk_overlap INTEGER NOT NULL,
            top_k INTEGER NOT NULL,
            filters TEXT,
            score_threshold REAL NOT NULL,
            prompt_version TEXT NOT NULL,
            frozen_at TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE BASELINE TO DATABASE
# ============================================================

def save_baseline_to_database() -> None:
    """
    Store the frozen baseline configuration in Day 09 DB.
    """

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    # Prevent duplicate baseline snapshots.
    cursor.execute(
        "DELETE FROM baseline_config"
    )

    frozen_at = datetime.now(
        timezone.utc
    ).isoformat()

    filters_json = json.dumps(
        BASELINE_CONFIG["filters"]
    )

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
            BASELINE_CONFIG["embedding_model"],
            BASELINE_CONFIG["chunk_size"],
            BASELINE_CONFIG["chunk_overlap"],
            BASELINE_CONFIG["top_k"],
            filters_json,
            BASELINE_CONFIG["score_threshold"],
            BASELINE_CONFIG["prompt_version"],
            frozen_at
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE BASELINE TO JSON
# ============================================================

def save_baseline_to_json() -> None:
    """
    Save the frozen baseline configuration as JSON.
    """

    snapshot = {
        "day": "Day 09",
        "purpose": "Frozen retrieval baseline",
        "frozen_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "database": str(DB_PATH),
        "configuration": BASELINE_CONFIG
    }

    with open(
        FROZEN_BASELINE_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            snapshot,
            file,
            indent=4
        )


# ============================================================
# VERIFY BASELINE
# ============================================================

def verify_baseline() -> dict:
    """
    Read the baseline back from the database
    and return it for verification.
    """

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            embedding_model,
            chunk_size,
            chunk_overlap,
            top_k,
            filters,
            score_threshold,
            prompt_version,
            frozen_at
        FROM baseline_config
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise RuntimeError(
            "Baseline configuration was not found in database."
        )

    return {
        "embedding_model": row[0],
        "chunk_size": row[1],
        "chunk_overlap": row[2],
        "top_k": row[3],
        "filters": json.loads(row[4]),
        "score_threshold": row[5],
        "prompt_version": row[6],
        "frozen_at": row[7]
    }


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("=" * 60)
    print("DAY 09 - FREEZE BASELINE")
    print("=" * 60)

    print()
    print(f"Project root    : {PROJECT_ROOT}")
    print(f"Database        : {DB_PATH}")
    print(f"JSON snapshot   : {FROZEN_BASELINE_PATH}")

    print()
    print("Initializing database...")

    initialize_database()

    print("Saving baseline to database...")

    save_baseline_to_database()

    print("Saving JSON snapshot...")

    save_baseline_to_json()

    print()
    print("Verifying frozen baseline...")

    baseline = verify_baseline()

    print()
    print("-" * 60)
    print("FROZEN BASELINE")
    print("-" * 60)

    for key, value in baseline.items():
        print(f"{key:20}: {value}")

    print("-" * 60)

    print()
    print("Baseline successfully frozen.")
    print()
    print(f"Database        : {DB_PATH}")
    print(f"JSON snapshot   : {FROZEN_BASELINE_PATH}")

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()