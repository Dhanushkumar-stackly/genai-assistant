import json
import sys
from pathlib import Path

from pydantic import ValidationError

from app.models.document import Document


def load_document(file_path: str) -> None:
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        document = Document(**data)

        print("Document loaded successfully.")
        print(f"Document ID: {document.document_id}")
        print(f"Title: {document.title}")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")

    except ValidationError as error:
        print("Error: Document validation failed.")
        print(error)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/load_documents.py <json_file>")
        sys.exit(1)

    load_document(sys.argv[1])