from src.rag.grounded_prompt import build_grounded_prompt


def test_grounded_prompt_contains_question():
    question = "What is reinforcement learning?"

    chunks = [
        {
            "chunk_id": "document_006_chunk_000",
            "text": (
                "Reinforcement Learning allows agents "
                "to learn by interacting with an environment."
            ),
            "metadata": {
                "chunk_id": "document_006_chunk_000",
                "chunk_index": 5
            },
            "distance": 0.25
        }
    ]

    prompt = build_grounded_prompt(
        question,
        chunks
    )

    assert question in prompt


def test_grounded_prompt_contains_chunk_id():
    chunks = [
        {
            "chunk_id": "document_006_chunk_000",
            "text": "Reinforcement learning uses interaction.",
            "metadata": {},
            "distance": 0.25
        }
    ]

    prompt = build_grounded_prompt(
        "What is reinforcement learning?",
        chunks
    )

    assert "document_006_chunk_000" in prompt


def test_grounded_prompt_has_grounding_rules():
    chunks = [
        {
            "chunk_id": "chunk_001",
            "text": "Sample information.",
            "metadata": {},
            "distance": 0.2
        }
    ]

    prompt = build_grounded_prompt(
        "What is this?",
        chunks
    )

    assert "ONLY" in prompt
    assert "Do not use outside knowledge." in prompt
    assert "Never guess." in prompt


def test_grounded_prompt_handles_empty_retrieval():
    prompt = build_grounded_prompt(
        "What is reinforcement learning?",
        []
    )

    assert prompt
    assert "No relevant context was retrieved." in prompt
    assert "not available" in prompt