import json
from pathlib import Path


CHUNKS_FILE = Path(__file__).resolve().parents[1] / "outputs" / "chunks.json"


def load_chunks():
    with CHUNKS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def test_chunk_dataset_is_not_empty():
    chunks = load_chunks()
    assert chunks


def test_no_empty_chunks():
    chunks = load_chunks()
    assert all(item.get("text", "").strip() for item in chunks)


def test_chunk_ids_are_unique():
    chunks = load_chunks()
    ids = [item["chunk_id"] for item in chunks]
    assert len(ids) == len(set(ids))


def test_every_chunk_has_traceability_metadata():
    chunks = load_chunks()
    required = {"chunk_id", "doc_id", "source_path", "chunk_index"}
    assert all(required.issubset(item.keys()) for item in chunks)


def test_chunks_have_positive_text_length():
    chunks = load_chunks()
    assert all(len(item.get("text", "").strip()) > 0 for item in chunks)
