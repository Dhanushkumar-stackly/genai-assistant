import json
from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
BASELINE_PATH = DATA_DIR / "baseline.json"


DEFAULT_BASELINE = {
    "day": 9,

    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",

    "chunking": {
        "chunk_size": 1000,
        "chunk_overlap": 200
    },

    "retrieval": {
        "top_k": 5,
        "filters": {},
        "score_threshold": None
    },

    "prompt": {
        "version": "v1"
    },

    "frozen": True,

    "created_at": None
}


def save_baseline(config=None):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if config is None:
        config = DEFAULT_BASELINE.copy()

    config["frozen"] = True

    if not config.get("created_at"):
        config["created_at"] = datetime.now(
            timezone.utc
        ).replace(microsecond=0).isoformat()

    with open(
        BASELINE_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            config,
            file,
            indent=2,
            ensure_ascii=False
        )

    return config


def load_baseline():
    if not BASELINE_PATH.exists():
        raise FileNotFoundError(
            f"Baseline file not found: {BASELINE_PATH}"
        )

    with open(
        BASELINE_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def display_baseline(config):

    print("=" * 70)
    print("DAY 09 - BASELINE CONFIGURATION")
    print("=" * 70)

    print(f"Day                : {config.get('day')}")
    print(
        f"Embedding Model    : "
        f"{config.get('embedding_model')}"
    )

    chunking = config.get("chunking", {})

    print(
        f"Chunk Size         : "
        f"{chunking.get('chunk_size')}"
    )

    print(
        f"Chunk Overlap      : "
        f"{chunking.get('chunk_overlap')}"
    )

    retrieval = config.get("retrieval", {})

    print(
        f"Top K              : "
        f"{retrieval.get('top_k')}"
    )

    print(
        f"Filters            : "
        f"{retrieval.get('filters', {})}"
    )

    print(
        f"Score Threshold    : "
        f"{retrieval.get('score_threshold')}"
    )

    prompt = config.get("prompt", {})

    print(
        f"Prompt Version     : "
        f"{prompt.get('version')}"
    )

    print(
        f"Frozen             : "
        f"{config.get('frozen')}"
    )

    print(
        f"Created At         : "
        f"{config.get('created_at')}"
    )

    print("=" * 70)


def main():

    print("=" * 70)
    print("DAY 09 - FREEZE BASELINE")
    print("=" * 70)

    baseline = save_baseline()

    print("\nCURRENT BASELINE\n")
    display_baseline(baseline)

    print(
        f"\nBaseline saved to: {BASELINE_PATH}"
    )

    print("\nSAVED BASELINE\n")

    saved = load_baseline()
    display_baseline(saved)

    print(
        "\nBaseline configuration frozen successfully."
    )


if __name__ == "__main__":
    main()