import json

import chromadb
from sentence_transformers import SentenceTransformer


QUESTIONS_FILE = "data/retrieval_questions.json"
VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "d5_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 3


def main():
    print("=" * 60)
    print("DAY 06 - RETRIEVAL EVALUATION")
    print("=" * 60)

    # Load questions
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    print(f"Evaluation questions: {len(questions)}")

    # Load model
    model = SentenceTransformer(MODEL_NAME)

    # Load vector database
    client = chromadb.PersistentClient(
        path=VECTOR_DB_PATH
    )

    collection = client.get_collection(
        COLLECTION_NAME
    )

    top1_correct = 0
    top3_correct = 0

    print("\nRunning evaluation...\n")

    for number, item in enumerate(questions, start=1):
        question = item["question"]
        expected_doc = item["expected_doc_id"]

        query_embedding = model.encode(
            question,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        results = collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=TOP_K,
        )

        retrieved_docs = [
            metadata["doc_id"]
            for metadata in results["metadatas"][0]
        ]

        top1_match = (
            retrieved_docs[0] == expected_doc
        )

        top3_match = (
            expected_doc in retrieved_docs
        )

        if top1_match:
            top1_correct += 1

        if top3_match:
            top3_correct += 1

        status = "PASS" if top3_match else "FAIL"

        print(
            f"{number:02d}. {status} | "
            f"Expected: {expected_doc} | "
            f"Retrieved: {retrieved_docs}"
        )

    total = len(questions)

    top1_accuracy = (
        top1_correct / total * 100
    )

    top3_accuracy = (
        top3_correct / total * 100
    )

    print("\n" + "=" * 60)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Total questions: {total}")
    print(f"Top-1 correct: {top1_correct}/{total}")
    print(f"Top-1 accuracy: {top1_accuracy:.2f}%")
    print(f"Top-3 correct: {top3_correct}/{total}")
    print(f"Top-3 accuracy: {top3_accuracy:.2f}%")

    print("\nEvaluation completed.")


if __name__ == "__main__":
    main()