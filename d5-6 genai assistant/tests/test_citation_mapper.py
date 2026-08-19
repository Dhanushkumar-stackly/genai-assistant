from src.rag.citation_mapper import map_citations


def test_map_citations_returns_source_and_chunk_id():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        }
    ]

    citations = map_citations(chunks)

    assert citations == [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
        }
    ]


def test_map_citations_supports_multiple_chunks():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        },
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_002",
            "text": "Python supports OOP.",
        },
    ]

    citations = map_citations(chunks)

    assert len(citations) == 2


def test_map_citations_removes_duplicates():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        },
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
            "text": "Python is a programming language.",
        },
    ]

    citations = map_citations(chunks)

    assert len(citations) == 1


def test_map_citations_skips_invalid_chunks():
    chunks = [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
        },
        {
            "source": "python_guide.pdf",
        },
        {
            "chunk_id": "chunk_003",
        },
    ]

    citations = map_citations(chunks)

    assert citations == [
        {
            "source": "python_guide.pdf",
            "chunk_id": "chunk_001",
        }
    ]


def test_map_citations_handles_empty_chunks():
    citations = map_citations([])

    assert citations == []