from pathlib import Path


def load_documents(document_folder):
    folder = Path(document_folder)

    documents = []

    for file_path in sorted(folder.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "doc_id": file_path.stem,
                "source_path": str(file_path),
                "text": text,
            }
        )

    return documents