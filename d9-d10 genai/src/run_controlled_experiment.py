import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_ROOT = (
    PROJECT_ROOT.parent
    / "d5-6 genai assistant"
)


# ============================================================
# INPUT FILES
# ============================================================

QUESTIONS_FILE = (
    SOURCE_ROOT
    / "data"
    / "retrieval_questions.json"
)

DIAGNOSIS_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "retrieval_failure_diagnosis.json"
)


# ============================================================
# DAY 8 VECTOR DATABASE
# ============================================================

VECTOR_DB = (
    SOURCE_ROOT
    / "outputs"
    / "chroma_db"
)

COLLECTION_NAME = "genai_documents"


# ============================================================
# OUTPUT FILE
# ============================================================

OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "controlled_experiment_results.json"
)


# ============================================================
# BASELINE CONFIGURATION
# ============================================================

BASELINE_TOP_K = 5

BASELINE_MODEL = (
    "all-MiniLM-L6-v2"
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

# Controlled experiment:
# Change ONLY top_k.
#
# Baseline:
# top_k = 5
#
# Experiment:
# top_k = 10

EXPERIMENT_TOP_K = 10


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
# LOAD QUESTIONS
# ============================================================

def load_questions():

    questions = load_json(
        QUESTIONS_FILE
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "retrieval_questions.json "
            "must contain a list."
        )

    return questions


# ============================================================
# CONVERT CHUNK ID → DOCUMENT ID
# ============================================================

def extract_document_id(metadata):

    """
    Day 8 ChromaDB stores document identity
    inside chunk_id.

    Example:

        document_001_chunk_000

    We need:

        document_001
    """

    if not metadata:

        return None

    # --------------------------------------------------------
    # Actual Day 8 metadata key
    # --------------------------------------------------------

    chunk_id = metadata.get(
        "chunk_id"
    )

    if not chunk_id:

        return None

    # --------------------------------------------------------
    # Convert:
    #
    # document_001_chunk_000
    #
    # into:
    #
    # document_001
    # --------------------------------------------------------

    if "_chunk_" in chunk_id:

        return chunk_id.split(
            "_chunk_",
            1,
        )[0]

    return None


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve(
    questions,
    model,
    top_k,
):

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    print(
        f"\nCollection: "
        f"{COLLECTION_NAME}"
    )

    print(
        f"Vector count: "
        f"{collection.count()}"
    )

    results = []

    for number, item in enumerate(
        questions,
        start=1,
    ):

        question = item[
            "question"
        ]

        expected_doc = item[
            "expected_doc_id"
        ]

        # ----------------------------------------------------
        # Create query embedding
        # ----------------------------------------------------

        embedding = model.encode(
            question,
            convert_to_numpy=True,
        )

        # ----------------------------------------------------
        # ChromaDB retrieval
        # ----------------------------------------------------

        search = collection.query(
            query_embeddings=[
                embedding.tolist()
            ],
            n_results=top_k,
            include=[
                "metadatas",
                "distances",
            ],
        )

        metadatas = (
            search["metadatas"][0]
        )

        distances = (
            search["distances"][0]
        )

        # ----------------------------------------------------
        # Convert chunk IDs to document IDs
        # ----------------------------------------------------

        retrieved_docs = []

        for metadata in metadatas:

            document_id = (
                extract_document_id(
                    metadata
                )
            )

            if document_id is not None:

                retrieved_docs.append(
                    document_id
                )

        # ----------------------------------------------------
        # Find expected document rank
        # ----------------------------------------------------

        expected_rank = None

        if expected_doc in retrieved_docs:

            expected_rank = (
                retrieved_docs.index(
                    expected_doc
                )
                + 1
            )

        # ----------------------------------------------------
        # Retrieval status
        # ----------------------------------------------------

        recovered = (
            expected_rank is not None
        )

        top1_hit = (
            expected_rank == 1
        )

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        result = {

            "question":
                question,

            "expected_doc_id":
                expected_doc,

            "retrieved_doc_ids":
                retrieved_docs,

            "distances":
                distances,

            "expected_rank":
                expected_rank,

            "top1_hit":
                top1_hit,

            "recovered":
                recovered,

            "top_k":
                top_k,
        }

        results.append(
            result
        )

        # ----------------------------------------------------
        # Console output
        # ----------------------------------------------------

        status = (
            "PASS"
            if recovered
            else "FAIL"
        )

        print(
            f"{number:02d}. "
            f"{status} | "
            f"Expected={expected_doc} | "
            f"Retrieved={retrieved_docs} | "
            f"Rank={expected_rank}"
        )

    return results


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(results):

    total = len(results)

    if total == 0:

        return {

            "total_questions": 0,

            "retrieval_recall": 0.0,

            "top1_accuracy": 0.0,

            "mrr": 0.0,
        }

    retrieved_count = 0

    top1_count = 0

    reciprocal_rank_sum = 0.0

    for result in results:

        rank = result[
            "expected_rank"
        ]

        # ----------------------------------------------------
        # Recall
        # ----------------------------------------------------

        if rank is not None:

            retrieved_count += 1

            reciprocal_rank_sum += (
                1 / rank
            )

        # ----------------------------------------------------
        # Top 1
        # ----------------------------------------------------

        if rank == 1:

            top1_count += 1

    # --------------------------------------------------------
    # Recall
    # --------------------------------------------------------

    recall = (
        retrieved_count
        / total
    )

    # --------------------------------------------------------
    # Top 1 accuracy
    # --------------------------------------------------------

    top1_accuracy = (
        top1_count
        / total
    )

    # --------------------------------------------------------
    # MRR
    # --------------------------------------------------------

    mrr = (
        reciprocal_rank_sum
        / total
    )

    return {

        "total_questions":
            total,

        "retrieval_recall":
            round(
                recall,
                4,
            ),

        "top1_accuracy":
            round(
                top1_accuracy,
                4,
            ),

        "mrr":
            round(
                mrr,
                4,
            ),
    }


# ============================================================
# EVALUATE WEAK QUESTIONS
# ============================================================

def evaluate_weak_questions(
    weak_questions,
    results,
):

    result_map = {

        item["question"]: item

        for item in results

    }

    evaluated = []

    for weak in weak_questions:

        question = weak[
            "question"
        ]

        result = result_map.get(
            question
        )

        if result is None:

            continue

        evaluated.append(
            {

                "question":
                    question,

                "expected_doc_id":
                    result[
                        "expected_doc_id"
                    ],

                "expected_rank":
                    result[
                        "expected_rank"
                    ],

                "retrieved_doc_ids":
                    result[
                        "retrieved_doc_ids"
                    ],

                "recovered":
                    result[
                        "recovered"
                    ],
            }
        )

    return evaluated


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("DAY 09 - TASK 4")
    print("CONTROLLED RETRIEVAL EXPERIMENT")
    print("=" * 70)

    # ========================================================
    # VALIDATE PATHS
    # ========================================================

    print(
        "\nChecking source files..."
    )

    print(
        f"Questions file: "
        f"{QUESTIONS_FILE}"
    )

    print(
        f"Questions exists: "
        f"{QUESTIONS_FILE.exists()}"
    )

    print(
        f"Vector DB: "
        f"{VECTOR_DB}"
    )

    print(
        f"Vector DB exists: "
        f"{VECTOR_DB.exists()}"
    )

    print(
        f"Diagnosis file: "
        f"{DIAGNOSIS_FILE}"
    )

    print(
        f"Diagnosis exists: "
        f"{DIAGNOSIS_FILE.exists()}"
    )

    if not QUESTIONS_FILE.exists():

        raise FileNotFoundError(
            "retrieval_questions.json "
            "was not found."
        )

    if not VECTOR_DB.exists():

        raise FileNotFoundError(
            "Day 8 ChromaDB was not found."
        )

    if not DIAGNOSIS_FILE.exists():

        raise FileNotFoundError(
            "retrieval_failure_diagnosis.json "
            "was not found."
        )

    # ========================================================
    # LOAD DATA
    # ========================================================

    questions = load_questions()

    diagnoses = load_json(
        DIAGNOSIS_FILE
    )

    if len(diagnoses) != 5:

        raise ValueError(
            "Task 3 must contain exactly "
            "five diagnosed questions."
        )

    print(
        f"\nTotal questions: "
        f"{len(questions)}"
    )

    print(
        f"Weak questions: "
        f"{len(diagnoses)}"
    )

    # ========================================================
    # LOAD EMBEDDING MODEL
    # ========================================================

    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        BASELINE_MODEL
    )

    print(
        f"Model: "
        f"{BASELINE_MODEL}"
    )

    # ========================================================
    # BASELINE EXPERIMENT
    # ========================================================

    print("\n" + "=" * 70)
    print("BASELINE")
    print("=" * 70)

    print(
        f"\nBaseline top_k: "
        f"{BASELINE_TOP_K}"
    )

    baseline_results = retrieve(
        questions,
        model,
        BASELINE_TOP_K,
    )

    baseline_metrics = (
        calculate_metrics(
            baseline_results
        )
    )

    print(
        "\nBaseline metrics:"
    )

    print(
        json.dumps(
            baseline_metrics,
            indent=2,
        )
    )

    # ========================================================
    # CONTROLLED EXPERIMENT
    # ========================================================

    print("\n" + "=" * 70)
    print("CONTROLLED EXPERIMENT")
    print("=" * 70)

    print(
        "\nVariable changed: top_k"
    )

    print(
        f"Baseline value: "
        f"{BASELINE_TOP_K}"
    )

    print(
        f"Experiment value: "
        f"{EXPERIMENT_TOP_K}"
    )

    print(
        "\nAll other variables remain unchanged."
    )

    experiment_results = retrieve(
        questions,
        model,
        EXPERIMENT_TOP_K,
    )

    experiment_metrics = (
        calculate_metrics(
            experiment_results
        )
    )

    print(
        "\nExperiment metrics:"
    )

    print(
        json.dumps(
            experiment_metrics,
            indent=2,
        )
    )

    # ========================================================
    # WEAK QUESTIONS
    # ========================================================

    weak_questions = [

        {
            "question":
                item["question"]
        }

        for item in diagnoses

    ]

    baseline_weak = (
        evaluate_weak_questions(
            weak_questions,
            baseline_results,
        )
    )

    experiment_weak = (
        evaluate_weak_questions(
            weak_questions,
            experiment_results,
        )
    )

    # ========================================================
    # CALCULATE IMPROVEMENT
    # ========================================================

    recall_change = (

        experiment_metrics[
            "retrieval_recall"
        ]

        -

        baseline_metrics[
            "retrieval_recall"
        ]

    )

    top1_change = (

        experiment_metrics[
            "top1_accuracy"
        ]

        -

        baseline_metrics[
            "top1_accuracy"
        ]

    )

    mrr_change = (

        experiment_metrics[
            "mrr"
        ]

        -

        baseline_metrics[
            "mrr"
        ]

    )

    # ========================================================
    # INTERPRETATION
    # ========================================================

    if recall_change > 0:

        interpretation = (
            "Increasing top_k improved "
            "retrieval recall."
        )

    elif recall_change < 0:

        interpretation = (
            "Increasing top_k reduced "
            "retrieval recall."
        )

    else:

        interpretation = (
            "Increasing top_k produced "
            "no recall improvement."
        )

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    output = {

        "experiment": {

            "variable":
                "top_k",

            "baseline_value":
                BASELINE_TOP_K,

            "experiment_value":
                EXPERIMENT_TOP_K,

            "embedding_model":
                BASELINE_MODEL,

            "controlled_variables": [

                "embedding_model",

                "chunk_size",

                "chunk_overlap",

                "filters",

                "score_threshold",

                "prompt_version",

            ],
        },

        "baseline": {

            "metrics":
                baseline_metrics,

            "weak_questions":
                baseline_weak,

        },

        "experiment": {

            "metrics":
                experiment_metrics,

            "weak_questions":
                experiment_weak,

        },

        "improvement": {

            "recall_change":
                round(
                    recall_change,
                    4,
                ),

            "top1_accuracy_change":
                round(
                    top1_change,
                    4,
                ),

            "mrr_change":
                round(
                    mrr_change,
                    4,
                ),
        },

        "interpretation":
            interpretation,

        "root_cause_fix": {

            "original_metadata_key":
                "doc_id",

            "actual_metadata_key":
                "chunk_id",

            "example_chunk_id":
                "document_001_chunk_000",

            "extracted_document_id":
                "document_001",

            "reason":
                (
                    "Day 8 ChromaDB stores "
                    "document identity inside "
                    "chunk_id rather than doc_id."
                ),
        },
    }

    # ========================================================
    # SAVE OUTPUT
    # ========================================================

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
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("EXPERIMENT SUMMARY")
    print("=" * 70)

    print(
        f"\nBaseline Recall: "
        f"{baseline_metrics['retrieval_recall']}"
    )

    print(
        f"Experiment Recall: "
        f"{experiment_metrics['retrieval_recall']}"
    )

    print(
        f"Recall Change: "
        f"{recall_change:+.4f}"
    )

    print(
        f"\nBaseline Top-1: "
        f"{baseline_metrics['top1_accuracy']}"
    )

    print(
        f"Experiment Top-1: "
        f"{experiment_metrics['top1_accuracy']}"
    )

    print(
        f"Top-1 Change: "
        f"{top1_change:+.4f}"
    )

    print(
        f"\nBaseline MRR: "
        f"{baseline_metrics['mrr']}"
    )

    print(
        f"Experiment MRR: "
        f"{experiment_metrics['mrr']}"
    )

    print(
        f"MRR Change: "
        f"{mrr_change:+.4f}"
    )

    print(
        f"\nInterpretation:\n"
        f"{interpretation}"
    )

    print(
        "\nTask 4 completed."
    )

    print(
        f"\nSaved to:\n"
        f"{OUTPUT_FILE}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()