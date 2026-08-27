import json
import time
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DAY6_ROOT = PROJECT_ROOT.parent / "d5-6 genai assistant"

DAY6_VECTOR_DB = (
    DAY6_ROOT
    / "outputs"
    / "chroma_db"
)

DAY6_QUESTIONS_FILE = (
    DAY6_ROOT
    / "data"
    / "retrieval_questions.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "day10"
    / "task3"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "reranking_results.json"
)


# ============================================================
# CHROMADB CONFIGURATION
# ============================================================

COLLECTION_NAME = "genai_documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# RERANKER CONFIGURATION
# ============================================================

RERANKER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ============================================================
# RETRIEVAL CONFIGURATION
# ============================================================

CANDIDATE_TOP_K = 10

FINAL_TOP_K = 5


# ============================================================
# JSON HELPERS
# ============================================================

def load_json(path: Path):

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_json(
    path: Path,
    data
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# LOAD EVALUATION QUESTIONS
# ============================================================

def load_questions():

    if not DAY6_QUESTIONS_FILE.exists():

        raise FileNotFoundError(
            "Evaluation question file not found:\n"
            f"{DAY6_QUESTIONS_FILE}"
        )

    data = load_json(
        DAY6_QUESTIONS_FILE
    )

    if isinstance(data, list):

        return data

    if isinstance(data, dict):

        for key in [
            "questions",
            "evaluation_questions",
            "data"
        ]:

            if key in data:

                return data[key]

    raise ValueError(
        "Unsupported evaluation question format."
    )


# ============================================================
# QUESTION TEXT
# ============================================================

def get_question_text(question):

    for key in [
        "question",
        "query",
        "text"
    ]:

        value = question.get(key)

        if value is not None:

            return str(value).strip()

    return ""


# ============================================================
# EXPECTED DOCUMENT ID
# ============================================================

def get_expected_doc_id(question):

    # Direct fields
    for key in [
        "expected_doc_id",
        "expected_document_id",
        "doc_id",
        "document_id"
    ]:

        value = question.get(key)

        if value is not None:

            return normalize_doc_id(value)

    # Nested expected object
    expected = question.get(
        "expected"
    )

    if isinstance(
        expected,
        dict
    ):

        for key in [
            "expected_doc_id",
            "expected_document_id",
            "doc_id",
            "document_id"
        ]:

            value = expected.get(key)

            if value is not None:

                return normalize_doc_id(value)

    # Nested metadata
    metadata = question.get(
        "metadata"
    )

    if isinstance(
        metadata,
        dict
    ):

        for key in [
            "expected_doc_id",
            "expected_document_id",
            "doc_id",
            "document_id"
        ]:

            value = metadata.get(key)

            if value is not None:

                return normalize_doc_id(value)

    return None


# ============================================================
# NORMALIZE DOCUMENT ID
# ============================================================

def normalize_doc_id(value):

    if value is None:

        return None

    doc_id = str(
        value
    ).strip()

    if not doc_id:

        return None

    # 001 -> document_001
    if doc_id.isdigit():

        return (
            f"document_{int(doc_id):03d}"
        )

    # DOC-001 -> document_001
    if doc_id.lower().startswith(
        "doc-"
    ):

        number = doc_id.split(
            "-"
        )[-1]

        if number.isdigit():

            return (
                f"document_{int(number):03d}"
            )

    # document 001 -> document_001
    if doc_id.lower().startswith(
        "document "
    ):

        number = doc_id.split()[-1]

        if number.isdigit():

            return (
                f"document_{int(number):03d}"
            )

    return doc_id


# ============================================================
# EXTRACT DOC ID FROM CHUNK ID
# ============================================================

def doc_id_from_chunk_id(
    chunk_id
):

    if chunk_id is None:

        return None

    chunk_id = str(
        chunk_id
    ).strip()

    # Example:
    #
    # document_001_chunk_000
    #
    # becomes:
    #
    # document_001

    if "_chunk_" in chunk_id:

        return (
            chunk_id
            .split(
                "_chunk_",
                1
            )[0]
        )

    return None


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

def load_embedding_model():

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
# LOAD RERANKER
# ============================================================

def load_reranker():

    print(
        "\nLoading reranker..."
    )

    reranker = CrossEncoder(
        RERANKER_MODEL
    )

    print(
        f"Reranker: {RERANKER_MODEL}"
    )

    return reranker


# ============================================================
# LOAD CHROMADB
# ============================================================

def load_collection():

    print(
        "\nConnecting to ChromaDB..."
    )

    if not DAY6_VECTOR_DB.exists():

        raise FileNotFoundError(
            "ChromaDB not found:\n"
            f"{DAY6_VECTOR_DB}"
        )

    client = chromadb.PersistentClient(
        path=str(DAY6_VECTOR_DB)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    print(
        f"Collection: {COLLECTION_NAME}"
    )

    print(
        f"Vectors: {collection.count()}"
    )

    return collection


# ============================================================
# VECTOR RETRIEVAL
# ============================================================

def retrieve_candidates(
    question,
    model,
    collection,
    top_k=CANDIDATE_TOP_K
):

    # --------------------------------------------------------
    # Create query embedding
    # --------------------------------------------------------

    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )[0].tolist()

    # --------------------------------------------------------
    # Query ChromaDB
    # --------------------------------------------------------

    search_result = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = search_result.get(
        "documents",
        [[]]
    )[0]

    metadatas = search_result.get(
        "metadatas",
        [[]]
    )[0]

    distances = search_result.get(
        "distances",
        [[]]
    )[0]

    candidates = []

    # --------------------------------------------------------
    # Build candidate records
    # --------------------------------------------------------

    for index in range(
        len(documents)
    ):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        if not isinstance(
            metadata,
            dict
        ):

            metadata = {}

        # ----------------------------------------------------
        # IMPORTANT:
        # Actual Chroma metadata contains chunk_id.
        #
        # Example:
        # document_001_chunk_000
        #
        # We derive:
        # document_001
        # ----------------------------------------------------

        chunk_id = metadata.get(
            "chunk_id"
        )

        doc_id = metadata.get(
            "doc_id"
        )

        if doc_id is None:

            doc_id = metadata.get(
                "document_id"
            )

        if doc_id is None:

            doc_id = doc_id_from_chunk_id(
                chunk_id
            )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        candidates.append(
            {
                # Original vector retrieval order
                "original_rank":
                    index + 1,

                # Original document ID
                "doc_id":
                    str(doc_id)
                    if doc_id is not None
                    else None,

                # Original chunk ID
                "chunk_id":
                    str(chunk_id)
                    if chunk_id is not None
                    else None,

                # IMPORTANT:
                # Preserve original vector distance
                "original_distance":
                    distance,

                # Candidate text
                "text":
                    documents[index]
            }
        )

    return candidates


# ============================================================
# RERANK CANDIDATES
# ============================================================

def rerank_candidates(
    question,
    candidates,
    reranker
):

    if not candidates:

        return []

    # --------------------------------------------------------
    # Create question/document pairs
    # --------------------------------------------------------

    pairs = []

    for candidate in candidates:

        pairs.append(
            [
                question,
                candidate["text"]
            ]
        )

    # --------------------------------------------------------
    # Calculate reranker scores
    # --------------------------------------------------------

    scores = reranker.predict(
        pairs
    )

    reranked = []

    for candidate, score in zip(
        candidates,
        scores
    ):

        result = dict(
            candidate
        )

        # New reranker score
        result[
            "reranker_score"
        ] = float(score)

        reranked.append(
            result
        )

    # --------------------------------------------------------
    # Sort by reranker score
    #
    # Higher CrossEncoder score
    # = better relevance
    # --------------------------------------------------------

    reranked.sort(
        key=lambda item:
            item["reranker_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # Preserve final selected order
    # --------------------------------------------------------

    for rank, result in enumerate(
        reranked,
        start=1
    ):

        result[
            "final_rank"
        ] = rank

    return reranked


# ============================================================
# RUN TASK 3
# ============================================================

def run_reranking(
    questions,
    embedding_model,
    collection,
    reranker
):

    results = []

    for number, question_data in enumerate(
        questions,
        start=1
    ):

        question = get_question_text(
            question_data
        )

        expected_doc_id = (
            get_expected_doc_id(
                question_data
            )
        )

        start_time = (
            time.perf_counter()
        )

        # ----------------------------------------------------
        # STEP 1
        # Vector retrieval
        # ----------------------------------------------------

        candidates = retrieve_candidates(
            question,
            embedding_model,
            collection,
            CANDIDATE_TOP_K
        )

        # ----------------------------------------------------
        # STEP 2
        # Reranking
        # ----------------------------------------------------

        reranked = rerank_candidates(
            question,
            candidates,
            reranker
        )

        # ----------------------------------------------------
        # STEP 3
        # Final Top-K
        # ----------------------------------------------------

        final_results = reranked[
            :FINAL_TOP_K
        ]

        # ----------------------------------------------------
        # Latency
        # ----------------------------------------------------

        latency_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        # ----------------------------------------------------
        # Final document IDs
        # ----------------------------------------------------

        retrieved_doc_ids = []

        for result in final_results:

            doc_id = result.get(
                "doc_id"
            )

            if doc_id is not None:

                retrieved_doc_ids.append(
                    str(doc_id)
                )

        # ----------------------------------------------------
        # Find expected document rank
        # ----------------------------------------------------

        expected_rank = None

        if expected_doc_id is not None:

            for rank, doc_id in enumerate(
                retrieved_doc_ids,
                start=1
            ):

                if (
                    str(doc_id)
                    == str(expected_doc_id)
                ):

                    expected_rank = rank

                    break

        hit = (
            expected_rank is not None
        )

        # ----------------------------------------------------
        # Print result
        # ----------------------------------------------------

        print(
            f"{number:02d}. "
            f"{'PASS' if hit else 'FAIL'} "
            f"| Rank={expected_rank}"
        )

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        results.append(
            {
                "question_number":
                    number,

                "question":
                    question,

                "expected_doc_id":
                    expected_doc_id,

                "retrieved_doc_ids":
                    retrieved_doc_ids,

                "expected_rank":
                    expected_rank,

                "hit":
                    hit,

                "latency_ms":
                    round(
                        latency_ms,
                        3
                    ),

                # ALL candidates after reranking
                #
                # Contains:
                # original_rank
                # original_distance
                # reranker_score
                # final_rank
                "candidate_results":
                    reranked,

                # Final selected Top-K
                "final_results":
                    final_results
            }
        )

    return results


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(
    results
):

    total = len(results)

    if total == 0:

        return {
            "total_questions": 0,
            "retrieval_recall": 0.0,
            "top1_accuracy": 0.0,
            "mrr": 0.0,
            "average_latency_ms": 0.0
        }

    recall_hits = 0

    top1_hits = 0

    reciprocal_rank_sum = 0.0

    latency_sum = 0.0

    for result in results:

        rank = result[
            "expected_rank"
        ]

        if rank is not None:

            recall_hits += 1

            reciprocal_rank_sum += (
                1.0 / rank
            )

            if rank == 1:

                top1_hits += 1

        latency_sum += result[
            "latency_ms"
        ]

    return {
        "total_questions":
            total,

        "retrieval_recall":
            round(
                recall_hits / total,
                4
            ),

        "top1_accuracy":
            round(
                top1_hits / total,
                4
            ),

        "mrr":
            round(
                reciprocal_rank_sum / total,
                4
            ),

        "average_latency_ms":
            round(
                latency_sum / total,
                3
            )
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "DAY 10 - TASK 3"
    )

    print(
        "RERANKING EXPERIMENT"
    )

    print("=" * 70)

    # ========================================================
    # LOAD QUESTIONS
    # ========================================================

    print(
        "\nLoading evaluation questions..."
    )

    questions = load_questions()

    print(
        f"Questions loaded: "
        f"{len(questions)}"
    )

    # ========================================================
    # LOAD EMBEDDING MODEL
    # ========================================================

    embedding_model = (
        load_embedding_model()
    )

    # ========================================================
    # LOAD RERANKER
    # ========================================================

    reranker = load_reranker()

    # ========================================================
    # LOAD CHROMADB
    # ========================================================

    collection = load_collection()

    # ========================================================
    # CONFIGURATION
    # ========================================================

    print()

    print("=" * 70)

    print(
        "RERANKING CONFIGURATION"
    )

    print("=" * 70)

    print(
        f"Embedding model : "
        f"{EMBEDDING_MODEL}"
    )

    print(
        f"Candidate Top-K : "
        f"{CANDIDATE_TOP_K}"
    )

    print(
        f"Final Top-K     : "
        f"{FINAL_TOP_K}"
    )

    print(
        f"Reranker        : "
        f"{RERANKER_MODEL}"
    )

    # ========================================================
    # RUN EXPERIMENT
    # ========================================================

    print()

    print("=" * 70)

    print(
        "RERANKED RETRIEVAL"
    )

    print("=" * 70)

    results = run_reranking(
        questions,
        embedding_model,
        collection,
        reranker
    )

    # ========================================================
    # CALCULATE METRICS
    # ========================================================

    metrics = calculate_metrics(
        results
    )

    print()

    print("=" * 70)

    print(
        "TASK 3 METRICS"
    )

    print("=" * 70)

    print(
        json.dumps(
            metrics,
            indent=2
        )
    )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    output = {

        "day": 10,

        "task": 3,

        "experiment":
            "reranking",

        "configuration": {

            "embedding_model":
                EMBEDDING_MODEL,

            "candidate_top_k":
                CANDIDATE_TOP_K,

            "final_top_k":
                FINAL_TOP_K,

            "reranker_model":
                RERANKER_MODEL
        },

        "metrics":
            metrics,

        "results":
            results
    }

    save_json(
        OUTPUT_FILE,
        output
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
        "DAY 10 TASK 3 COMPLETE"
    )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()