import json
import time
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# DAY 08 VECTOR DATABASE
# ============================================================

SOURCE_ROOT = (
    PROJECT_ROOT.parent
    / "d5-6 genai assistant"
)

VECTOR_DB_DIR = (
    SOURCE_ROOT
    / "outputs"
    / "chroma_db"
)

COLLECTION_NAME = "genai_documents"


# ============================================================
# EVALUATION QUESTIONS
# ============================================================

QUESTIONS_FILE = (
    SOURCE_ROOT
    / "data"
    / "retrieval_questions.json"
)


# ============================================================
# MODEL
# ============================================================

EMBEDDING_MODEL = (
    "all-MiniLM-L6-v2"
)


# ============================================================
# RETRIEVAL CONFIGURATION
# ============================================================

TOP_K = 5

CANDIDATES_PER_QUERY = 5

MULTI_QUERY_COUNT = 3


# ============================================================
# OUTPUT
# ============================================================

OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "day10_task2_multi_query_results.json"
)


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_questions() -> list[dict[str, Any]]:
    """
    Load the fixed Day 06 / Day 08
    evaluation question set.
    """

    if not QUESTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Questions file not found:\n"
            f"{QUESTIONS_FILE}"
        )

    with QUESTIONS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "Evaluation questions must "
            "be stored as a list."
        )

    return data


# ============================================================
# LOAD VECTOR DATABASE
# ============================================================

def load_collection():

    if not VECTOR_DB_DIR.exists():
        raise FileNotFoundError(
            f"Vector database not found:\n"
            f"{VECTOR_DB_DIR}"
        )

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print(
        f"Model: {EMBEDDING_MODEL}"
    )

    return model


# ============================================================
# EXTRACT QUESTION
# ============================================================

def extract_question(
    item: dict[str, Any],
) -> str:

    for key in (
        "question",
        "query",
        "text",
    ):

        value = item.get(key)

        if value:
            return str(value).strip()

    return ""


# ============================================================
# EXTRACT EXPECTED DOCUMENT
# ============================================================

def extract_expected_doc_id(
    item: dict[str, Any],
) -> str | None:

    for key in (
        "expected_doc_id",
        "expected_document_id",
    ):

        value = item.get(key)

        if value is not None:
            return str(value)

    expected = item.get(
        "expected"
    )

    if isinstance(expected, dict):

        for key in (
            "doc_id",
            "document_id",
            "expected_doc_id",
            "expected_document_id",
        ):

            value = expected.get(key)

            if value is not None:
                return str(value)

    metadata = item.get(
        "metadata"
    )

    if isinstance(metadata, dict):

        for key in (
            "doc_id",
            "document_id",
            "expected_doc_id",
            "expected_document_id",
        ):

            value = metadata.get(key)

            if value is not None:
                return str(value)

    return None


# ============================================================
# QUERY REWRITING
# ============================================================

def generate_queries(
    original_question: str,
) -> list[str]:
    """
    Generate deterministic query variants.

    We intentionally avoid an external LLM here.
    The experiment must be reproducible.

    Query 1 = original query.
    Query 2 = keyword-focused version.
    Query 3 = semantic paraphrase.
    """

    original = (
        original_question.strip()
    )

    query_1 = original

    query_2 = (
        f"key information about "
        f"{original}"
    )

    query_3 = (
        f"policy and details related to "
        f"{original}"
    )

    queries = [
        query_1,
        query_2,
        query_3,
    ]

    return queries[
        :MULTI_QUERY_COUNT
    ]


# ============================================================
# VECTOR SEARCH
# ============================================================

def search_query(
    collection,
    model,
    query: str,
) -> list[dict[str, Any]]:

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )[0]

    result = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=CANDIDATES_PER_QUERY,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = result.get(
        "documents",
        [[]],
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]],
    )[0]

    distances = result.get(
        "distances",
        [[]],
    )[0]

    candidates = []

    for index, metadata in enumerate(metadatas):

        if not metadata:
            continue

        # Day-09 stores:
        # document_001_chunk_000

        chunk_id = metadata.get(
            "chunk_id"
        )

        # Try normal document ID first.
        doc_id = metadata.get(
            "doc_id"
        )

        if doc_id is None:
            doc_id = metadata.get(
                "document_id"
            )

        # FIX:
        # Derive document ID from chunk ID.
        if (
            doc_id is None
            and chunk_id is not None
        ):
            chunk_id = str(chunk_id)

            if "_chunk_" in chunk_id:
                doc_id = chunk_id.split(
                    "_chunk_",
                    1,
                )[0]

        if doc_id is None:
            continue

        distance = None

        if index < len(distances):
            distance = distances[index]

        document = ""

        if index < len(documents):
            document = documents[index]

        candidates.append(
            {
                "doc_id": str(doc_id),
                "chunk_id": chunk_id,
                "distance": distance,
                "document": document,
                "query": query,
            }
        )

    return candidates


# ============================================================
# DEDUPLICATE CANDIDATES
# ============================================================

def deduplicate_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove duplicate chunks.

    Same chunk_id = same candidate.
    """

    unique = {}

    for candidate in candidates:

        chunk_id = candidate.get(
            "chunk_id"
        )

        if chunk_id is None:

            chunk_id = (
                candidate["doc_id"]
                + "::"
                + candidate["document"]
            )

        if chunk_id not in unique:

            unique[chunk_id] = candidate

        else:

            existing = unique[
                chunk_id
            ]

            existing_distance = (
                existing.get("distance")
            )

            new_distance = (
                candidate.get("distance")
            )

            if (
                new_distance is not None
                and (
                    existing_distance is None
                    or new_distance
                    < existing_distance
                )
            ):

                unique[chunk_id] = candidate

    return list(
        unique.values()
    )


# ============================================================
# RANK CANDIDATES
# ============================================================

def rank_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Chroma distance is lower when the
    candidate is more similar.

    Therefore sort by ascending distance.
    """

    ranked = sorted(
        candidates,
        key=lambda item: (
            item.get("distance")
            if item.get("distance")
            is not None
            else float("inf")
        ),
    )

    return ranked[
        :TOP_K
    ]


# ============================================================
# SINGLE QUERY RETRIEVAL
# ============================================================

def baseline_retrieve(
    collection,
    model,
    question: str,
) -> list[dict[str, Any]]:

    return search_query(
        collection=collection,
        model=model,
        query=question,
    )


# ============================================================
# MULTI QUERY RETRIEVAL
# ============================================================

def multi_query_retrieve(
    collection,
    model,
    question: str,
) -> dict[str, Any]:

    queries = generate_queries(
        question
    )

    all_candidates = []

    query_results = []

    for query in queries:

        candidates = search_query(
            collection=collection,
            model=model,
            query=query,
        )

        query_results.append(
            {
                "query": query,
                "candidates": candidates,
            }
        )

        all_candidates.extend(
            candidates
        )

    unique_candidates = (
        deduplicate_candidates(
            all_candidates
        )
    )

    ranked_candidates = (
        rank_candidates(
            unique_candidates
        )
    )

    return {
        "queries": queries,
        "query_results": query_results,
        "candidate_count_before_dedup": (
            len(all_candidates)
        ),
        "candidate_count_after_dedup": (
            len(unique_candidates)
        ),
        "final_candidates": (
            ranked_candidates
        ),
    }


# ============================================================
# FIND EXPECTED RANK
# ============================================================

def find_expected_rank(
    candidates: list[dict[str, Any]],
    expected_doc_id: str,
) -> int | None:

    for rank, candidate in enumerate(
        candidates,
        start=1,
    ):

        if (
            candidate["doc_id"]
            == str(expected_doc_id)
        ):

            return rank

    return None


# ============================================================
# EVALUATE
# ============================================================

def evaluate(
    collection,
    model,
    questions,
    use_multi_query: bool,
):

    results = []

    hits = 0
    top1_hits = 0
    reciprocal_rank_sum = 0.0

    total_latency = 0.0

    for number, item in enumerate(
        questions,
        start=1,
    ):

        question = extract_question(
            item
        )

        expected_doc_id = (
            extract_expected_doc_id(
                item
            )
        )

        if (
            not question
            or expected_doc_id is None
        ):
            continue

        start = time.perf_counter()

        if use_multi_query:

            retrieval = (
                multi_query_retrieve(
                    collection=collection,
                    model=model,
                    question=question,
                )
            )

            candidates = (
                retrieval[
                    "final_candidates"
                ]
            )

        else:

            candidates = (
                baseline_retrieve(
                    collection=collection,
                    model=model,
                    question=question,
                )
            )

            retrieval = {
                "queries": [
                    question
                ],
                "query_results": [],
                "candidate_count_before_dedup": (
                    len(candidates)
                ),
                "candidate_count_after_dedup": (
                    len(candidates)
                ),
                "final_candidates": (
                    candidates
                ),
            }

        latency_ms = (
            time.perf_counter()
            - start
        ) * 1000

        total_latency += latency_ms

        expected_rank = (
            find_expected_rank(
                candidates,
                expected_doc_id,
            )
        )

        hit = (
            expected_rank is not None
        )

        if hit:

            hits += 1

            reciprocal_rank_sum += (
                1 / expected_rank
            )

            if expected_rank == 1:
                top1_hits += 1

        retrieved_doc_ids = [
            candidate["doc_id"]
            for candidate in candidates
        ]

        results.append(
            {
                "question_number": number,
                "question": question,
                "expected_doc_id": (
                    expected_doc_id
                ),
                "queries": retrieval[
                    "queries"
                ],
                "candidate_count_before_dedup": (
                    retrieval[
                        "candidate_count_before_dedup"
                    ]
                ),
                "candidate_count_after_dedup": (
                    retrieval[
                        "candidate_count_after_dedup"
                    ]
                ),
                "retrieved_doc_ids": (
                    retrieved_doc_ids
                ),
                "expected_rank": (
                    expected_rank
                ),
                "hit": hit,
                "latency_ms": round(
                    latency_ms,
                    3,
                ),
                "final_candidates": (
                    candidates
                ),
            }
        )

        print(
            f"{number:02d}. "
            f"{'PASS' if hit else 'FAIL'} "
            f"| Rank={expected_rank}"
        )

    total = len(results)

    recall = (
        hits / total
        if total
        else 0.0
    )

    top1 = (
        top1_hits / total
        if total
        else 0.0
    )

    mrr = (
        reciprocal_rank_sum / total
        if total
        else 0.0
    )

    average_latency = (
        total_latency / total
        if total
        else 0.0
    )

    metrics = {
        "total_questions": total,
        "retrieval_recall": round(
            recall,
            4,
        ),
        "top1_accuracy": round(
            top1,
            4,
        ),
        "mrr": round(
            mrr,
            4,
        ),
        "average_latency_ms": round(
            average_latency,
            3,
        ),
    }

    return {
        "metrics": metrics,
        "results": results,
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

    print(
        "\nLoading evaluation questions..."
    )

    questions = load_questions()

    print(
        f"Questions loaded: "
        f"{len(questions)}"
    )

    model = load_model()

    print(
        "\nConnecting to ChromaDB..."
    )

    collection = load_collection()

    print(
        f"Collection: "
        f"{COLLECTION_NAME}"
    )

    print(
        f"Vectors: "
        f"{collection.count()}"
    )

    # --------------------------------------------------------
    # BASELINE
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "BASELINE SINGLE-QUERY RETRIEVAL"
    )
    print("=" * 70)

    baseline = evaluate(
        collection=collection,
        model=model,
        questions=questions,
        use_multi_query=False,
    )

    print()
    print(
        json.dumps(
            baseline["metrics"],
            indent=2,
        )
    )

    # --------------------------------------------------------
    # MULTI QUERY
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "MULTI-QUERY RETRIEVAL"
    )
    print("=" * 70)

    multi_query = evaluate(
        collection=collection,
        model=model,
        questions=questions,
        use_multi_query=True,
    )

    print()
    print(
        json.dumps(
            multi_query["metrics"],
            indent=2,
        )
    )

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    baseline_metrics = (
        baseline["metrics"]
    )

    multi_metrics = (
        multi_query["metrics"]
    )

    comparison = {
        "recall_change": round(
            multi_metrics[
                "retrieval_recall"
            ]
            - baseline_metrics[
                "retrieval_recall"
            ],
            4,
        ),
        "top1_change": round(
            multi_metrics[
                "top1_accuracy"
            ]
            - baseline_metrics[
                "top1_accuracy"
            ],
            4,
        ),
        "mrr_change": round(
            multi_metrics[
                "mrr"
            ]
            - baseline_metrics[
                "mrr"
            ],
            4,
        ),
        "latency_change_ms": round(
            multi_metrics[
                "average_latency_ms"
            ]
            - baseline_metrics[
                "average_latency_ms"
            ],
            3,
        ),
    }

    print()
    print("=" * 70)
    print(
        "TASK 2 COMPARISON"
    )
    print("=" * 70)

    print(
        f"Baseline Recall : "
        f"{baseline_metrics['retrieval_recall']}"
    )

    print(
        f"Multi-query Recall : "
        f"{multi_metrics['retrieval_recall']}"
    )

    print(
        f"Recall Change : "
        f"{comparison['recall_change']:+.4f}"
    )

    print()

    print(
        f"Baseline Top-1 : "
        f"{baseline_metrics['top1_accuracy']}"
    )

    print(
        f"Multi-query Top-1 : "
        f"{multi_metrics['top1_accuracy']}"
    )

    print(
        f"Top-1 Change : "
        f"{comparison['top1_change']:+.4f}"
    )

    print()

    print(
        f"Baseline MRR : "
        f"{baseline_metrics['mrr']}"
    )

    print(
        f"Multi-query MRR : "
        f"{multi_metrics['mrr']}"
    )

    print(
        f"MRR Change : "
        f"{comparison['mrr_change']:+.4f}"
    )

    print()

    print(
        f"Baseline Latency : "
        f"{baseline_metrics['average_latency_ms']} ms"
    )

    print(
        f"Multi-query Latency : "
        f"{multi_metrics['average_latency_ms']} ms"
    )

    print(
        f"Latency Change : "
        f"{comparison['latency_change_ms']:+.3f} ms"
    )

    # --------------------------------------------------------
    # DECISION
    # --------------------------------------------------------

    if (
        comparison["recall_change"] > 0
        and comparison["mrr_change"] >= 0
    ):

        decision = "ACCEPT"

    else:

        decision = "REJECT"

    print()
    print(
        f"Decision: {decision}"
    )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    output = {
        "task": "day10_task2",
        "experiment": (
            "multi_query_retrieval"
        ),
        "configuration": {
            "embedding_model": (
                EMBEDDING_MODEL
            ),
            "top_k": TOP_K,
            "candidates_per_query": (
                CANDIDATES_PER_QUERY
            ),
            "multi_query_count": (
                MULTI_QUERY_COUNT
            ),
        },
        "baseline": baseline,
        "multi_query": multi_query,
        "comparison": comparison,
        "decision": decision,
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
        f"Results saved to:\n"
        f"{OUTPUT_FILE}"
    )

    print()
    print("=" * 70)
    print(
        "DAY 10 TASK 2 COMPLETE"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()