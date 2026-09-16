from src.day10.task1_chunking_experiment import (
    split_text,
)


def test_empty_text_returns_no_chunks():

    result = split_text(
        text="",
        chunk_size=300,
        overlap=50,
    )

    assert result == []


def test_chunk_size_creates_multiple_chunks():

    text = "A" * 1000

    result = split_text(
        text=text,
        chunk_size=300,
        overlap=50,
    )

    assert len(result) > 1


def test_overlap_is_smaller_than_chunk_size():

    text = "A" * 1000

    result = split_text(
        text=text,
        chunk_size=300,
        overlap=50,
    )

    assert result[0][-50:] == result[1][:50]


def test_invalid_chunk_size():

    try:

        split_text(
            text="hello",
            chunk_size=0,
            overlap=0,
        )

    except ValueError:

        return

    assert False


def test_invalid_overlap():

    try:

        split_text(
            text="hello",
            chunk_size=100,
            overlap=100,
        )

    except ValueError:

        return

    assert False