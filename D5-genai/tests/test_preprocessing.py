from pathlib import Path

import pytest

from app.preprocessing.chunker import (
    ChunkConfig,
    chunk_text,
)

from app.preprocessing.cleaner import (
    clean_text,
)

from app.preprocessing.loader import (
    load_document,
)


def test_clean_text_normalizes_whitespace():

    raw_text = (
        "Hello     world\n\n\n\n"
        "Second paragraph"
    )

    result = clean_text(
        raw_text,
        ".md",
    )

    assert result == (
        "Hello world\n"
        "Second paragraph"
    )


def test_markdown_heading_is_preserved():

    raw_text = (
        "# Employee Handbook\n\n"
        "Employees must follow policy."
    )

    result = clean_text(
        raw_text,
        ".md",
    )

    assert (
        "# Employee Handbook"
        in result
    )


def test_html_heading_is_preserved():

    raw_html = """
    <html>
        <body>
            <h1>Leave Policy</h1>
            <p>Employees must submit leave.</p>
            <h2>Approval</h2>
            <p>Manager approval is required.</p>
        </body>
    </html>
    """

    result = clean_text(
        raw_html,
        ".html",
    )

    assert "# Leave Policy" in result
    assert "## Approval" in result
    assert (
        "Employees must submit leave."
        in result
    )


def test_empty_text_creates_no_chunks():

    config = ChunkConfig(
        chunk_size=800,
        overlap=120,
    )

    result = chunk_text(
        "",
        config,
    )

    assert result == []


def test_chunking_creates_multiple_chunks():

    text = (
        "This is a sentence. " * 200
    )

    config = ChunkConfig(
        chunk_size=200,
        overlap=40,
    )

    chunks = chunk_text(
        text,
        config,
    )

    assert len(chunks) > 1


def test_invalid_chunk_size():

    with pytest.raises(
        ValueError
    ):

        ChunkConfig(
            chunk_size=0,
            overlap=0,
        )


def test_invalid_overlap():

    with pytest.raises(
        ValueError
    ):

        ChunkConfig(
            chunk_size=100,
            overlap=100,
        )


def test_document_loader(
    tmp_path: Path,
):

    document = (
        tmp_path
        / "sample.md"
    )

    document.write_text(
        "# Sample\n\nHello",
        encoding="utf-8",
    )

    result = load_document(
        document
    )

    assert "# Sample" in result


def test_unsupported_extension(
    tmp_path: Path,
):

    document = (
        tmp_path
        / "sample.pdf"
    )

    document.write_text(
        "sample",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError
    ):

        load_document(
            document
        )