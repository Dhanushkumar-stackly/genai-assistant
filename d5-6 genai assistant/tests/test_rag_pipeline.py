from src.rag.retrieve import retrieve
from src.rag.generate import generate_context


def test_retrieval_returns_results():
    question = "What is reinforcement learning?"

    results = retrieve(
        question,
        top_k=5
    )

    assert len(results) > 0


def test_retrieval_contains_required_fields():
    question = "What is reinforcement learning?"

    results = retrieve(
        question,
        top_k=5
    )

    result = results[0]

    assert "chunk_id" in result
    assert "text" in result
    assert "metadata" in result
    assert "distance" in result


def test_generation_context_is_created():
    question = "What is reinforcement learning?"

    results = retrieve(
        question,
        top_k=5
    )

    prompt = generate_context(
        question,
        results,
        max_chunks=5
    )

    assert prompt
    assert question in prompt
    assert "Context:" in prompt


def test_empty_retrieval_is_handled():
    question = "What is reinforcement learning?"

    prompt = generate_context(
        question,
        [],
        max_chunks=5
    )

    assert prompt
    assert "No relevant context" in prompt