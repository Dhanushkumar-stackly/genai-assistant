from src.rag.citation_mapper import (
    build_allowed_citations,
    validate_citations,
    map_citations_to_sources
)


def sample_chunks():

    return [
        {
            "chunk_id":
                "document_006_chunk_000",

            "text":
                "Reinforcement Learning "
                "uses agents, states, "
                "actions, and rewards.",

            "metadata": {
                "source":
                    "document_006"
            },

            "distance": 0.25
        },
        {
            "chunk_id":
                "document_021_chunk_000",

            "text":
                "Machine learning systems "
                "can learn from data.",

            "metadata": {
                "source":
                    "document_021"
            },

            "distance": 0.40
        }
    ]


def test_allowed_citations_only_contain_retrieved_chunks():

    chunks = sample_chunks()

    allowed = build_allowed_citations(
        chunks
    )

    assert (
        "document_006_chunk_000"
        in allowed
    )

    assert (
        "document_021_chunk_000"
        in allowed
    )

    assert (
        "document_030_chunk_000"
        not in allowed
    )


def test_invalid_citation_is_removed():

    chunks = sample_chunks()

    citations = [
        "document_006_chunk_000",
        "document_030_chunk_000"
    ]

    valid = validate_citations(
        citations,
        chunks
    )

    assert valid == [
        "document_006_chunk_000"
    ]


def test_duplicate_citations_are_removed():

    chunks = sample_chunks()

    citations = [
        "document_006_chunk_000",
        "document_006_chunk_000"
    ]

    valid = validate_citations(
        citations,
        chunks
    )

    assert valid == [
        "document_006_chunk_000"
    ]


def test_citations_are_mapped_to_sources():

    chunks = sample_chunks()

    citations = [
        "document_006_chunk_000"
    ]

    sources = map_citations_to_sources(
        citations,
        chunks
    )

    assert len(sources) == 1

    assert (
        sources[0]["chunk_id"]
        == "document_006_chunk_000"
    )

    assert (
        sources[0]["source"]
        == "document_006"
    )

    assert (
        sources[0]["distance"]
        == 0.25
    )