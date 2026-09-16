from src.day10.task1_experiments import (
    changed_parameters,
    create_experiment,
    load_baseline,
    validate_controlled_experiment,
)


def test_load_baseline():

    baseline = load_baseline()

    assert (
        baseline["embedding_model"]
        == "all-MiniLM-L6-v2"
    )

    assert baseline["chunk_size"] == 500
    assert baseline["chunk_overlap"] == 50
    assert baseline["top_k"] == 5


def test_chunking_changes_only_chunk_size():

    baseline = {
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 500,
        "chunk_overlap": 50,
        "top_k": 5,
        "filters": "none",
        "score_threshold": 0.35,
        "prompt_version": "v1",
    }

    experiment = create_experiment(
        "chunk_test",
        baseline,
        chunk_size=300,
    )

    changes = changed_parameters(
        baseline,
        experiment,
    )

    assert changes == [
        "chunk_size"
    ]


def test_top_k_changes_only_top_k():

    baseline = {
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 500,
        "chunk_overlap": 50,
        "top_k": 5,
        "filters": "none",
        "score_threshold": 0.35,
        "prompt_version": "v1",
    }

    experiment = create_experiment(
        "top_k_test",
        baseline,
        top_k=10,
    )

    changes = changed_parameters(
        baseline,
        experiment,
    )

    assert changes == [
        "top_k"
    ]


def test_multiple_changes_are_rejected():

    baseline = {
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 500,
        "chunk_overlap": 50,
        "top_k": 5,
        "filters": "none",
        "score_threshold": 0.35,
        "prompt_version": "v1",
    }

    experiment = create_experiment(
        "invalid_test",
        baseline,
        chunk_size=300,
        top_k=10,
    )

    try:
        validate_controlled_experiment(
            baseline,
            experiment,
        )

    except ValueError:
        return

    assert False, (
        "Multiple configuration changes "
        "must be rejected."
    )