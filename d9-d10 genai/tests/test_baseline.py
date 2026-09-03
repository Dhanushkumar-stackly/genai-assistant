from src.baseline import load_baseline


def test_baseline_exists():
    config = load_baseline()

    assert config is not None


def test_baseline_is_frozen():
    config = load_baseline()

    assert config["frozen"] is True


def test_required_configuration_exists():
    config = load_baseline()

    assert "embedding_model" in config
    assert "chunking" in config
    assert "retrieval" in config
    assert "prompt" in config


def test_chunk_configuration_exists():
    config = load_baseline()

    assert "chunk_size" in config["chunking"]
    assert "chunk_overlap" in config["chunking"]


def test_retrieval_configuration_exists():
    config = load_baseline()

    assert "top_k" in config["retrieval"]
    assert "filters" in config["retrieval"]
    assert "score_threshold" in config["retrieval"]