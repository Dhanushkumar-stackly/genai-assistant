from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.embeddings import EmbeddingModel
from app.search import SemanticSearcher
from app.vector_store.vector_store import VectorStore


# ============================================================
# PATHS
# ============================================================

EVALUATION_FILE = Path(
    "data/evaluation/evaluation_questions.json"
)

RESULTS_FILE = Path(
    "outputs/retrieval_evaluation.json"
)


# ============================================================
# LOAD EVALUATION QUESTIONS
# ============================================================

def load_questions() -> list[dict[str, Any]]:

    if not EVALUATION_FILE.exists():

        raise FileNotFoundError(
            f"\nEvaluation file not found:\n"
            f"{EVALUATION_FILE}\n"
        )

    if EVALUATION_FILE.stat().st_size == 0:

        raise ValueError(
            f"\nEvaluation file is empty:\n"
            f"{EVALUATION_FILE}\n"
        )

    try:

        with EVALUATION_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as error:

        raise ValueError(
            "\nInvalid JSON in evaluation file.\n"
            f"File: {EVALUATION_FILE}\n"
            f"Line: {error.lineno}\n"
            f"Column: {error.colno}\n"
            f"Message: {error.msg}\n"
        ) from error

    if not isinstance(data, list):

        raise ValueError(
            "Evaluation JSON must contain a list."
        )

    if not data:

        raise ValueError(
            "Evaluation question list is empty."
        )

    return data


# ============================================================
# VALIDATE QUESTIONS
# ============================================================

def validate_questions(
    questions: list[dict[str, Any]],
) -> None:

    required_fields = {
        "id",
        "question",
        "expected_sources",
    }

    for index, item in enumerate(
        questions,
        start=1,
    ):

        if not isinstance(item, dict):

            raise ValueError(
                f"Question {index} must be a JSON object."
            )

        missing = (
            required_fields
            - set(item.keys())
        )

        if missing:

            raise ValueError(
                f"Question {index} is missing: "
                f"{sorted(missing)}"
            )

        if not isinstance(
            item["question"],
            str,
        ):

            raise ValueError(
                f"Question {item['id']} "
                f"'question' must be a string."
            )

        if not isinstance(
            item["expected_sources"],
            list,
        ):

            raise ValueError(
                f"Question {item['id']} "
                f"'expected_sources' must be a list."
            )


# ============================================================
# LOAD VECTOR STORE
# ============================================================

def create_vector_store() -> VectorStore:

    print()
    print("Step 2: Loading vector store...")

    vector_store = VectorStore(
        persist_directory="vector_db",
        collection_name="d5_chunks",
    )

    count = vector_store.count()

    print(
        f"Vector count: {count}"
    )

    if count == 0:

        raise ValueError(
            "\nVector store is empty.\n"
            "Run this first:\n\n"
            "python -m scripts.build_vector_index\n"
        )

    return vector_store


# ============================================================
# GET SOURCE FROM RESULT
# ============================================================

def get_source(
    result: dict[str, Any],
) -> str | None:

    # Direct source
    source = result.get("source")

    if source:
        return str(source)

    # Metadata source
    metadata = result.get("metadata")

    if isinstance(
        metadata,
        dict,
    ):

        source = metadata.get("source")

        if source:
            return str(source)

    return None


# ============================================================
# EVALUATE ONE QUESTION
# ============================================================

def evaluate_question(
    searcher: SemanticSearcher,
    question: dict[str, Any],
) -> dict[str, Any]:

    question_id = question["id"]

    query = question["question"]

    expected_sources = [
        str(source)
        for source
        in question["expected_sources"]
    ]

    results = searcher.search(
        query=query,
        top_k=5,
    )

    retrieved_sources = []

    for result in results:

        source = get_source(result)

        if source:

            retrieved_sources.append(
                source
            )

    # Remove duplicates while preserving order
    retrieved_sources = list(
        dict.fromkeys(
            retrieved_sources
        )
    )

    # If expected_sources is empty,
    # we cannot calculate a meaningful hit.
    if expected_sources:

        hit = any(
            source in expected_sources
            for source in retrieved_sources
        )

    else:

        hit = False

    return {
        "id": question_id,
        "question": query,
        "expected_sources":
            expected_sources,
        "retrieved_sources":
            retrieved_sources,
        "hit":
            hit,
        "result_count":
            len(results),
        "results":
            results,
    }


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print()
    print("=" * 70)
    print("DAY 06 - RETRIEVAL EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Step 1
    # --------------------------------------------------------

    print()
    print(
        "Step 1: Loading evaluation questions..."
    )

    questions = load_questions()

    validate_questions(
        questions
    )

    print(
        f"Loaded questions: "
        f"{len(questions)}"
    )

    # --------------------------------------------------------
    # Step 2
    # --------------------------------------------------------

    vector_store = create_vector_store()

    # --------------------------------------------------------
    # Step 3
    # --------------------------------------------------------

    print()
    print(
        "Step 3: Loading embedding model..."
    )

    embedding_model = EmbeddingModel()

    # --------------------------------------------------------
    # Step 4
    # --------------------------------------------------------

    print()
    print(
        "Step 4: Creating semantic searcher..."
    )

    searcher = SemanticSearcher(
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    print(
        "Semantic searcher ready."
    )

    # --------------------------------------------------------
    # Step 5
    # --------------------------------------------------------

    print()
    print(
        "Step 5: Evaluating retrieval..."
    )

    evaluation_results = []

    successful_hits = 0

    evaluable_questions = 0

    for question in questions:

        print()
        print(
            "-" * 70
        )

        print(
            f"Question ID: "
            f"{question['id']}"
        )

        print(
            f"Question: "
            f"{question['question']}"
        )

        result = evaluate_question(
            searcher=searcher,
            question=question,
        )

        evaluation_results.append(
            result
        )

        expected = (
            result["expected_sources"]
        )

        retrieved = (
            result["retrieved_sources"]
        )

        print(
            f"Expected sources: "
            f"{expected}"
        )

        print(
            f"Retrieved sources: "
            f"{retrieved}"
        )

        if expected:

            evaluable_questions += 1

            if result["hit"]:

                successful_hits += 1

                print(
                    "Result: HIT"
                )

            else:

                print(
                    "Result: MISS"
                )

        else:

            print(
                "Result: NOT EVALUABLE "
                "(expected_sources is empty)"
            )

    # --------------------------------------------------------
    # Step 6 - Metrics
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        "Step 6: Calculating metrics..."
    )

    if evaluable_questions:

        hit_rate = (
            successful_hits
            / evaluable_questions
        )

    else:

        hit_rate = 0.0

    print(
        f"Total questions: "
        f"{len(questions)}"
    )

    print(
        f"Evaluable questions: "
        f"{evaluable_questions}"
    )

    print(
        f"Successful hits: "
        f"{successful_hits}"
    )

    print(
        f"Hit rate: "
        f"{hit_rate:.2%}"
    )

    # --------------------------------------------------------
    # Step 7 - Save
    # --------------------------------------------------------

    print()
    print(
        "Step 7: Saving evaluation results..."
    )

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "total_questions":
            len(questions),

        "evaluable_questions":
            evaluable_questions,

        "successful_hits":
            successful_hits,

        "hit_rate":
            hit_rate,

        "results":
            evaluation_results,
    }

    with RESULTS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Results saved to: "
        f"{RESULTS_FILE}"
    )

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "RETRIEVAL EVALUATION COMPLETE"
    )
    print("=" * 70)

    print(
        f"Hit rate: {hit_rate:.2%}"
    )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()