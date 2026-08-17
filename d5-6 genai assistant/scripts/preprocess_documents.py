import json
import re
from pathlib import Path

from src.preprocessing.loader import load_documents
from src.preprocessing.cleaner import clean_text
from src.preprocessing.chunker import chunk_text
from src.preprocessing.metadata import create_chunk_metadata


DOCUMENT_FOLDER = "data/documents"
OUTPUT_FILE = "outputs/chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def extract_title(text, fallback_title):
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)

    if match:
        return match.group(1).strip()

    return fallback_title


def main():
    documents = load_documents(DOCUMENT_FOLDER)

    all_chunks = []

    for document in documents:
        cleaned_text = clean_text(document["text"])

        title = extract_title(
            cleaned_text,
            document["doc_id"],
        )

        chunks = chunk_text(
            cleaned_text,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        for index, chunk in enumerate(chunks):

            metadata = create_chunk_metadata(
                doc_id=document["doc_id"],
                title=title,
                source_path=document["source_path"],
                chunk_index=index,
            )

            chunk_record = {
                "chunk_id": metadata["chunk_id"],
                "doc_id": metadata["doc_id"],
                "title": metadata["title"],
                "source_path": metadata["source_path"],
                "updated_at": metadata["updated_at"],
                "chunk_index": metadata["chunk_index"],
                "text": chunk,
            }

            all_chunks.append(chunk_record)

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("Preprocessing completed successfully.")
    print(f"Documents processed: {len(documents)}")
    print(f"Chunks created: {len(all_chunks)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()