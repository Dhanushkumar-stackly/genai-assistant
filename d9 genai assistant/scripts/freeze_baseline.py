import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_FILE = (
    PROJECT_ROOT
    / "config"
    / "baseline_config.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "baseline"
)

REPORT_FILE = (
    OUTPUT_DIR
    / "baseline_freeze_report.json"
)


# ============================================================
# LOAD BASELINE CONFIGURATION
# ============================================================

def load_baseline_config() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Baseline configuration not found:\n"
            f"{CONFIG_FILE}"
        )

    with CONFIG_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ============================================================
# CALCULATE FILE HASH
# ============================================================

def calculate_sha256(
    file_path: Path
) -> str:

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for block in iter(
            lambda: file.read(65536),
            b""
        ):
            sha256.update(block)

    return sha256.hexdigest()


# ============================================================
# CREATE FREEZE REPORT
# ============================================================

def create_freeze_report(
    config: dict,
    config_hash: str
) -> dict:

    return {
        "report": {
            "name": "Day 09 Task 1 Baseline Freeze",
            "status": "FROZEN",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        },

        "configuration": config,

        "integrity": {
            "config_file": str(CONFIG_FILE),
            "sha256": config_hash
        }
    }


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("=" * 70)
    print("DAY 09 - TASK 1")
    print("FREEZE BASELINE CONFIGURATION")
    print("=" * 70)

    print()
    print(
        f"Configuration file : {CONFIG_FILE}"
    )

    # --------------------------------------------------------
    # Load configuration
    # --------------------------------------------------------

    config = load_baseline_config()

    print(
        "Configuration loaded successfully."
    )

    # --------------------------------------------------------
    # Calculate SHA256
    # --------------------------------------------------------

    config_hash = calculate_sha256(
        CONFIG_FILE
    )

    print()
    print(
        f"SHA256             : {config_hash}"
    )

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Create freeze report
    # --------------------------------------------------------

    report = create_freeze_report(
        config=config,
        config_hash=config_hash
    )

    # --------------------------------------------------------
    # Save report
    # --------------------------------------------------------

    with REPORT_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print()
    print(
        f"Freeze report saved : {REPORT_FILE}"
    )

    print()
    print("=" * 70)
    print("BASELINE CONFIGURATION FROZEN")
    print("=" * 70)


if __name__ == "__main__":
    main()