import json
import time
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# DAY 10 - TASK 2
# QUERY REWRITING / MULTI-QUERY RETRIEVAL
# ============================================================


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_ROOT = (
    PROJECT_ROOT.parent / "d5-6 genai assistant"
)

VECTOR_DB_PATH = (
    SOURCE_ROOT / "outputs" / "chroma_db"
)

COLLECTION_NAME = "genai_documents"

QUESTION_FILE = (
    SOURCE_ROOT / "data" / "retrieval_questions.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "day10_task2_multi_query_results.json"
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5

MULTI_QUERY_COUNT = 3


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_questions() -> list[dict[str, Any]]:

    with QUESTION_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if isinstance(data, list):

        return data

    if isinstance(data, dict):

        if "questions" in data:

            return data["questions"]

        if "data" in data:

            return data["data"]

    raise ValueError(
        "Invalid retrieval_questions.json format."
    )


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        MODEL_NAME
    )

    print(
        f"Model: {MODEL_NAME}"
    )

    return model


# ============================================================
# LOAD CHROMA
# ============================================================

def load_collection():

    print(
        "\nConnecting to ChromaDB..."
    )

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_PATH)
    )

    collection = client.get_collection(
        COLLECTION_NAME
    )

    print(
        f"Collection: {COLLECTION_NAME}"
    )

    print(
        f"Vectors: {collection.count()}"
    )

    return collection


# ============================================================
# GET DOCUMENT ID FROM METADATA
# ============================================================

def get_doc_id(
    metadata: dict[str, Any],
) -> str | None:

    # --------------------------------------------------------
    # Preferred format
    # --------------------------------------------------------

    if metadata.get("doc_id"):

        return str(
            metadata["doc_id"]
        )


    # --------------------------------------------------------
    # Alternative format
    # --------------------------------------------------------

    if metadata.get("document_id"):

        return str(
            metadata["document_id"]
        )


    # --------------------------------------------------------
    # Day-09 format
    #
    # document_001_chunk_000
    #          ↓
    # document_001
    # --------------------------------------------------------

    chunk_id = metadata.get(
        "chunk_id"
    )

    if chunk_id:

        chunk_id = str(
            chunk_id
        )

        if "_chunk_" in chunk_id:

            return chunk_id.split(
                "_chunk_",
                1,
            )[0]


    return None


# ============================================================
# SEARCH CHROMADB
# ============================================================

def retrieve(
    collection,
    model,
    query: str,
) -> list[dict[str, Any]]:

    # --------------------------------------------------------
    # Convert query to embedding
    # --------------------------------------------------------

    embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )[0].tolist()


    # --------------------------------------------------------
    # Chroma search
    # --------------------------------------------------------

    result = collection.query(
        query_embeddings=[embedding],
        n_results=TOP_K,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )


    documents = result[
        "documents"
    ][0]

    metadatas = result[
        "metadatas"
    ][0]

    distances = result[
        "distances"
    ][0]


    retrieved = []


    # --------------------------------------------------------
    # Convert Chroma results
    # --------------------------------------------------------

    for index in range(
        len(metadatas)
    ):

        metadata = metadatas[index]

        doc_id = get_doc_id(
            metadata
        )

        if doc_id is None:

            continue


        retrieved.append(
            {
                "doc_id": doc_id,

                "chunk_id":
                    metadata.get(
                        "chunk_id"
                    ),

                "document":
                    documents[index],

                "distance":
                    distances[index],
            }
        )


    return retrieved


# ============================================================
# GENERATE QUERY VARIATIONS
# ============================================================

def generate_queries(
    question: str,
) -> list[str]:

    return [

        question,

        (
            "Explain "
            + question
        ),

        (
            "Provide detailed information about "
            + question
        ),
    ][:MULTI_QUERY_COUNT]


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def merge_results(
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    best = {}


    for result in results:

        key = result[
            "chunk_id"
        ]


        if key not in best:

            best[key] = result

        else:

            old_distance = best[key][
                "distance"
            ]

            new_distance = result[
                "distance"
            ]

            if (
                new_distance
                < old_distance
            ):

                best[key] = result


    # --------------------------------------------------------
    # Sort by semantic distance
    # Smaller distance = better result
    # --------------------------------------------------------

    merged = sorted(
        best.values(),
        key=lambda x: x["distance"],
    )


    return merged[:TOP_K]


# ============================================================
# FIND EXPECTED DOCUMENT RANK
# ============================================================

def find_rank(
    results: list[dict[str, Any]],
    expected_doc_id: str,
) -> int | None:

    expected = (
        str(expected_doc_id)
        .strip()
        .lower()
    )


    for rank, result in enumerate(
        results,
        start=1,
    ):

        actual = (
            str(result["doc_id"])
            .strip()
            .lower()
        )


        if actual == expected:

            return rank


    return None


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(
    records: list[dict[str, Any]],
) -> dict[str, Any]:

    total = len(records)

    hits = sum(
        record["rank"] is not None
        for record in records
    )

    top1 = sum(
        record["rank"] == 1
        for record in records
    )


    reciprocal_sum = 0.0


    for record in records:

        rank = record["rank"]

        if rank is not None:

            reciprocal_sum += (
                1 / rank
            )


    latency_sum = sum(
        record["latency_ms"]
        for record in records
    )


    return {

        "total_questions": total,

        "retrieval_recall": round(
            hits / total
            if total
            else 0,
            4,
        ),

        "top1_accuracy": round(
            top1 / total
            if total
            else 0,
            4,
        ),

        "mrr": round(
            reciprocal_sum / total
            if total
            else 0,
            4,
        ),

        "average_latency_ms": round(
            latency_sum / total
            if total
            else 0,
            3,
        ),
    }


# ============================================================
# BASELINE RETRIEVAL
# ============================================================

def run_baseline(
    questions,
    collection,
    model,
):

    records = []


    print(
        "\n"
        + "=" * 70
    )

    print(
        "BASELINE SINGLE-QUERY RETRIEVAL"
    )

    print(
        "=" * 70
    )


    for number, item in enumerate(
        questions,
        start=1,
    ):

        question = item[
            "question"
        ]

        expected = item[
            "expected_doc_id"
        ]


        start = time.perf_counter()


        results = retrieve(
            collection,
            model,
            question,
        )


        latency = (
            time.perf_counter()
            - start
        ) * 1000


        rank = find_rank(
            results,
            expected,
        )


        status = (
            "PASS"
            if rank is not None
            else "FAIL"
        )


        print(
            f"{number:02d}. "
            f"{status} | "
            f"Expected={expected} | "
            f"Rank={rank}"
        )


        records.append(
            {
                "question_number":
                    number,

                "question":
                    question,

                "expected_doc_id":
                    expected,

                "rank":
                    rank,

                "latency_ms":
                    round(
                        latency,
                        3,
                    ),
            }
        )


    return {

        "metrics":
            calculate_metrics(
                records
            ),

        "results":
            records,
    }


# ============================================================
# MULTI-QUERY RETRIEVAL
# ============================================================

def run_multi_query(
    questions,
    collection,
    model,
):

    records = []


    print(
        "\n"
        + "=" * 70
    )

    print(
        "MULTI-QUERY RETRIEVAL"
    )

    print(
        "=" * 70
    )


    for number, item in enumerate(
        questions,
        start=1,
    ):

        question = item[
            "question"
        ]

        expected = item[
            "expected_doc_id"
        ]


        start = time.perf_counter()


        # ----------------------------------------------------
        # Generate query variations
        # ----------------------------------------------------

        queries = generate_queries(
            question
        )


        all_results = []


        # ----------------------------------------------------
        # Retrieve each variation
        # ----------------------------------------------------

        for query in queries:

            results = retrieve(
                collection,
                model,
                query,
            )

            all_results.extend(
                results
            )


        # ----------------------------------------------------
        # Merge and rank
        # ----------------------------------------------------

        merged_results = merge_results(
            all_results
        )


        latency = (
            time.perf_counter()
            - start
        ) * 1000


        rank = find_rank(
            merged_results,
            expected,
        )


        status = (
            "PASS"
            if rank is not None
            else "FAIL"
        )


        print(
            f"{number:02d}. "
            f"{status} | "
            f"Expected={expected} | "
            f"Rank={rank}"
        )


        records.append(
            {
                "question_number":
                    number,

                "question":
                    question,

                "expected_doc_id":
                    expected,

                "generated_queries":
                    queries,

                "rank":
                    rank,

                "latency_ms":
                    round(
                        latency,
                        3,
                    ),
            }
        )


    return {

        "metrics":
            calculate_metrics(
                records
            ),

        "results":
            records,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "DAY 10 - TASK 2"
    )

    print(
        "QUERY REWRITING / MULTI-QUERY RETRIEVAL"
    )

    print("=" * 70)


    # --------------------------------------------------------
    # Questions
    # --------------------------------------------------------

    print(
        "\nLoading evaluation questions..."
    )

    questions = load_questions()

    print(
        f"Questions loaded: "
        f"{len(questions)}"
    )


    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model = load_model()


    # --------------------------------------------------------
    # Chroma
    # --------------------------------------------------------

    collection = load_collection()


    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    baseline = run_baseline(
        questions,
        collection,
        model,
    )


    print(
        "\nBASELINE METRICS"
    )

    print("-" * 70)

    print(
        json.dumps(
            baseline["metrics"],
            indent=2,
        )
    )


    # --------------------------------------------------------
    # Multi-query
    # --------------------------------------------------------

    multi_query = run_multi_query(
        questions,
        collection,
        model,
    )


    print(
        "\nMULTI-QUERY METRICS"
    )

    print("-" * 70)

    print(
        json.dumps(
            multi_query["metrics"],
            indent=2,
        )
    )


    # --------------------------------------------------------
    # Comparison
    # --------------------------------------------------------

    baseline_metrics = (
        baseline["metrics"]
    )

    multi_metrics = (
        multi_query["metrics"]
    )


    recall_change = round(

        multi_metrics[
            "retrieval_recall"
        ]

        -

        baseline_metrics[
            "retrieval_recall"
        ],

        4,
    )


    top1_change = round(

        multi_metrics[
            "top1_accuracy"
        ]

        -

        baseline_metrics[
            "top1_accuracy"
        ],

        4,
    )


    mrr_change = round(

        multi_metrics["mrr"]

        -

        baseline_metrics["mrr"],

        4,
    )


    latency_change = round(

        multi_metrics[
            "average_latency_ms"
        ]

        -

        baseline_metrics[
            "average_latency_ms"
        ],

        3,
    )


    # --------------------------------------------------------
    # Decision
    # --------------------------------------------------------

    if (
        recall_change > 0
        and mrr_change >= 0
    ):

        decision = "ACCEPT"

    else:

        decision = "REJECT"


    # --------------------------------------------------------
    # Print comparison
    # --------------------------------------------------------

    print(
        "\n"
        + "=" * 70
    )

    print(
        "TASK 2 COMPARISON"
    )

    print(
        "=" * 70
    )


    print(
        f"Baseline Recall      : "
        f"{baseline_metrics['retrieval_recall']}"
    )

    print(
        f"Multi-query Recall   : "
        f"{multi_metrics['retrieval_recall']}"
    )

    print(
        f"Recall Change        : "
        f"{recall_change:+.4f}"
    )


    print()


    print(
        f"Baseline Top-1       : "
        f"{baseline_metrics['top1_accuracy']}"
    )

    print(
        f"Multi-query Top-1    : "
        f"{multi_metrics['top1_accuracy']}"
    )

    print(
        f"Top-1 Change         : "
        f"{top1_change:+.4f}"
    )


    print()


    print(
        f"Baseline MRR         : "
        f"{baseline_metrics['mrr']}"
    )

    print(
        f"Multi-query MRR      : "
        f"{multi_metrics['mrr']}"
    )

    print(
        f"MRR Change           : "
        f"{mrr_change:+.4f}"
    )


    print()


    print(
        f"Baseline Latency     : "
        f"{baseline_metrics['average_latency_ms']} ms"
    )

    print(
        f"Multi-query Latency  : "
        f"{multi_metrics['average_latency_ms']} ms"
    )

    print(
        f"Latency Change       : "
        f"{latency_change:+.3f} ms"
    )


    print()

    print(
        f"Decision: {decision}"
    )


    # --------------------------------------------------------
    # Save output
    # --------------------------------------------------------

    output = {

        "task":
            "day10_task2",

        "experiment":
            "query_rewriting_multi_query",

        "configuration": {

            "embedding_model":
                MODEL_NAME,

            "top_k":
                TOP_K,

            "multi_query_count":
                MULTI_QUERY_COUNT,
        },

        "baseline":
            baseline,

        "multi_query":
            multi_query,

        "comparison": {

            "recall_change":
                recall_change,

            "top1_change":
                top1_change,

            "mrr_change":
                mrr_change,

            "latency_change_ms":
                latency_change,
        },

        "decision":
            decision,
    }


    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )


    print()

    print(
        "Results saved to:"
    )

    print(
        OUTPUT_FILE
    )


    print()

    print("=" * 70)

    print(
        "DAY 10 TASK 2 COMPLETE"
    )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()