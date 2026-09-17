import sys
from pathlib import Path
TASK_ROOT = Path(__file__).resolve().parents[1]
if str(TASK_ROOT) not in sys.path:
    sys.path.insert(0, str(TASK_ROOT))

from pathlib import Path
from src.preprocessing.loader import load_documents
from src.preprocessing.cleaner import clean_text


DOCUMENT_FOLDER = str(Path(__file__).resolve().parents[1] / "data" / "documents")


documents = load_documents(DOCUMENT_FOLDER)

print(f"Documents loaded: {len(documents)}")

for document in documents:
    cleaned_text = clean_text(document["text"])

    print("\n" + "=" * 60)
    print(f"Doc ID: {document['doc_id']}")
    print(f"Source: {document['source_path']}")
    print("Cleaned text:")
    print(cleaned_text[:500])