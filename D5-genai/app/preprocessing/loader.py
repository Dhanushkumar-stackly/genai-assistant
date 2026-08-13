from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".html",
    ".htm",
}


def load_document(path: Path) -> str:
    """Load one supported document as UTF-8 text."""

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Expected a file: {path}"
        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    return path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def load_documents(
    directory: Path,
) -> list[tuple[Path, str]]:

    """Load all supported documents."""

    if not directory.exists():
        raise FileNotFoundError(
            f"Document directory does not exist: {directory}"
        )

    if not directory.is_dir():
        raise ValueError(
            f"Expected directory: {directory}"
        )

    documents = []

    for path in sorted(directory.iterdir()):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        text = load_document(path)

        documents.append(
            (path, text)
        )

    return documents