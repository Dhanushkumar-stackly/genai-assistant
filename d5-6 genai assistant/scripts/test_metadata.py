from pathlib import Path

from src.preprocessing.loader import load_documents
from src.preprocessing.cleaner import clean_text
from src.preprocessing.chunker import chunk_text
from src.preprocessing.metadata import create_chunk_metadata


DOCUMENT_FOLDER = "data/documents"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


documents = load_documents(DOCUMENT_FOLDER)

for document in documents:
    cleaned_text = clean_text(document["text"])

    chunks = chunk_text(
        cleaned_text,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    title = Path(document["source_path"]).stem

    print("\n" + "=" * 60)
    print(f"Document: {document['doc_id']}")

    for index, chunk in enumerate(chunks):

        metadata = create_chunk_metadata(
            doc_id=document["doc_id"],
            title=title,
            source_path=document["source_path"],
            chunk_index=index,
        )

        print("\nMetadata:")
        print(metadata)

        print("\nChunk:")
        print(chunk[:200])