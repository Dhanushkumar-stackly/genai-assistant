import json
from datetime import datetime, timezone
from pathlib import Path

from day09.database import (
    create_tables,
    save_baseline
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_DIR = PROJECT_ROOT / "config"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

CONFIG_FILE = CONFIG_DIR / "baseline_config.json"

REPORT_FILE = OUTPUT_DIR / "baseline_report.txt"


# ============================================================
# CREATE DIRECTORIES
# ============================================================

CONFIG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# INPUT HELPERS
# ============================================================

def ask_text(
    label: str,
    default: str | None = None
) -> str:

    if default:
        value = input(
            f"{label} [{default}]: "
        ).strip()

        return value or default

    while True:

        value = input(
            f"{label}: "
        ).strip()

        if value:
            return value

        print("Value cannot be empty.")


def ask_integer(
    label: str
) -> int:

    while True:

        value = input(
            f"{label}: "
        ).strip()

        try:

            number = int(value)

            if number < 0:
                raise ValueError

            return number

        except ValueError:

            print(
                "Please enter a valid non-negative integer."
            )


def ask_float_or_none(
    label: str
):

    while True:

        value = input(
            f"{label} "
            "(enter 'none' if not used): "
        ).strip()

        if value.lower() == "none":

            return None

        try:

            return float(value)

        except ValueError:

            print(
                "Please enter a number or 'none'."
            )


# ============================================================
# COLLECT BASELINE CONFIGURATION
# ============================================================

def collect_baseline() -> dict:

    print()
    print("=" * 60)
    print("DAY 09 - TASK 1")
    print("FREEZE BASELINE CONFIGURATION")
    print("=" * 60)
    print()

    print(
        "Enter the CURRENT Day 08 configuration."
    )

    print(
        "Do NOT enter experimental/new values."
    )

    print()

    embedding_model = ask_text(
        "Embedding model",
        default="all-MiniLM-L6-v2"
    )

    chunk_size = ask_integer(
        "Chunk size"
    )

    chunk_overlap = ask_integer(
        "Chunk overlap"
    )

    top_k = ask_integer(
        "Top-k"
    )

    filters = ask_text(
        "Filters",
        default="none"
    )

    score_threshold = ask_float_or_none(
        "Score threshold"
    )

    prompt_version = ask_text(
        "Prompt version"
    )

    frozen_at = datetime.now(
        timezone.utc
    ).isoformat()

    return {
        "embedding_model": embedding_model,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "top_k": top_k,
        "filters": filters,
        "score_threshold": score_threshold,
        "prompt_version": prompt_version,
        "frozen_at": frozen_at
    }


# ============================================================
# SAVE JSON CONFIGURATION
# ============================================================

def save_json(config: dict) -> None:

    with CONFIG_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            config,
            file,
            indent=4
        )


# ============================================================
# SAVE HUMAN-READABLE REPORT
# ============================================================

def save_report(config: dict) -> None:

    lines = [
        "=" * 60,
        "DAY 09 - BASELINE CONFIGURATION",
        "=" * 60,
        "",
        f"Embedding model : {config['embedding_model']}",
        f"Chunk size      : {config['chunk_size']}",
        f"Chunk overlap   : {config['chunk_overlap']}",
        f"Top-k           : {config['top_k']}",
        f"Filters         : {config['filters']}",
        f"Score threshold : {config['score_threshold']}",
        f"Prompt version  : {config['prompt_version']}",
        f"Frozen at       : {config['frozen_at']}",
        "",
        "STATUS: BASELINE FROZEN",
        "",
        "No experimental changes have been applied.",
        "=" * 60
    ]

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    create_tables()

    config = collect_baseline()

    save_json(
        config
    )

    save_baseline(
        config
    )

    save_report(
        config
    )

    print()
    print("=" * 60)
    print("BASELINE FROZEN SUCCESSFULLY")
    print("=" * 60)

    print()
    print(
        f"Configuration : {CONFIG_FILE}"
    )

    print(
        f"Database      : "
        f"{PROJECT_ROOT / 'db' / 'day09.sqlite3'}"
    )

    print(
        f"Report        : {REPORT_FILE}"
    )

    print()
    print("Day 09 Task 1 completed.")


if __name__ == "__main__":
    main()