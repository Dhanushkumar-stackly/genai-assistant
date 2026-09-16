import chromadb
from sentence_transformers import SentenceTransformer


VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "d5_chunks"

MODEL_NAME = "all-MiniLM-L6-v2"


def semantic_search(query, top_k=3):
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(
        path=VECTOR_DB_PATH
    )

    collection = client.get_collection(
        COLLECTION_NAME
    )

    query_embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
    )

    return results


def main():
    query = input("Enter your question: ").strip()

    if not query:
        print("Question cannot be empty.")
        return

    results = semantic_search(
        query,
        top_k=3,
    )

    print("\n" + "=" * 60)
    print("SEMANTIC SEARCH RESULTS")
    print("=" * 60)

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]
    ids = results["ids"][0]

    for index, (
        chunk_id,
        document,
        distance,
        metadata,
    ) in enumerate(
        zip(
            ids,
            documents,
            distances,
            metadatas,
        ),
        start=1,
    ):
        print(f"\n--- Result {index} ---")

        print(f"Chunk ID: {chunk_id}")
        print(f"Distance: {distance}")
        print(f"Document ID: {metadata['doc_id']}")
        print(f"Title: {metadata['title']}")
        print(f"Source: {metadata['source_path']}")
        print(f"Chunk Index: {metadata['chunk_index']}")

        print("\nText:")
        print(document)


if __name__ == "__main__":
    main()