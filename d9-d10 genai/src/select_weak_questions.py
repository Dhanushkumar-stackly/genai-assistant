import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Existing Day 6 + Day 8 project
SOURCE_ROOT = (
    PROJECT_ROOT.parent
    / "d5-6 genai assistant"
)


# ============================================================
# DAY 6 CONFIGURATION
# ============================================================

DAY6_QUESTIONS_FILE = (
    SOURCE_ROOT
    / "data"
    / "retrieval_questions.json"
)

DAY6_VECTOR_DB = (
    SOURCE_ROOT
    / "vector_db"
)

DAY6_COLLECTION = "d5_chunks"


# ============================================================
# DAY 8 CONFIGURATION
# ============================================================

DAY8_VECTOR_DB = (
    SOURCE_ROOT
    / "outputs"
    / "chroma_db"
)

DAY8_COLLECTION = "genai_documents"


# ============================================================
# OUTPUT FILES
# ============================================================

DAY6_RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "day6_results.json"
)

DAY8_RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "day8_results.json"
)

WEAK_QUESTIONS_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "weak_questions.json"
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# Day 6 baseline
DAY6_TOP_K = 3

# Day 8 baseline
DAY8_TOP_K = 5


# ============================================================
# VALIDATE SOURCE DATA
# ============================================================

def validate_source_data():

    print("=" * 70)
    print("VALIDATING DAY 6 / DAY 8 SOURCE DATA")
    print("=" * 70)

    print(
        f"Source root:\n{SOURCE_ROOT}"
    )

    print(
        f"\nQuestions file:\n"
        f"{DAY6_QUESTIONS_FILE}"
    )

    print(
        f"Exists: "
        f"{DAY6_QUESTIONS_FILE.exists()}"
    )

    print(
        f"\nDay 6 vector DB:\n"
        f"{DAY6_VECTOR_DB}"
    )

    print(
        f"Exists: "
        f"{DAY6_VECTOR_DB.exists()}"
    )

    print(
        f"\nDay 8 vector DB:\n"
        f"{DAY8_VECTOR_DB}"
    )

    print(
        f"Exists: "
        f"{DAY8_VECTOR_DB.exists()}"
    )

    if not DAY6_QUESTIONS_FILE.exists():

        raise FileNotFoundError(
            "Day 6 retrieval_questions.json "
            "was not found."
        )

    if not DAY6_VECTOR_DB.exists():

        raise FileNotFoundError(
            "Day 6 vector_db was not found."
        )

    if not DAY8_VECTOR_DB.exists():

        raise FileNotFoundError(
            "Day 8 outputs/chroma_db "
            "was not found."
        )

    print(
        "\nSource validation PASSED."
    )


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_questions():

    with open(
        DAY6_QUESTIONS_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        questions = json.load(file)

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "retrieval_questions.json "
            "must contain a list."
        )

    print(
        f"\nTotal evaluation questions: "
        f"{len(questions)}"
    )

    return questions


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

def load_model():

    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print(
        f"Model loaded: "
        f"{EMBEDDING_MODEL}"
    )

    return model


# ============================================================
# DAY 6 RETRIEVAL
# ============================================================

def run_day6(
    questions,
    model,
):

    print("\n" + "=" * 70)
    print("DAY 06 RETRIEVAL")
    print("=" * 70)

    client = chromadb.PersistentClient(
        path=str(
            DAY6_VECTOR_DB
        )
    )

    collection = client.get_collection(
        name=DAY6_COLLECTION
    )

    print(
        f"Collection: "
        f"{DAY6_COLLECTION}"
    )

    print(
        f"Vectors: "
        f"{collection.count()}"
    )

    results = []

    for number, item in enumerate(
        questions,
        start=1,
    ):

        question = item["question"]

        expected_doc = (
            item["expected_doc_id"]
        )

        # ----------------------------------------------------
        # Create query embedding
        # ----------------------------------------------------

        query_embedding = model.encode(
            question,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        # ----------------------------------------------------
        # Search top 3
        # ----------------------------------------------------

        search_results = collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=DAY6_TOP_K,
            include=[
                "metadatas",
                "distances",
            ],
        )

        metadatas = (
            search_results[
                "metadatas"
            ][0]
        )

        distances = (
            search_results[
                "distances"
            ][0]
        )

        retrieved_docs = []

        for metadata in metadatas:

            doc_id = metadata.get(
                "doc_id"
            )

            retrieved_docs.append(
                doc_id
            )

        # ----------------------------------------------------
        # Find expected rank
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
        # Metrics
        # ----------------------------------------------------

        top1_hit = (
            expected_rank == 1
        )

        top3_hit = (
            expected_doc
            in retrieved_docs
        )

        result = {

            "question": question,

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

            "top3_hit":
                top3_hit,
        }

        results.append(result)

        status = (
            "PASS"
            if top3_hit
            else "FAIL"
        )

        print(
            f"{number:02d}. {status} | "
            f"Expected={expected_doc} | "
            f"Retrieved={retrieved_docs} | "
            f"Rank={expected_rank}"
        )

    return results


# ============================================================
# DAY 8 RETRIEVAL
# ============================================================

def run_day8(
    questions,
    model,
):

    print("\n" + "=" * 70)
    print("DAY 08 RETRIEVAL")
    print("=" * 70)

    client = chromadb.PersistentClient(
        path=str(
            DAY8_VECTOR_DB
        )
    )

    collection = client.get_collection(
        name=DAY8_COLLECTION
    )

    print(
        f"Collection: "
        f"{DAY8_COLLECTION}"
    )

    print(
        f"Vectors: "
        f"{collection.count()}"
    )

    results = []

    for number, item in enumerate(
        questions,
        start=1,
    ):

        question = item["question"]

        expected_doc = (
            item["expected_doc_id"]
        )

        # ----------------------------------------------------
        # Create query embedding
        # ----------------------------------------------------

        query_embedding = model.encode(
            question,
            convert_to_numpy=True,
        )

        # ----------------------------------------------------
        # Search top 5
        # ----------------------------------------------------

        search_results = collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=DAY8_TOP_K,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = (
            search_results[
                "documents"
            ][0]
        )

        metadatas = (
            search_results[
                "metadatas"
            ][0]
        )

        distances = (
            search_results[
                "distances"
            ][0]
        )

        retrieved_docs = []

        for metadata in metadatas:

            doc_id = metadata.get(
                "doc_id"
            )

            retrieved_docs.append(
                doc_id
            )

        # ----------------------------------------------------
        # Expected source rank
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
        # Context check
        # ----------------------------------------------------

        has_context = any(
            isinstance(
                document,
                str,
            )
            and document.strip()
            for document in documents
        )

        # ----------------------------------------------------
        # Retrieval status
        # ----------------------------------------------------

        if has_context:

            status = "context_available"

        else:

            status = "no_context"

        result = {

            "question": question,

            "expected_doc_id":
                expected_doc,

            "retrieved_doc_ids":
                retrieved_docs,

            "distances":
                distances,

            "expected_rank":
                expected_rank,

            "status":
                status,

            "has_context":
                has_context,
        }

        results.append(result)

        print(
            f"{number:02d}. "
            f"Expected={expected_doc} | "
            f"Retrieved={retrieved_docs} | "
            f"Rank={expected_rank} | "
            f"Context={has_context}"
        )

    return results


# ============================================================
# FAILURE ANALYSIS
# ============================================================

def analyse_failure(
    day6,
    day8,
):

    expected_doc = (
        day6["expected_doc_id"]
    )

    score = 0

    reasons = []

    # ========================================================
    # FAILURE 1
    # Missing source
    # ========================================================

    if (
        expected_doc
        not in day6["retrieved_doc_ids"]
    ):

        score += 5

        reasons.append(
            "missing_source"
        )

    # ========================================================
    # FAILURE 2
    # Wrong ranking
    # ========================================================

    else:

        rank = (
            day6["expected_rank"]
        )

        if rank == 2:

            score += 2

            reasons.append(
                "wrong_ranking"
            )

        elif rank == 3:

            score += 3

            reasons.append(
                "low_ranking"
            )

    # ========================================================
    # DAY 8 MISSING SOURCE
    # ========================================================

    if (
        expected_doc
        not in day8["retrieved_doc_ids"]
    ):

        score += 5

        reasons.append(
            "day8_missing_source"
        )

    # ========================================================
    # DAY 8 WRONG RANK
    # ========================================================

    else:

        rank = (
            day8["expected_rank"]
        )

        if rank is not None and rank > 1:

            score += 2

            reasons.append(
                "day8_wrong_ranking"
            )

    # ========================================================
    # INCOMPLETE CONTEXT
    # ========================================================

    if not day8["has_context"]:

        score += 5

        reasons.append(
            "incomplete_context"
        )

    # ========================================================
    # UNNECESSARY ABSTENTION
    # ========================================================

    # Important:
    # We only call it unnecessary abstention
    # when expected source exists but no context
    # was considered available.

    if (
        day8["status"] == "no_context"
        and expected_doc
        in day8["retrieved_doc_ids"]
    ):

        score += 5

        reasons.append(
            "unnecessary_abstention"
        )

    return score, reasons


# ============================================================
# SELECT FIVE WEAKEST
# ============================================================

def select_five_weakest(
    day6_results,
    day8_results,
):

    day8_map = {
        item["question"]: item
        for item in day8_results
    }

    analysed = []

    for day6 in day6_results:

        question = (
            day6["question"]
        )

        day8 = (
            day8_map[question]
        )

        score, reasons = (
            analyse_failure(
                day6,
                day8,
            )
        )

        analysed.append(
            {

                "question":
                    question,

                "expected_doc_id":
                    day6[
                        "expected_doc_id"
                    ],

                "day6_retrieved":
                    day6[
                        "retrieved_doc_ids"
                    ],

                "day6_expected_rank":
                    day6[
                        "expected_rank"
                    ],

                "day6_distances":
                    day6[
                        "distances"
                    ],

                "day8_retrieved":
                    day8[
                        "retrieved_doc_ids"
                    ],

                "day8_expected_rank":
                    day8[
                        "expected_rank"
                    ],

                "day8_distances":
                    day8[
                        "distances"
                    ],

                "day8_status":
                    day8[
                        "status"
                    ],

                "failure_score":
                    score,

                "failure_reasons":
                    reasons,
            }
        )

    # --------------------------------------------------------
    # Weakest first
    # --------------------------------------------------------

    analysed.sort(
        key=lambda item: (
            -item["failure_score"],
            item["question"],
        )
    )

    return analysed[:5]


# ============================================================
# SAVE JSON
# ============================================================

def save_json(
    path,
    data,
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    validate_source_data()

    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    questions = load_questions()

    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    model = load_model()

    # --------------------------------------------------------
    # STEP 4
    # DAY 6
    # --------------------------------------------------------

    day6_results = run_day6(
        questions,
        model,
    )

    save_json(
        DAY6_RESULTS_FILE,
        day6_results,
    )

    print(
        f"\nDay 6 results saved to:\n"
        f"{DAY6_RESULTS_FILE}"
    )

    # --------------------------------------------------------
    # STEP 5
    # DAY 8
    # --------------------------------------------------------

    day8_results = run_day8(
        questions,
        model,
    )

    save_json(
        DAY8_RESULTS_FILE,
        day8_results,
    )

    print(
        f"\nDay 8 results saved to:\n"
        f"{DAY8_RESULTS_FILE}"
    )

    # --------------------------------------------------------
    # STEP 6
    # SELECT FIVE
    # --------------------------------------------------------

    weakest_questions = (
        select_five_weakest(
            day6_results,
            day8_results,
        )
    )

    # --------------------------------------------------------
    # STEP 7
    # SAVE
    # --------------------------------------------------------

    save_json(
        WEAK_QUESTIONS_FILE,
        weakest_questions,
    )

    # --------------------------------------------------------
    # STEP 8
    # DISPLAY
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DAY 09 - FIVE WEAKEST QUESTIONS")
    print("=" * 70)

    for index, item in enumerate(
        weakest_questions,
        start=1,
    ):

        print(
            f"\n#{index}"
        )

        print(
            f"Question:\n"
            f"{item['question']}"
        )

        print(
            f"Expected source: "
            f"{item['expected_doc_id']}"
        )

        print(
            f"Day 6 retrieved: "
            f"{item['day6_retrieved']}"
        )

        print(
            f"Day 6 expected rank: "
            f"{item['day6_expected_rank']}"
        )

        print(
            f"Day 8 retrieved: "
            f"{item['day8_retrieved']}"
        )

        print(
            f"Day 8 expected rank: "
            f"{item['day8_expected_rank']}"
        )

        print(
            f"Day 8 status: "
            f"{item['day8_status']}"
        )

        print(
            f"Failure score: "
            f"{item['failure_score']}"
        )

        print(
            f"Failure reasons: "
            f"{item['failure_reasons']}"
        )

        print("-" * 70)

    print(
        "\nTask 2 completed."
    )

    print(
        f"\nWeak questions saved to:\n"
        f"{WEAK_QUESTIONS_FILE}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()