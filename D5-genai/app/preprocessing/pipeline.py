import json
from pathlib import Path

from .chunker import (
    ChunkConfig,
    chunk_text,
)

from .cleaner import (
    clean_text,
)

from .loader import (
    load_documents,
)

from .metadata import (
    ChunkMetadata,
    calculate_line_range,
    create_chunk_metadata,
    create_document_id,
)


def document_title(
    path: Path,
) -> str:

    return (
        path.stem
        .replace("_", " ")
        .replace("-", " ")
        .strip()
        .title()
    )


def detect_category(
    path: Path,
) -> str:

    name = path.stem.lower()

    category_rules = {
        "policy": "policy",
        "security": "security",
        "handbook": "handbook",
        "guide": "guide",
        "testing": "testing",
        "qa": "testing",
        "deployment": "engineering",
        "release": "engineering",
        "coding": "engineering",
        "api": "engineering",
        "database": "engineering",
    }

    for keyword, category in (
        category_rules.items()
    ):

        if keyword in name:
            return category

    return "general"


def process_documents(
    input_directory: Path,
    output_file: Path,
    chunk_config: ChunkConfig,
) -> list[ChunkMetadata]:

    documents = load_documents(
        input_directory
    )

    all_chunks: list[
        ChunkMetadata
    ] = []

    for document_index, (
        source_path,
        raw_text,
    ) in enumerate(
        documents,
        start=1,
    ):

        document_id = create_document_id(
            document_index
        )

        cleaned_text = clean_text(
            raw_text,
            source_path.suffix,
        )

        if not cleaned_text:
            print(
                f"WARNING: Empty document skipped: "
                f"{source_path}"
            )

            continue

        chunks = chunk_text(
            cleaned_text,
            chunk_config,
        )

        title = document_title(
            source_path
        )

        category = detect_category(
            source_path
        )

        search_start = 0

        for chunk_index, chunk in enumerate(
            chunks
        ):

            (
                source_line_start,
                source_line_end,
                search_start,
            ) = calculate_line_range(
                cleaned_text,
                chunk,
                search_start,
            )

            metadata = create_chunk_metadata(
                document_id=document_id,
                title=title,
                source_path=source_path,
                chunk_index=chunk_index,
                text=chunk,
                category=category,
                source_line_start=source_line_start,
                source_line_end=source_line_end,
            )

            all_chunks.append(
                metadata
            )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        for item in all_chunks:

            file.write(
                json.dumps(
                    item.model_dump(),
                    ensure_ascii=False,
                )
                + "\n"
            )

    return all_chunks