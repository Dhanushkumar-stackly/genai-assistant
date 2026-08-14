import json
from pathlib import Path

from app.embeddings import EmbeddingModel
from app.vector_store.vector_store import VectorStore


# ============================================================
# PATHS
# ============================================================

CHUNKS_FILE = Path(
    "outputs/chunks.jsonl"
)

EMBEDDING_METADATA_FILE = Path(
    "outputs/embedding_metadata.json"
)


# ============================================================
# LOAD CHUNKS
# ============================================================

def load_chunks():

    if not CHUNKS_FILE.exists():

        raise FileNotFoundError(
            f"Day 5 chunks file not found: "
            f"{CHUNKS_FILE}"
        )

    chunks = []

    with CHUNKS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
        ):

            line = line.strip()

            if not line:
                continue

            try:

                chunk = json.loads(line)

            except json.JSONDecodeError as error:

                raise ValueError(
                    f"Invalid JSON on line "
                    f"{line_number}: {error}"
                )

            chunks.append(chunk)

    return chunks


# ============================================================
# PREPARE METADATA
# ============================================================

def prepare_metadata(chunks):

    metadatas = []

    for index, chunk in enumerate(chunks):

        metadata = chunk.get(
            "metadata"
        )

        if not isinstance(
            metadata,
            dict
        ):

            metadata = {}

        # ChromaDB does not accept
        # an empty metadata dictionary.

        if not metadata:

            metadata = {
                "chunk_index": index
            }

        clean_metadata = {}

        for key, value in metadata.items():

            if value is None:
                continue

            if isinstance(
                value,
                (str, int, float, bool)
            ):

                clean_metadata[
                    str(key)
                ] = value

            else:

                clean_metadata[
                    str(key)
                ] = str(value)

        if not clean_metadata:

            clean_metadata = {
                "chunk_index": index
            }

        metadatas.append(
            clean_metadata
        )

    return metadatas


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("DAY 06 - VECTOR INDEX BUILD")
    print("=" * 60)

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    print()
    print(
        "Step 1: Loading Day 5 chunks..."
    )

    chunks = load_chunks()

    print(
        f"Loaded chunks: {len(chunks)}"
    )

    if not chunks:

        raise ValueError(
            "No chunks found in Day 5 output."
        )

    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    print()
    print(
        "Step 2: Preparing chunk data..."
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    metadatas = prepare_metadata(
        chunks
    )

    print(
        f"Prepared texts: "
        f"{len(texts)}"
    )

    print(
        f"Prepared IDs: "
        f"{len(ids)}"
    )

    print(
        f"Prepared metadata: "
        f"{len(metadatas)}"
    )

    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    print()
    print(
        "Step 3: Loading embedding model..."
    )

    embedding_model = EmbeddingModel()

    print(
        f"Embedding model: "
        f"{embedding_model.model_name}"
    )

    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    print()
    print(
        "Step 4: Generating embeddings..."
    )

    embeddings = embedding_model.encode(
        texts,
        batch_size=32,
    )

    print(
        f"Generated embeddings: "
        f"{len(embeddings)}"
    )

    if embeddings:

        print(
            f"Embedding dimension: "
            f"{len(embeddings[0])}"
        )

    # --------------------------------------------------------
    # STEP 5
    # --------------------------------------------------------

    print()
    print(
        "Step 5: Creating vector store..."
    )

    vector_store = VectorStore(
        persist_directory="vector_db",
        collection_name="d5_chunks",
    )

    print(
        "Vector store initialized."
    )

    # --------------------------------------------------------
    # STEP 6
    # --------------------------------------------------------

    print()
    print(
        "Step 6: Adding documents "
        "to vector store..."
    )

    vector_store.add_documents(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        "Documents added successfully."
    )

    # --------------------------------------------------------
    # STEP 7
    # --------------------------------------------------------

    print()
    print(
        "Step 7: Saving embedding metadata..."
    )

    metadata = {

        "embedding_model":
            embedding_model.model_name,

        "batch_size":
            32,

        "normalized":
            True,

        "embedding_dimension":
            (
                len(embeddings[0])
                if embeddings
                else 0
            ),

        "chunk_count":
            len(chunks),

        "collection":
            "d5_chunks",
    }

    EMBEDDING_METADATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with EMBEDDING_METADATA_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=2,
        )

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print(
        "VECTOR INDEX CREATED SUCCESSFULLY"
    )
    print("=" * 60)

    print(
        f"Vector count: "
        f"{vector_store.count()}"
    )

    print(
        f"Embedding metadata: "
        f"{EMBEDDING_METADATA_FILE}"
    )

    print(
        "Vector database: vector_db/"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()