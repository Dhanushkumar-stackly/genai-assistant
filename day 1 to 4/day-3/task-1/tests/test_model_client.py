import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model_client import ModelClient, ModelResponse

def test_model_client_returns_metadata():
    result = ModelClient().generate("hello")
    assert isinstance(result, ModelResponse)
    assert result.text == "hello"
    assert result.model == "offline-test-model"
    assert result.latency_ms >= 0

def test_model_client_rejects_empty_prompt():
    import pytest
    with pytest.raises(ValueError):
        ModelClient().generate("  ")
