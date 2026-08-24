import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_FILE = PROJECT_ROOT / "config" / "day09_baseline.json"


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config: dict) -> None:
    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            config,
            file,
            indent=4
        )


if __name__ == "__main__":
    config = load_config()

    print("=" * 60)
    print("DAY 09 BASELINE CONFIGURATION")
    print("=" * 60)

    for key, value in config.items():
        print(f"{key}: {value}")