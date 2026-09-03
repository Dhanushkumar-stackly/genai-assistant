"""
DAY 09 - TASK 1
FREEZE BASELINE CONFIGURATION

This module records the current retrieval configuration
before controlled experiments are performed.
"""

import json
from datetime import datetime
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

# freeze_baseline.py
#     -> src
#         -> day09
#
# parents[0] = day09
# parents[1] = src
# parents[2] = project root

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

BASELINE_FILE = DATA_DIR / "baseline.json"


# ============================================================
# BASELINE CONFIGURATION
# ============================================================

baseline = {
    "day": 9,

    "embedding_model": (
        "sentence-transformers/all-MiniLM-L6-v2"
    ),

    "chunk_size": 1000,

    "overlap": 200,

    "top_k": 5,

    "filters": {},

    "score_threshold": None,

    "prompt_version": "v1",

    "created_at": datetime.now().isoformat(
        timespec="seconds"
    ),
}


# ============================================================
# VALIDATE BASELINE
# ============================================================

def validate_baseline(config: dict) -> None:
    """
    Make sure every required Day 09 field exists.
    """

    required_fields = [
        "day",
        "embedding_model",
        "chunk_size",
        "overlap",
        "top_k",
        "filters",
        "score_threshold",
        "prompt_version",
        "created_at",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in config
    ]

    if missing_fields:
        raise ValueError(
            "Missing required baseline fields: "
            + ", ".join(missing_fields)
        )


# ============================================================
# DISPLAY BASELINE
# ============================================================

def display_baseline(config: dict) -> None:
    """
    Display the baseline configuration.
    """

    print()
    print("=" * 70)
    print("DAY 09 - BASELINE CONFIGURATION")
    print("=" * 70)

    print(
        f"Day                : "
        f"{config['day']}"
    )

    print(
        f"Embedding Model    : "
        f"{config['embedding_model']}"
    )

    print(
        f"Chunk Size         : "
        f"{config['chunk_size']}"
    )

    print(
        f"Overlap            : "
        f"{config['overlap']}"
    )

    print(
        f"Top K              : "
        f"{config['top_k']}"
    )

    print(
        f"Filters            : "
        f"{config['filters']}"
    )

    print(
        f"Score Threshold    : "
        f"{config['score_threshold']}"
    )

    print(
        f"Prompt Version     : "
        f"{config['prompt_version']}"
    )

    print(
        f"Created At         : "
        f"{config['created_at']}"
    )

    print("=" * 70)


# ============================================================
# SAVE BASELINE
# ============================================================

def save_baseline(config: dict) -> None:
    """
    Save the frozen baseline configuration.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        BASELINE_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            config,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print(
        f"Baseline saved to: {BASELINE_FILE}"
    )


# ============================================================
# LOAD BASELINE
# ============================================================

def load_baseline() -> dict:
    """
    Load the frozen baseline configuration.
    """

    if not BASELINE_FILE.exists():
        raise FileNotFoundError(
            f"Baseline file does not exist: "
            f"{BASELINE_FILE}"
        )

    with open(
        BASELINE_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        config = json.load(file)

    return config


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("=" * 70)
    print("DAY 09 - FREEZE BASELINE")
    print("=" * 70)

    # --------------------------------------------------------
    # Validate current configuration
    # --------------------------------------------------------

    validate_baseline(baseline)

    # --------------------------------------------------------
    # Display current configuration
    # --------------------------------------------------------

    print()
    print("CURRENT BASELINE")

    display_baseline(baseline)

    # --------------------------------------------------------
    # Save configuration
    # --------------------------------------------------------

    save_baseline(baseline)

    # --------------------------------------------------------
    # Load configuration back from disk
    # --------------------------------------------------------

    saved_baseline = load_baseline()

    # --------------------------------------------------------
    # Validate saved configuration
    # --------------------------------------------------------

    validate_baseline(saved_baseline)

    # --------------------------------------------------------
    # Display saved configuration
    # --------------------------------------------------------

    print()
    print("SAVED BASELINE")

    display_baseline(saved_baseline)

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("Baseline configuration frozen successfully.")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()