import json
from pathlib import Path

import chromadb
import numpy as np


CHUNKS_FILE = "outputs/chunks.json"
EMBEDDINGS_FILE = "outputs/embeddings.npz"

VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "d5_chunks"


def main():
    print("=" * 60)
    print("DAY 06 - VECTOR INDEX BUILD")
    print("=" * 60)

    # Load Day 05 chunks
    print("\nStep 1: Loading Day 05 chunks...")

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    print(f"Loaded chunks: {len(chunks)}")

    # Load embeddings
    print("\nStep 2: Loading embeddings...")

    data = np.load(EMBEDDINGS_FILE)

    embeddings = data["embeddings"]

    print(f"Loaded embeddings: {embeddings.shape}")

    # Safety check
    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunk count ({len(chunks)}) does not match "
            f"embedding count ({len(embeddings)})."
        )

    # Create Chroma client
    print("\nStep 3: Creating ChromaDB client...")

    client = chromadb.PersistentClient(
        path=VECTOR_DB_PATH
    )

    # Recreate collection
    print(f"Collection: {COLLECTION_NAME}")

    try:
        client.delete_collection(COLLECTION_NAME)
        print("Existing collection deleted.")
    except Exception:
        print("No existing collection found.")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={
            "embedding_model": "all-MiniLM-L6-v2",
            "source": "Day 05 chunks",
        },
    )

    # Prepare data
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])

        metadatas.append(
            {
                "doc_id": chunk["doc_id"],
                "title": chunk["title"],
                "source_path": chunk["source_path"],
                "updated_at": chunk["updated_at"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    # Add vectors
    print("\nStep 4: Adding vectors to index...")

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Indexed chunks: {collection.count()}")

    print("\nVector index created successfully.")
    print(f"Database: {VECTOR_DB_PATH}")
    print(f"Collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()