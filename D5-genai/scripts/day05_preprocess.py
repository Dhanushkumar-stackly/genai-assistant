from pathlib import Path

from app.preprocessing.chunker import (
    ChunkConfig,
)

from app.preprocessing.pipeline import (
    process_documents,
)


PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]


INPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "documents"
)


OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "chunks.jsonl"
)


def main() -> None:

    config = ChunkConfig(
        chunk_size=800,
        overlap=120,
    )

    print("=" * 70)
    print("DAY 05 - DOCUMENT PREPROCESSING")
    print("=" * 70)

    print(
        f"Input directory : "
        f"{INPUT_DIRECTORY}"
    )

    print(
        f"Output file     : "
        f"{OUTPUT_FILE}"
    )

    print(
        f"Chunk size      : "
        f"{config.chunk_size}"
    )

    print(
        f"Overlap         : "
        f"{config.overlap}"
    )

    print("=" * 70)

    chunks = process_documents(
        input_directory=INPUT_DIRECTORY,
        output_file=OUTPUT_FILE,
        chunk_config=config,
    )

    document_ids = {
        chunk.document_id
        for chunk in chunks
    }

    print(
        f"Documents represented : "
        f"{len(document_ids)}"
    )

    print(
        f"Total chunks          : "
        f"{len(chunks)}"
    )

    print("=" * 70)

    if not chunks:

        print(
            "ERROR: No chunks generated."
        )

        raise SystemExit(1)

    print(
        "SUCCESS: Preprocessing completed."
    )

    print(
        f"Dataset written to: "
        f"{OUTPUT_FILE}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()