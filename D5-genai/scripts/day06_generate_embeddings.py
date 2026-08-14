import json
from pathlib import Path

from retrieval.config import (
    CHUNKS_FILE,
    EMBEDDINGS_FILE,
    EMBEDDING_METADATA_FILE,
    EMBEDDING_MODEL_NAME,
    BATCH_SIZE,
)

from retrieval.embeddings import EmbeddingService


def load_chunks():
    """
    Load chunks from JSONL file.

    Each line in chunks.jsonl is one JSON object.
    """

    chunks = []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {error}"
                ) from error

            chunks.append(chunk)

    return chunks


def main():

    print("=" * 60)
    print("DAY 06 - EMBEDDING GENERATION")
    print("=" * 60)

    print(f"Input file : {CHUNKS_FILE}")
    print(f"Model      : {EMBEDDING_MODEL_NAME}")
    print(f"Batch size : {BATCH_SIZE}")
    print()

    # --------------------------------------------------------
    # CHECK INPUT FILE
    # --------------------------------------------------------

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}"
        )

    # --------------------------------------------------------
    # LOAD CHUNKS
    # --------------------------------------------------------

    chunks = load_chunks()

    print(f"Total chunks: {len(chunks)}")

    if not chunks:
        raise ValueError("No chunks found in chunks.jsonl")

    # --------------------------------------------------------
    # EXTRACT TEXT
    # --------------------------------------------------------

    texts = []

    for index, chunk in enumerate(chunks):

        text = chunk.get("text")

        if text is None:
            raise KeyError(
                f"Chunk at index {index} does not contain 'text'"
            )

        if not isinstance(text, str):
            raise TypeError(
                f"Chunk at index {index} has non-string 'text'"
            )

        if not text.strip():
            raise ValueError(
                f"Chunk at index {index} contains empty text"
            )

        texts.append(text)

    # --------------------------------------------------------
    # CREATE EMBEDDING SERVICE
    # --------------------------------------------------------

    embedding_service = EmbeddingService(
        model_name=EMBEDDING_MODEL_NAME,
        batch_size=BATCH_SIZE,
    )

    # --------------------------------------------------------
    # GENERATE EMBEDDINGS
    # --------------------------------------------------------

    embeddings = embedding_service.encode(
        texts,
        batch_size=BATCH_SIZE,
    )

    # --------------------------------------------------------
    # CHECK EMBEDDING COUNT
    # --------------------------------------------------------

    if len(embeddings) != len(chunks):
        raise ValueError(
            f"Embedding count mismatch: "
            f"{len(embeddings)} embeddings for "
            f"{len(chunks)} chunks"
        )

    # --------------------------------------------------------
    # EMBEDDING DIMENSION
    # --------------------------------------------------------

    embedding_dimension = len(embeddings[0])

    print(f"Embedding dimension: {embedding_dimension}")

    # --------------------------------------------------------
    # BUILD OUTPUT RECORDS
    # --------------------------------------------------------

    embedding_records = []

    for chunk, embedding in zip(chunks, embeddings):

        record = {
            "chunk_id": chunk.get("chunk_id"),
            "document_id": chunk.get("document_id"),
            "text": chunk.get("text"),
            "embedding": embedding,
        }

        embedding_records.append(record)

    # --------------------------------------------------------
    # SAVE EMBEDDINGS
    # --------------------------------------------------------

    EMBEDDINGS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        EMBEDDINGS_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            embedding_records,
            file,
            ensure_ascii=False,
            indent=2,
        )

    # --------------------------------------------------------
    # SAVE METADATA
    # --------------------------------------------------------

    metadata = {
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_dimension": embedding_dimension,
        "batch_size": BATCH_SIZE,
        "total_chunks": len(chunks),
        "input_file": str(CHUNKS_FILE),
        "output_file": str(EMBEDDINGS_FILE),
    }

    EMBEDDING_METADATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        EMBEDDING_METADATA_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2,
        )

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("EMBEDDING GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(f"Total chunks      : {len(chunks)}")
    print(f"Embedding dimension: {embedding_dimension}")
    print(f"Embeddings file   : {EMBEDDINGS_FILE}")
    print(f"Metadata file     : {EMBEDDING_METADATA_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()