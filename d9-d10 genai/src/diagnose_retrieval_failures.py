import json
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

WEAK_QUESTIONS_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "weak_questions.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "retrieval_failure_diagnosis.json"
)


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path: Path):

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# ============================================================
# DIAGNOSE ONE QUESTION
# ============================================================

def diagnose_question(item):

    question = item["question"]

    expected_doc = item[
        "expected_doc_id"
    ]

    day6_docs = item[
        "day6_retrieved"
    ]

    day8_docs = item[
        "day8_retrieved"
    ]

    day6_rank = item[
        "day6_expected_rank"
    ]

    day8_rank = item[
        "day8_expected_rank"
    ]

    day8_status = item[
        "day8_status"
    ]

    reasons = []

    # --------------------------------------------------------
    # Failure 1: source completely missing
    # --------------------------------------------------------

    if expected_doc not in day6_docs:

        reasons.append(
            "expected_source_missing_from_day6_top_k"
        )

    # --------------------------------------------------------
    # Failure 2: source ranking problem
    # --------------------------------------------------------

    elif day6_rank is not None and day6_rank > 1:

        reasons.append(
            "expected_source_ranked_below_top1"
        )

    # --------------------------------------------------------
    # Failure 3: Day 8 source missing
    # --------------------------------------------------------

    if expected_doc not in day8_docs:

        reasons.append(
            "expected_source_missing_from_day8_top_k"
        )

    # --------------------------------------------------------
    # Failure 4: Day 8 ranking
    # --------------------------------------------------------

    elif day8_rank is not None and day8_rank > 1:

        reasons.append(
            "expected_source_not_ranked_first"
        )

    # --------------------------------------------------------
    # Failure 5: No context
    # --------------------------------------------------------

    if day8_status == "no_context":

        reasons.append(
            "no_usable_context_retrieved"
        )

    # --------------------------------------------------------
    # Determine primary diagnosis
    # --------------------------------------------------------

    if (
        "expected_source_missing_from_day6_top_k"
        in reasons
    ):

        diagnosis = "retrieval_recall_failure"

        experiment_variable = "top_k"

        proposed_change = (
            "Increase top_k and measure whether "
            "the expected source enters the retrieved set."
        )

    elif (
        "expected_source_ranked_below_top1"
        in reasons
    ):

        diagnosis = "ranking_failure"

        experiment_variable = "embedding_model"

        proposed_change = (
            "Test one alternative embedding model "
            "while keeping chunking, top_k, filters, "
            "threshold, and prompt unchanged."
        )

    elif (
        "no_usable_context_retrieved"
        in reasons
    ):

        diagnosis = "context_failure"

        experiment_variable = "chunk_size"

        proposed_change = (
            "Test one different chunk size while "
            "keeping all other retrieval parameters fixed."
        )

    else:

        diagnosis = "mixed_retrieval_failure"

        experiment_variable = "top_k"

        proposed_change = (
            "Run a controlled top_k experiment first "
            "to determine whether broader retrieval "
            "recovers the expected source."
        )

    # --------------------------------------------------------
    # Expected outcome
    # --------------------------------------------------------

    expected_outcome = (
        f"Improve retrieval for: {expected_doc}"
    )

    return {

        "question": question,

        "expected_doc_id": expected_doc,

        "day6_rank": day6_rank,

        "day8_rank": day8_rank,

        "day8_status": day8_status,

        "failure_reasons": reasons,

        "diagnosis": diagnosis,

        "experiment_variable":
            experiment_variable,

        "proposed_change":
            proposed_change,

        "expected_outcome":
            expected_outcome,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    weak_questions = load_json(
        WEAK_QUESTIONS_FILE
    )

    if len(weak_questions) != 5:

        raise ValueError(
            "Task 2 must contain exactly "
            "five weak questions."
        )

    diagnoses = []

    for item in weak_questions:

        diagnosis = diagnose_question(
            item
        )

        diagnoses.append(
            diagnosis
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            diagnoses,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 70)
    print("DAY 09 - TASK 3")
    print("RETRIEVAL FAILURE DIAGNOSIS")
    print("=" * 70)

    for index, item in enumerate(
        diagnoses,
        start=1,
    ):

        print(
            f"\n#{index}"
        )

        print(
            f"Question: "
            f"{item['question']}"
        )

        print(
            f"Expected source: "
            f"{item['expected_doc_id']}"
        )

        print(
            f"Diagnosis: "
            f"{item['diagnosis']}"
        )

        print(
            f"Failure reasons: "
            f"{item['failure_reasons']}"
        )

        print(
            f"Experiment variable: "
            f"{item['experiment_variable']}"
        )

        print(
            f"Proposed change: "
            f"{item['proposed_change']}"
        )

        print(
            f"Expected outcome: "
            f"{item['expected_outcome']}"
        )

        print("-" * 70)

    print(
        "\nTask 3 completed."
    )

    print(
        f"Output saved to:\n"
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()