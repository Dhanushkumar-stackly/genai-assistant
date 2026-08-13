from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):

    chunk_id: str

    document_id: str

    title: str

    source_path: str

    updated_at: str

    chunk_index: int = Field(
        ge=0
    )

    category: str = "general"

    source_line_start: int = Field(
        ge=1
    )

    source_line_end: int = Field(
        ge=1
    )

    text: str


def create_document_id(
    document_index: int,
) -> str:

    return f"DOC-{document_index:03d}"


def create_chunk_id(
    document_id: str,
    chunk_index: int,
) -> str:

    return (
        f"{document_id}"
        f"-CHUNK-{chunk_index:04d}"
    )


def get_updated_at(
    source_path: Path,
) -> str:

    timestamp = source_path.stat().st_mtime

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).isoformat()


def calculate_line_range(
    full_text: str,
    chunk_text: str,
    search_start: int,
) -> tuple[int, int, int]:

    position = full_text.find(
        chunk_text,
        search_start,
    )

    if position == -1:

        position = full_text.find(
            chunk_text
        )

    if position == -1:

        return (
            1,
            max(
                1,
                len(chunk_text.splitlines()),
            ),
            search_start,
        )

    end_position = (
        position
        + len(chunk_text)
    )

    start_line = (
        full_text[:position].count("\n")
        + 1
    )

    end_line = (
        full_text[:end_position].count("\n")
        + 1
    )

    return (
        start_line,
        end_line,
        end_position,
    )


def create_chunk_metadata(
    *,
    document_id: str,
    title: str,
    source_path: Path,
    chunk_index: int,
    text: str,
    category: str,
    source_line_start: int,
    source_line_end: int,
) -> ChunkMetadata:

    return ChunkMetadata(
        chunk_id=create_chunk_id(
            document_id,
            chunk_index,
        ),
        document_id=document_id,
        title=title,
        source_path=str(
            source_path
        ),
        updated_at=get_updated_at(
            source_path
        ),
        chunk_index=chunk_index,
        category=category,
        source_line_start=source_line_start,
        source_line_end=source_line_end,
        text=text,
    )