from src.preprocessing.loader import load_documents
from src.preprocessing.cleaner import clean_text
from src.preprocessing.chunker import chunk_text


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

    print("\n" + "=" * 60)
    print(f"Document: {document['doc_id']}")
    print(f"Number of chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print(f"\n--- Chunk {index} ---")
        print(chunk)