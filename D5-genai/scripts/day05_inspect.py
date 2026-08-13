from pathlib import Path
import json
from collections import Counter


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = BASE_DIR / "outputs"
CHUNKS_PATH = OUTPUTS_DIR / "chunks.jsonl"


# ============================================================
# LOAD CHUNKS
# ============================================================

def load_chunks():
    """
    Load chunks from outputs/chunks.jsonl.

    utf-8-sig is intentionally used here because it supports:
    1. Normal UTF-8
    2. UTF-8 files containing BOM
    """

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Chunk dataset not found: {CHUNKS_PATH}"
        )

    chunks = []

    # IMPORTANT:
    # utf-8-sig fixes the UTF-8 BOM error.
    with open(CHUNKS_PATH, "r", encoding="utf-8-sig") as f:

        for line_number, line in enumerate(f, start=1):

            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            try:
                chunk = json.loads(line)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}"
                ) from exc

            chunks.append(chunk)

    return chunks


# ============================================================
# VALIDATE CHUNK
# ============================================================

def validate_chunk(chunk, index):
    """
    Validate the basic structure of each chunk.
    """

    required_fields = [
        "chunk_id",
        "document_id",
        "text",
        "metadata",
    ]

    errors = []

    for field in required_fields:

        if field not in chunk:
            errors.append(
                f"Missing field: {field}"
            )

    if "text" in chunk:

        if not isinstance(chunk["text"], str):
            errors.append(
                "text must be a string"
            )

        elif not chunk["text"].strip():
            errors.append(
                "text is empty"
            )

    if "metadata" in chunk:

        if not isinstance(chunk["metadata"], dict):
            errors.append(
                "metadata must be an object"
            )

    if errors:

        print(
            f"❌ Chunk {index} validation failed:"
        )

        for error in errors:
            print(f"   - {error}")

        return False

    return True


# ============================================================
# PRINT CHUNK
# ============================================================

def print_chunk(chunk, index):
    """
    Print one chunk in a readable format.
    """

    print()
    print("=" * 70)

    print(f"Chunk #{index}")

    print("-" * 70)

    print(
        f"Chunk ID     : "
        f"{chunk.get('chunk_id')}"
    )

    print(
        f"Document ID  : "
        f"{chunk.get('document_id')}"
    )

    print(
        f"Text         : "
        f"{chunk.get('text')}"
    )

    metadata = chunk.get("metadata", {})

    print(
        f"Source       : "
        f"{metadata.get('source')}"
    )

    print(
        f"Chunk Index  : "
        f"{metadata.get('chunk_index')}"
    )

    print(
        f"Text Length  : "
        f"{len(chunk.get('text', ''))}"
    )


# ============================================================
# DOCUMENT STATISTICS
# ============================================================

def document_statistics(chunks):
    """
    Display document-level statistics.
    """

    document_ids = [
        chunk.get("document_id")
        for chunk in chunks
    ]

    counts = Counter(document_ids)

    print()
    print("=" * 70)
    print("DOCUMENT STATISTICS")
    print("=" * 70)

    for document_id, count in counts.items():

        print(
            f"{document_id}: "
            f"{count} chunk(s)"
        )


# ============================================================
# SOURCE STATISTICS
# ============================================================

def source_statistics(chunks):
    """
    Display source file statistics.
    """

    sources = []

    for chunk in chunks:

        metadata = chunk.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            "unknown"
        )

        sources.append(source)

    counts = Counter(sources)

    print()
    print("=" * 70)
    print("SOURCE STATISTICS")
    print("=" * 70)

    for source, count in counts.items():

        print(
            f"{source}: "
            f"{count} chunk(s)"
        )


# ============================================================
# TEXT STATISTICS
# ============================================================

def text_statistics(chunks):
    """
    Display text length statistics.
    """

    lengths = [
        len(chunk.get("text", ""))
        for chunk in chunks
    ]

    if not lengths:
        return

    total_characters = sum(lengths)

    minimum = min(lengths)
    maximum = max(lengths)
    average = total_characters / len(lengths)

    print()
    print("=" * 70)
    print("TEXT STATISTICS")
    print("=" * 70)

    print(
        f"Total characters : "
        f"{total_characters}"
    )

    print(
        f"Minimum length   : "
        f"{minimum}"
    )

    print(
        f"Maximum length   : "
        f"{maximum}"
    )

    print(
        f"Average length   : "
        f"{average:.2f}"
    )


# ============================================================
# CHECK DUPLICATES
# ============================================================

def check_duplicate_chunk_ids(chunks):
    """
    Check whether duplicate chunk IDs exist.
    """

    chunk_ids = [
        chunk.get("chunk_id")
        for chunk in chunks
    ]

    counts = Counter(chunk_ids)

    duplicates = [
        chunk_id
        for chunk_id, count in counts.items()
        if count > 1
    ]

    print()
    print("=" * 70)
    print("DUPLICATE CHECK")
    print("=" * 70)

    if duplicates:

        print("❌ Duplicate chunk IDs found:")

        for chunk_id in duplicates:

            print(
                f"   - {chunk_id}"
            )

    else:

        print(
            "✅ No duplicate chunk IDs found."
        )


# ============================================================
# VALIDATE ALL CHUNKS
# ============================================================

def validate_all_chunks(chunks):
    """
    Validate every chunk.
    """

    print()
    print("=" * 70)
    print("CHUNK VALIDATION")
    print("=" * 70)

    valid_count = 0
    invalid_count = 0

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        if validate_chunk(
            chunk,
            index
        ):

            valid_count += 1

        else:

            invalid_count += 1

    print()

    print(
        f"Valid chunks   : "
        f"{valid_count}"
    )

    print(
        f"Invalid chunks : "
        f"{invalid_count}"
    )

    if invalid_count == 0:

        print(
            "✅ All chunks are valid."
        )

        return True

    print(
        "❌ Some chunks require attention."
    )

    return False


# ============================================================
# DISPLAY SUMMARY
# ============================================================

def display_summary(chunks):
    """
    Display overall dataset summary.
    """

    print()
    print("=" * 70)
    print("CHUNK DATASET SUMMARY")
    print("=" * 70)

    print(
        f"Dataset path : "
        f"{CHUNKS_PATH}"
    )

    print(
        f"Total chunks : "
        f"{len(chunks)}"
    )

    document_ids = {
        chunk.get("document_id")
        for chunk in chunks
    }

    print(
        f"Documents    : "
        f"{len(document_ids)}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("DAY 05 - CHUNK DATASET INSPECTION")
    print("=" * 70)

    print()
    print(
        f"Loading chunks from:"
    )

    print(
        CHUNKS_PATH
    )

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    try:

        chunks = load_chunks()

    except FileNotFoundError as exc:

        print()
        print("❌ ERROR")
        print(exc)

        return

    except ValueError as exc:

        print()
        print("❌ ERROR")
        print(exc)

        return

    # --------------------------------------------------------
    # EMPTY DATASET CHECK
    # --------------------------------------------------------

    if not chunks:

        print()
        print(
            "❌ No chunks found in "
            "chunks.jsonl"
        )

        return

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    display_summary(chunks)

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    validate_all_chunks(chunks)

    # --------------------------------------------------------
    # DOCUMENT STATISTICS
    # --------------------------------------------------------

    document_statistics(chunks)

    # --------------------------------------------------------
    # SOURCE STATISTICS
    # --------------------------------------------------------

    source_statistics(chunks)

    # --------------------------------------------------------
    # TEXT STATISTICS
    # --------------------------------------------------------

    text_statistics(chunks)

    # --------------------------------------------------------
    # DUPLICATE CHECK
    # --------------------------------------------------------

    check_duplicate_chunk_ids(chunks)

    # --------------------------------------------------------
    # PRINT ALL CHUNKS
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("ALL CHUNKS")
    print("=" * 70)

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        print_chunk(
            chunk,
            index
        )

    # --------------------------------------------------------
    # COMPLETED
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("✅ INSPECTION COMPLETED")
    print("=" * 70)

    print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()