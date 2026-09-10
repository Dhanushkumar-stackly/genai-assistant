import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


INPUT_FILE = "outputs/chunks.json"
OUTPUT_FILE = "outputs/embeddings.npz"

MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 32


def main():
    print("=" * 60)
    print("DAY 06 - EMBEDDING GENERATION")
    print("=" * 60)

    # Load Day 05 chunks
    print("\nStep 1: Loading Day 05 chunks...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    print(f"Loaded chunks: {len(chunks)}")

    if not chunks:
        raise ValueError("No chunks found in Day 05 output.")

    # Prepare texts
    texts = [chunk["text"] for chunk in chunks]

    print(f"Prepared texts: {len(texts)}")

    # Load embedding model
    print("\nStep 2: Loading embedding model...")
    print(f"Model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    # Generate embeddings in batches
    print("\nStep 3: Generating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    print(f"Embedding shape: {embeddings.shape}")

    # Save embeddings
    print("\nStep 4: Saving embeddings...")

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        output_path,
        embeddings=embeddings,
        chunk_ids=np.array(
            [chunk["chunk_id"] for chunk in chunks]
        ),
        model_name=np.array(MODEL_NAME),
        batch_size=np.array(BATCH_SIZE),
    )

    print(f"Saved: {OUTPUT_FILE}")
    print("\nEmbedding generation completed successfully.")


if __name__ == "__main__":
    main()