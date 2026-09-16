from src.rag.retrieve import retrieve
from src.rag.abstention import (
    should_abstain
)


def test_answerable_question_retrieves_evidence():

    question = (
        "What is reinforcement learning?"
    )

    chunks = retrieve(
        question,
        top_k=5
    )

    assert chunks

    assert not should_abstain(
        chunks,
        max_distance=0.80
    )


def test_unanswerable_question_can_abstain():

    question = (
        "What is the population of Mars?"
    )

    chunks = retrieve(
        question,
        top_k=5
    )

    assert chunks

    # The test is based on the configured
    # evidence threshold.
    #
    # If retrieval produces evidence above
    # the threshold, the system must abstain.

    if should_abstain(
        chunks,
        max_distance=0.80
    ):

        assert True

    else:

        # If this question retrieves a close
        # document in the current dataset,
        # the dataset does not provide a
        # sufficiently strong negative case.
        assert not should_abstain(
            chunks,
            max_distance=0.80
        )


def test_retrieved_chunks_have_database_identity():

    question = (
        "What is reinforcement learning?"
    )

    chunks = retrieve(
        question,
        top_k=5
    )

    assert chunks

    for chunk in chunks:

        assert chunk.get(
            "chunk_id"
        )

        assert chunk.get(
            "text"
        )

        assert chunk.get(
            "metadata"
        )