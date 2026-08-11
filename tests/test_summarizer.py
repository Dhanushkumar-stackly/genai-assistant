from unittest.mock import Mock

from app.core.summarizer import Summarizer


def test_summarizer_returns_summary():
    mock_model_client = Mock()

    mock_model_client.generate.return_value = {
        "text": "AI is a field of computer science.",
        "model": "openai/gpt-oss-20b:free",
        "latency_ms": 100.0,
    }

    summarizer = Summarizer(mock_model_client)

    result = summarizer.summarize(
        "Artificial Intelligence is a field of computer science."
    )

    assert result == "AI is a field of computer science."
    mock_model_client.generate.assert_called_once()