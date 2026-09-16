import json
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

D5_D6_ROOT = PROJECT_ROOT.parent / "d5-6 genai assistant"

WEAK_QUESTIONS_FILE = PROJECT_ROOT / "outputs" / "weak_questions.json"
QUESTIONS_FILE = D5_D6_ROOT / "data" / "retrieval_questions.json"
CHUNKS_FILE = D5_D6_ROOT / "outputs" / "chunks.json"

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
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize(text: str) -> str:
    """
    Normalize text for simple lexical comparison.
    """

    return " ".join(
        text.lower()
        .replace("?", "")
        .replace(",", "")
        .replace(".", "")
        .split()
    )


# ============================================================
# FIND QUESTION METADATA
# ============================================================

def find_question_metadata(question: str, questions: list):
    """
    Find the expected document ID for a weak question.
    """

    normalized_question = normalize(question)

    for item in questions:
        if normalize(item["question"]) == normalized_question:
            return item

    return None


# ============================================================
# FIND EXPECTED CHUNK
# ============================================================

def find_chunk(doc_id: str, chunks: list):
    """
    Find the chunk belonging to the expected document.
    """

    for chunk in chunks:
        if chunk.get("doc_id") == doc_id:
            return chunk

    return None


# ============================================================
# DIAGNOSE FAILURE
# ============================================================

def diagnose(question: str, metadata: dict | None, chunk: dict | None):
    """
    Produce a controlled diagnosis based on the available
    retrieval corpus metadata.
    """

    if metadata is None:
        return {
            "question": question,
            "expected_doc_id": None,
            "diagnosis": "Question metadata not found.",
            "evidence": "No matching question found in retrieval_questions.json.",
        }

    expected_doc_id = metadata["expected_doc_id"]

    if chunk is None:
        return {
            "question": question,
            "expected_doc_id": expected_doc_id,
            "diagnosis": "Missing expected document chunk.",
            "evidence": (
                f"No chunk was found for expected document "
                f"{expected_doc_id}."
            ),
        }

    text = chunk.get("text", "")

    if not text.strip():
        return {
            "question": question,
            "expected_doc_id": expected_doc_id,
            "diagnosis": "Empty chunk content.",
            "evidence": f"{expected_doc_id} exists but contains no text.",
        }

    return {
        "question": question,
        "expected_doc_id": expected_doc_id,
        "diagnosis": "Requires retrieval-ranking experiment.",
        "evidence": (
            f"Expected document {expected_doc_id} exists in the indexed "
            "corpus. The available corpus does not contain historical "
            "Day 6/Day 8 retrieval rankings, so ranking failure cannot "
            "be proven from these files alone."
        ),
    }


# ============================================================
# MAIN
# ============================================================

def main():

    weak_questions = load_json(WEAK_QUESTIONS_FILE)
    questions = load_json(QUESTIONS_FILE)
    chunks = load_json(CHUNKS_FILE)

    diagnoses = []

    for item in weak_questions:

        question = item["question"]

        metadata = find_question_metadata(
            question,
            questions,
        )

        if metadata is not None:
            chunk = find_chunk(
                metadata["expected_doc_id"],
                chunks,
            )
        else:
            chunk = None

        result = diagnose(
            question,
            metadata,
            chunk,
        )

        diagnoses.append(result)

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
            indent=4,
            ensure_ascii=False,
        )

    # ========================================================
    # DISPLAY
    # ========================================================

    print()
    print("=" * 70)
    print("RETRIEVAL FAILURE DIAGNOSIS")
    print("=" * 70)

    print(f"Weak questions diagnosed: {len(diagnoses)}")

    for index, result in enumerate(diagnoses, start=1):

        print()
        print(f"{index}. {result['question']}")
        print(
            f"   Expected document : "
            f"{result['expected_doc_id']}"
        )
        print(
            f"   Diagnosis         : "
            f"{result['diagnosis']}"
        )
        print(
            f"   Evidence          : "
            f"{result['evidence']}"
        )

    print()
    print("=" * 70)
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
