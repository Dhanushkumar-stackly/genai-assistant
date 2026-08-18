from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

COLLECTION_NAME = "d5_chunks"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_vector_collection():
    """Load the existing ChromaDB collection."""

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR)
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def load_embedding_model():
    """Load the embedding model."""

    model = SentenceTransformer(
        MODEL_NAME
    )

    return model


def retrieve(
    question,
    top_k=5
):
    """Retrieve the most relevant chunks for a question."""

    print(f"Question: {question}")

    model = load_embedding_model()

    collection = load_vector_collection()

    question_embedding = model.encode(
        [question]
    )

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=top_k
    )

    retrieved_chunks = []

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "score": distance
            }
        )

    return retrieved_chunks


if __name__ == "__main__":

    question = (
        "What are the responsibilities "
        "of team members?"
    )

    results = retrieve(
        question,
        top_k=5
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "=" * 60)

        print(
            f"Result {index}"
        )

        print(
            f"Score: {result['score']}"
        )

        print(
            f"Metadata: {result['metadata']}"
        )

        print(
            result["text"][:500]
        )