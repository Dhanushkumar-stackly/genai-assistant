<<<<<<< HEAD
from pathlib import Path
=======
>>>>>>> origin/main
from src.preprocessing.loader import load_documents
from src.preprocessing.cleaner import clean_text


<<<<<<< HEAD
DOCUMENT_FOLDER = str(Path(__file__).resolve().parents[1] / "data" / "documents")
=======
DOCUMENT_FOLDER = "data/documents"
>>>>>>> origin/main


documents = load_documents(DOCUMENT_FOLDER)

print(f"Documents loaded: {len(documents)}")

for document in documents:
    cleaned_text = clean_text(document["text"])

    print("\n" + "=" * 60)
    print(f"Doc ID: {document['doc_id']}")
    print(f"Source: {document['source_path']}")
    print("Cleaned text:")
    print(cleaned_text[:500])