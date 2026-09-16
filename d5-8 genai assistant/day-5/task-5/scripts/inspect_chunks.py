import json
from collections import Counter


INPUT_FILE = "outputs/chunks.json"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    print("=" * 60)
    print("CHUNK QUALITY INSPECTION")
    print("=" * 60)

    print(f"Total chunks: {len(chunks)}")

    # 1. Empty chunks
    empty_chunks = [
        chunk for chunk in chunks
        if not chunk["text"].strip()
    ]

    print(f"Empty chunks: {len(empty_chunks)}")

    # 2. Duplicate chunk IDs
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    duplicate_ids = [
        chunk_id
        for chunk_id, count in Counter(chunk_ids).items()
        if count > 1
    ]

    print(f"Duplicate chunk IDs: {len(duplicate_ids)}")

    # 3. Missing metadata
    required_fields = [
        "chunk_id",
        "doc_id",
        "title",
        "source_path",
        "updated_at",
        "chunk_index",
        "text",
    ]

    missing_metadata = []

    for chunk in chunks:
        missing = [
            field
            for field in required_fields
            if field not in chunk or chunk[field] in ("", None)
        ]

        if missing:
            missing_metadata.append(
                {
                    "chunk_id": chunk.get("chunk_id"),
                    "missing": missing,
                }
            )

    print(f"Chunks with missing metadata: {len(missing_metadata)}")

    # 4. Chunk lengths
    lengths = [len(chunk["text"]) for chunk in chunks]

    if lengths:
        print(f"Minimum chunk length: {min(lengths)}")
        print(f"Maximum chunk length: {max(lengths)}")
        print(f"Average chunk length: {sum(lengths) / len(lengths):.2f}")

    # 5. Documents represented
    documents = sorted(
        set(chunk["doc_id"] for chunk in chunks)
    )

    print(f"Documents represented: {len(documents)}")

    print("\nQuality checks:")

    print(
        "PASS" if not empty_chunks
        else "FAIL",
        "- No empty chunks"
    )

    print(
        "PASS" if not duplicate_ids
        else "FAIL",
        "- No duplicate chunk IDs"
    )

    print(
        "PASS" if not missing_metadata
        else "FAIL",
        "- Complete metadata"
    )


if __name__ == "__main__":
    main()