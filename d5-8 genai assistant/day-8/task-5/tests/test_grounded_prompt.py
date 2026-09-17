import sys
from pathlib import Path
TASK_ROOT = Path(__file__).resolve().parents[1]
if str(TASK_ROOT) not in sys.path:
    sys.path.insert(0, str(TASK_ROOT))

from src.rag.grounded_prompt import (
    build_grounded_prompt
)


def test_grounded_prompt_uses_context():

    question = (
        "What is reinforcement learning?"
    )

    retrieved_chunks = [
        {
            "chunk_id":
                "document_006_chunk_000",

            "text":
                "Reinforcement Learning "
                "uses an agent, environment, "
                "states, actions, and rewards.",

            "metadata": {
                "source":
                    "document_006"
            },

            "distance": 0.25
        }
    ]

    prompt = build_grounded_prompt(
        question,
        retrieved_chunks
    )

    assert question in prompt

    assert (
        "Reinforcement Learning"
        in prompt
    )

    assert (
        "document_006"
        in prompt
    )


def test_grounded_prompt_rejects_empty_context():

    question = (
        "What is reinforcement learning?"
    )

    prompt = build_grounded_prompt(
        question,
        []
    )

    assert (
        "No supporting evidence"
        in prompt
    )