from datetime import datetime


def create_chunk_metadata(
    doc_id,
    title,
    source_path,
    chunk_index,
):
    return {
        "chunk_id": f"{doc_id}_chunk_{chunk_index:03d}",
        "doc_id": doc_id,
        "title": title,
        "source_path": source_path,
        "updated_at": datetime.now().isoformat(),
        "chunk_index": chunk_index,
    }