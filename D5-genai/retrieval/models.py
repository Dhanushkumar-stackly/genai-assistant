from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ChunkRecord:
    chunk_id: str
    document_id: str
    title: str
    source_path: str
    updated_at: str
    chunk_index: int
    category: str
    text: str


@dataclass
class SearchResult:
    chunk_id: str
    document_id: str
    title: str
    source_path: str
    chunk_index: int
    category: str
    text: str
    score: float
    metadata: Dict[str, Any]