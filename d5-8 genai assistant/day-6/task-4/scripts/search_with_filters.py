import chromadb
from sentence_transformers import SentenceTransformer


VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "d5_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"


model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(
    path=VECTOR_DB_PATH
)

collection = client.get_collection(
    COLLECTION_NAME
)


def semantic_search(
    query,
    top_k=3,
    min_score=0.30,
    doc_id=None,
):
    query_embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    where_filter = None

    if doc_id:
        where_filter = {
            "doc_id": doc_id
        }

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
        where=where_filter,
    )

    output = []

    for chunk_id, document, distance, metadata in zip(
        results["ids"][0],
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0],
    ):
        # Chroma cosine distance -> similarity score
        score = 1 - distance

        if score >= min_score:
            output.append(
                {
                    "chunk_id": chunk_id,
                    "score": score,
                    "text": document,
                    "metadata": metadata,
                }
            )

    return output


def main():
    query = input("Enter your question: ").strip()

    results = semantic_search(
        query=query,
        top_k=3,
        min_score=0.30,
    )

    print("\n" + "=" * 60)
    print("FILTERED SEMANTIC SEARCH")
    print("=" * 60)

    if not results:
        print("No results passed the minimum score threshold.")
        return

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Score: {result['score']:.4f}")
        print(f"Document: {result['metadata']['doc_id']}")
        print(f"Title: {result['metadata']['title']}")
        print(f"Source: {result['metadata']['source_path']}")
        print(f"Chunk Index: {result['metadata']['chunk_index']}")

        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()