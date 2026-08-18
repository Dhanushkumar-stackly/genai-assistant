"""
DAY 05-06 RAG INGESTION
=======================

Pipeline:

Chunks
   ↓
Embeddings
   ↓
ChromaDB Vector Store
   ↓
Semantic Retrieval
"""

from pathlib import Path
import json

import chromadb
import numpy as np


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "outputs"

CHUNKS_FILE = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_FILE = OUTPUT_DIR / "embeddings.npy"

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

COLLECTION_NAME = "rag_documents"


# ============================================================
# FIND JSON CHUNK FILE
# ============================================================

def find_chunks_file():

    # First try the expected Day 5 file
    if CHUNKS_FILE.exists():
        return CHUNKS_FILE

    # Otherwise search automatically
    candidates = list(
        OUTPUT_DIR.glob("*.json")
    )

    for file_path in candidates:

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, list):

                if data and isinstance(data[0], dict):

                    return file_path

            if isinstance(data, dict):

                for key in [
                    "chunks",
                    "data",
                    "records"
                ]:

                    if isinstance(
                        data.get(key),
                        list
                    ):

                        return file_path

        except Exception:
            continue

    raise FileNotFoundError(
        "Could not find Day 5 chunks JSON file "
        f"inside: {OUTPUT_DIR}"
    )


# ============================================================
# LOAD CHUNKS
# ============================================================

def load_chunks():

    print("Loading chunks...")

    file_path = find_chunks_file()

    print(
        f"Chunk file: {file_path}"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    if isinstance(data, list):

        chunks = data

    elif isinstance(data, dict):

        if isinstance(
            data.get("chunks"),
            list
        ):

            chunks = data["chunks"]

        elif isinstance(
            data.get("data"),
            list
        ):

            chunks = data["data"]

        elif isinstance(
            data.get("records"),
            list
        ):

            chunks = data["records"]

        else:

            raise ValueError(
                "Could not identify chunks list "
                "inside JSON."
            )

    else:

        raise ValueError(
            "Unsupported chunks JSON structure."
        )

    print(
        f"Loaded chunks: {len(chunks)}"
    )

    return chunks


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

def load_embeddings():

    print("Loading embeddings...")

    embeddings_file = PROJECT_ROOT / "outputs" / "embeddings.npz"

    if not embeddings_file.exists():

        raise FileNotFoundError(
            f"Embeddings file not found:\n"
            f"{embeddings_file}"
        )

    data = np.load(
        embeddings_file
    )

    print(
        f"NPZ keys: {data.files}"
    )

    # --------------------------------------------------------
    # Find embedding array
    # --------------------------------------------------------

    embeddings = None

    # Preferred key names
    for key in [
        "embeddings",
        "vectors",
        "embedding",
        "arr_0"
    ]:

        if key in data.files:

            embeddings = data[key]

            break

    if embeddings is None:

        raise ValueError(
            "Could not find embedding array in "
            f"{embeddings_file}\n"
            f"Available keys: {data.files}"
        )

    print(
        f"Loaded embeddings: "
        f"{embeddings.shape}"
    )

    return embeddings

    print("Loading embeddings...")

    if not EMBEDDINGS_FILE.exists():

        raise FileNotFoundError(
            f"Embeddings file not found:\n"
            f"{EMBEDDINGS_FILE}"
        )

    embeddings = np.load(
        EMBEDDINGS_FILE
    )

    print(
        f"Loaded embeddings: "
        f"{embeddings.shape}"
    )

    return embeddings


# ============================================================
# EXTRACT TEXT
# ============================================================

def extract_text(chunk):

    if not isinstance(chunk, dict):

        return str(chunk)

    for key in [
        "text",
        "content",
        "page_content",
        "chunk"
    ]:

        value = chunk.get(key)

        if value is not None:

            return str(value)

    return ""


# ============================================================
# EXTRACT METADATA
# ============================================================

def extract_metadata(
    chunk,
    index
):

    metadata = {}

    if isinstance(chunk, dict):

        original_metadata = chunk.get(
            "metadata"
        )

        if isinstance(
            original_metadata,
            dict
        ):

            metadata.update(
                original_metadata
            )

        # ----------------------------------------------------
        # Preserve common top-level metadata
        # ----------------------------------------------------

        for key in [
            "source",
            "source_file",
            "document_id",
            "doc_id",
            "chunk_id",
            "file_name",
            "filename"
        ]:

            if key in chunk:

                value = chunk[key]

                if value is not None:

                    metadata[key] = value

    # --------------------------------------------------------
    # ChromaDB requires NON-EMPTY metadata
    # --------------------------------------------------------

    if not metadata:

        metadata = {
            "chunk_id": f"chunk_{index + 1}",
            "source": f"document_{index + 1}"
        }

    # --------------------------------------------------------
    # Convert metadata values into Chroma-compatible types
    # --------------------------------------------------------

    clean_metadata = {}

    for key, value in metadata.items():

        if value is None:
            continue

        if isinstance(
            value,
            (str, int, float, bool)
        ):

            clean_metadata[str(key)] = value

        else:

            clean_metadata[str(key)] = str(
                value
            )

    # Final safety fallback
    if not clean_metadata:

        clean_metadata = {
            "chunk_id": f"chunk_{index + 1}"
        }

    return clean_metadata


# ============================================================
# BUILD VECTOR INDEX
# ============================================================

def build_vector_index(
    chunks,
    embeddings
):

    print("Building vector index...")

    # --------------------------------------------------------
    # Create ChromaDB client
    # --------------------------------------------------------

    chroma_client = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR)
    )

    # --------------------------------------------------------
    # Create / load collection
    # --------------------------------------------------------

    collection = (
        chroma_client.get_or_create_collection(
            name=COLLECTION_NAME
        )
    )

    ids = []
    documents = []
    metadatas = []
    vectors = []

    # --------------------------------------------------------
    # Prepare records
    # --------------------------------------------------------

    for index, chunk in enumerate(chunks):

        text = extract_text(chunk)

        metadata = extract_metadata(
            chunk,
            index
        )

        # Unique ID
        chunk_id = metadata.get(
            "chunk_id"
        )

        if not chunk_id:

            chunk_id = (
                f"chunk_{index + 1}"
            )

        chunk_id = str(
            chunk_id
        )

        ids.append(chunk_id)

        documents.append(text)

        metadatas.append(metadata)

        vectors.append(
            embeddings[index].tolist()
        )

    # --------------------------------------------------------
    # Validate counts
    # --------------------------------------------------------

    print(
        f"Prepared IDs: {len(ids)}"
    )

    print(
        f"Prepared documents: "
        f"{len(documents)}"
    )

    print(
        f"Prepared metadata: "
        f"{len(metadatas)}"
    )

    print(
        f"Prepared embeddings: "
        f"{len(vectors)}"
    )

    if not (
        len(ids)
        == len(documents)
        == len(metadatas)
        == len(vectors)
    ):

        raise ValueError(
            "Count mismatch between "
            "IDs, documents, metadata "
            "and embeddings."
        )

    # --------------------------------------------------------
    # Validate metadata
    # --------------------------------------------------------

    empty_metadata = [
        index
        for index, metadata in enumerate(
            metadatas
        )
        if not metadata
    ]

    if empty_metadata:

        raise ValueError(
            "Empty metadata found at "
            f"indexes: {empty_metadata}"
        )

    # --------------------------------------------------------
    # Upsert into ChromaDB
    # --------------------------------------------------------

    collection.upsert(

        ids=ids,

        documents=documents,

        embeddings=vectors,

        metadatas=metadatas
    )

    print(
        f"Successfully inserted "
        f"{len(ids)} chunks."
    )

    print(
        f"Collection count: "
        f"{collection.count()}"
    )

    return collection


# ============================================================
# MAIN INGESTION
# ============================================================

def ingest_documents():

    print("=" * 60)
    print("RAG INGESTION")
    print("=" * 60)

    # Step 1
    chunks = load_chunks()

    # Step 2
    embeddings = load_embeddings()

    # --------------------------------------------------------
    # Check chunk / embedding count
    # --------------------------------------------------------

    if len(chunks) != len(embeddings):

        raise ValueError(
            f"Chunk count ({len(chunks)}) "
            f"does not match embedding count "
            f"({len(embeddings)})."
        )

    # Step 3
    collection = build_vector_index(
        chunks,
        embeddings
    )

    # --------------------------------------------------------
    # Final output
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("RAG INGESTION COMPLETE")
    print("=" * 60)

    print(
        f"Collection: {COLLECTION_NAME}"
    )

    print(
        f"Vector count: {collection.count()}"
    )

    print(
        f"Vector DB: {VECTOR_DB_DIR}"
    )

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    ingest_documents()