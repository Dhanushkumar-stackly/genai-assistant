# scripts/preprocess_documents.py

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.loader import load_documents


DOCUMENT_FOLDER = PROJECT_ROOT / "data" / "documents"


def main():

    print("=" * 60)
    print("STAGE: preprocessing")
    print("=" * 60)

    if not DOCUMENT_FOLDER.exists():
        raise FileNotFoundError(
            f"Document folder not found: {DOCUMENT_FOLDER}"
        )

    documents = load_documents(
        document_folder=str(DOCUMENT_FOLDER)
    )

    print(
        f"Documents loaded: {len(documents)}"
    )

    return documents


if __name__ == "__main__":
    main()