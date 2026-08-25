from pathlib import Path
import json


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
BASELINE_FILE = DATA_DIR / "baseline.json"


# ============================================================
# BASELINE CONFIGURATION
# ============================================================

baseline = {
    "day": "Day 09",

    # Keep these values equal to your current Day 6 / Day 8 setup.
    "embedding_model": "all-MiniLM-L6-v2",
    "chunk_size": 500,
    "overlap": 50,
    "top_k": 5,
    "filter": None,
    "score_threshold": 0.3,
    "prompt_version": "v1",
}


# ============================================================
# DISPLAY BASELINE
# ============================================================

def display_baseline(config: dict) -> None:
    """
    Display the frozen baseline configuration.
    """

    print()
    print("=" * 60)
    print("BASELINE CONFIGURATION")
    print("=" * 60)

    print(f"Day                : {config.get('day', 'Day 09')}")
    print(
        f"Embedding Model    : "
        f"{config.get('embedding_model', 'Not specified')}"
    )
    print(f"Chunk Size         : {config.get('chunk_size', 'Not specified')}")
    print(f"Overlap            : {config.get('overlap', 'Not specified')}")
    print(f"Top K              : {config.get('top_k', 'Not specified')}")
    print(f"Filter             : {config.get('filter', 'None')}")
    print(
        f"Score Threshold    : "
        f"{config.get('score_threshold', 'Not specified')}"
    )
    print(
        f"Prompt Version     : "
        f"{config.get('prompt_version', 'Not specified')}"
    )

    print("=" * 60)
    print()


# ============================================================
# SAVE BASELINE
# ============================================================

def save_baseline(config: dict) -> None:
    """
    Save the baseline configuration as JSON.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

    print(f"Baseline saved to: {BASELINE_FILE}")


# ============================================================
# LOAD BASELINE
# ============================================================

def load_baseline() -> dict:
    """
    Load the saved baseline configuration.
    """

    if not BASELINE_FILE.exists():
        raise FileNotFoundError(
            f"Baseline file not found: {BASELINE_FILE}"
        )

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # Display current baseline
    display_baseline(baseline)

    # Save baseline
    save_baseline(baseline)

    # Verify saved baseline
    saved_baseline = load_baseline()

    print("VERIFICATION")
    print("-" * 60)

    display_baseline(saved_baseline)

    print("Baseline configuration frozen successfully.")