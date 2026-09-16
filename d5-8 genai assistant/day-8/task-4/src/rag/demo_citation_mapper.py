from src.rag.citation_mapper import map_citations


chunks = [
    {
        "source": "python_guide.pdf",
        "chunk_id": "chunk_001",
        "text": "Python is a programming language.",
    },
    {
        "source": "python_guide.pdf",
        "chunk_id": "chunk_002",
        "text": "Python supports object-oriented programming.",
    },
]

citations = map_citations(chunks)

print("=" * 60)
print("CITATION MAPPING OUTPUT")
print("=" * 60)

for citation in citations:
    print(
        f"Source: {citation['source']} | "
        f"Chunk: {citation['chunk_id']}"
    )