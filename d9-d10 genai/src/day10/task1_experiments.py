import json
from pathlib import Path
from typing import Any


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_FILE = (
    PROJECT_ROOT
    / "config"
    / "baseline_config.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "day10_task1_results.json"
)


# ============================================================
# LOAD FROZEN BASELINE
# ============================================================

def load_baseline() -> dict[str, Any]:
    """
    Load the frozen Day 09 baseline configuration.
    """

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Baseline configuration not found: "
            f"{CONFIG_FILE}"
        )

    with CONFIG_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        baseline = json.load(file)

    return baseline


# ============================================================
# CREATE EXPERIMENT CONFIGURATION
# ============================================================

def create_experiment(
    name: str,
    baseline: dict[str, Any],
    *,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    top_k: int | None = None,
) -> dict[str, Any]:
    """
    Create a controlled experiment.

    Only explicitly supplied parameters are changed.
    Everything else remains identical to the baseline.
    """

    experiment = dict(baseline)

    experiment["experiment_name"] = name

    if chunk_size is not None:
        experiment["chunk_size"] = chunk_size

    if chunk_overlap is not None:
        experiment["chunk_overlap"] = chunk_overlap

    if top_k is not None:
        experiment["top_k"] = top_k

    return experiment


# ============================================================
# VERIFY ONE-VARIABLE-AT-A-TIME RULE
# ============================================================

def changed_parameters(
    baseline: dict[str, Any],
    experiment: dict[str, Any],
) -> list[str]:
    """
    Return the configuration fields that changed.
    """

    parameters = [
        "embedding_model",
        "chunk_size",
        "chunk_overlap",
        "top_k",
        "filters",
        "score_threshold",
        "prompt_version",
    ]

    changes = []

    for parameter in parameters:

        if baseline.get(parameter) != experiment.get(
            parameter
        ):
            changes.append(parameter)

    return changes


def validate_controlled_experiment(
    baseline: dict[str, Any],
    experiment: dict[str, Any],
) -> None:
    """
    Ensure exactly one retrieval parameter changed.
    """

    changes = changed_parameters(
        baseline,
        experiment,
    )

    if len(changes) != 1:
        raise ValueError(
            "Controlled experiment must change "
            f"exactly one parameter. "
            f"Changed: {changes}"
        )


# ============================================================
# BUILD DAY 10 TASK 1 EXPERIMENTS
# ============================================================

def build_experiments() -> dict[str, Any]:

    baseline = load_baseline()

    # --------------------------------------------------------
    # Experiment 1:
    # Chunk size 500 -> 300
    # --------------------------------------------------------

    chunking_experiment = create_experiment(
        "chunk_size_300",
        baseline,
        chunk_size=300,
    )

    validate_controlled_experiment(
        baseline,
        chunking_experiment,
    )

    # --------------------------------------------------------
    # Experiment 2:
    # Top-k 5 -> 10
    # --------------------------------------------------------

    top_k_experiment = create_experiment(
        "top_k_10",
        baseline,
        top_k=10,
    )

    validate_controlled_experiment(
        baseline,
        top_k_experiment,
    )

    return {
        "baseline": baseline,
        "experiments": [
            chunking_experiment,
            top_k_experiment,
        ],
    }


# ============================================================
# SAVE EXPERIMENT PLAN
# ============================================================

def save_results(results: dict[str, Any]) -> None:

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
        )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("=" * 60)
    print("DAY 10 - TASK 1")
    print("CHUNKING AND TOP-K EXPERIMENT PLAN")
    print("=" * 60)

    results = build_experiments()

    baseline = results["baseline"]

    print("\nFROZEN BASELINE")
    print("-" * 60)

    print(
        f"Embedding model : "
        f"{baseline['embedding_model']}"
    )

    print(
        f"Chunk size      : "
        f"{baseline['chunk_size']}"
    )

    print(
        f"Chunk overlap   : "
        f"{baseline['chunk_overlap']}"
    )

    print(
        f"Top-k           : "
        f"{baseline['top_k']}"
    )

    print(
        f"Score threshold : "
        f"{baseline['score_threshold']}"
    )

    print("\nEXPERIMENTS")
    print("-" * 60)

    for experiment in results["experiments"]:

        changes = changed_parameters(
            baseline,
            experiment,
        )

        print(
            f"{experiment['experiment_name']} "
            f"| changed={changes}"
        )

    save_results(results)

    print("\nSaved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()