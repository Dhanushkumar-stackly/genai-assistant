import json
from pathlib import Path

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHUNKS_FILE = PROJECT_ROOT / "outputs" / "chunks.json"

CHROMA_DIR = PROJECT_ROOT / "outputs" / "chroma_db"

COLLECTION_NAME = "genai_documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# STEP 1: LOAD CHUNKS
# ============================================================

def load_chunks(chunks_file):
    print("\nStep 1: Loading Day 5 chunks...")

    with open(chunks_file, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No chunks found in chunks.json")

    print(f"Loaded chunks: {len(chunks)}")

    return chunks


# ============================================================
# STEP 2: PREPARE CHUNK DATA
# ============================================================

def prepare_chunk_data(chunks):
    print("\nStep 2: Preparing chunk data...")

    texts = []
    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        # ----------------------------------------------------
        # Handle different possible chunk structures
        # ----------------------------------------------------

        if isinstance(chunk, dict):

            # Text
            text = (
                chunk.get("text")
                or chunk.get("content")
                or chunk.get("chunk")
                or ""
            )

            # ID
            chunk_id = (
                chunk.get("id")
                or chunk.get("chunk_id")
                or f"chunk_{index:04d}"
            )

            # Metadata
            original_metadata = chunk.get("metadata", {})

            if not isinstance(original_metadata, dict):
                original_metadata = {}

        else:
            text = str(chunk)
            chunk_id = f"chunk_{index:04d}"
            original_metadata = {}

        # ----------------------------------------------------
        # Make sure text is valid
        # ----------------------------------------------------

        text = str(text).strip()

        if not text:
            print(f"Skipping empty chunk at index {index}")
            continue

        # ----------------------------------------------------
        # FIX: ChromaDB does NOT allow empty metadata {}
        # ----------------------------------------------------

        metadata = dict(original_metadata)

        # Add guaranteed metadata fields
        metadata["chunk_id"] = str(chunk_id)
        metadata["chunk_index"] = index

        # Convert metadata values into Chroma-compatible types
        for key, value in list(metadata.items()):

            if value is None:
                metadata[key] = ""

            elif isinstance(value, (str, int, float, bool)):
                pass

            else:
                metadata[key] = str(value)

        # ----------------------------------------------------
        # Store
        # ----------------------------------------------------

        ids.append(str(chunk_id))
        texts.append(text)
        metadatas.append(metadata)

    print(f"Prepared texts: {len(texts)}")
    print(f"Prepared IDs: {len(ids)}")
    print(f"Prepared metadata: {len(metadatas)}")

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not ids:
        raise ValueError("No valid chunks available.")

    if len(ids) != len(texts):
        raise ValueError("IDs and texts count mismatch.")

    if len(ids) != len(metadatas):
        raise ValueError("IDs and metadata count mismatch.")

    empty_metadata = [
        i for i, metadata in enumerate(metadatas)
        if not metadata
    ]

    if empty_metadata:
        raise ValueError(
            f"Empty metadata found at indexes: {empty_metadata}"
        )

    return ids, texts, metadatas


# ============================================================
# STEP 3: LOAD EMBEDDING MODEL
# ============================================================

def load_embedding_model():
    print("\nStep 3: Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"Loaded model: {EMBEDDING_MODEL}")

    return model


# ============================================================
# STEP 4: GENERATE EMBEDDINGS
# ============================================================

def generate_embeddings(model, texts):
    print("\nStep 4: Generating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    print(f"Generated embeddings shape: {embeddings.shape}")

    return embeddings


# ============================================================
# STEP 5: UPSERT VECTORS INTO CHROMADB
# ============================================================

def build_vector_index(ids, texts, metadatas, embeddings):

    print("\nStep 5: Upserting vectors...")

    # --------------------------------------------------------
    # Final validation before ChromaDB
    # --------------------------------------------------------

    if len(ids) != len(texts):
        raise ValueError("IDs and texts count mismatch.")

    if len(ids) != len(metadatas):
        raise ValueError("IDs and metadata count mismatch.")

    if len(ids) != len(embeddings):
        raise ValueError("IDs and embeddings count mismatch.")

    for index, metadata in enumerate(metadatas):

        if not isinstance(metadata, dict) or len(metadata) == 0:
            raise ValueError(
                f"Invalid metadata at index {index}: {metadata}"
            )

    # --------------------------------------------------------
    # Create ChromaDB client
    # --------------------------------------------------------

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # --------------------------------------------------------
    # Create or get collection
    # --------------------------------------------------------

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    print(f"Collection: {COLLECTION_NAME}")

    # --------------------------------------------------------
    # Upsert
    # --------------------------------------------------------

    collection.upsert(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas
    )

    print(f"Upserted vectors: {len(ids)}")

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    count = collection.count()

    print(f"Vectors in collection: {count}")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("DAY 06 - VECTOR INDEX BUILD")
    print("=" * 70)

    # Step 1
    chunks = load_chunks(CHUNKS_FILE)

    # Step 2
    ids, texts, metadatas = prepare_chunk_data(chunks)

    # Step 3
    model = load_embedding_model()

    # Step 4
    embeddings = generate_embeddings(
        model,
        texts
    )

    # Step 5
    build_vector_index(
        ids,
        texts,
        metadatas,
        embeddings
    )

    print("\n" + "=" * 70)
    print("VECTOR INDEX BUILD COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()