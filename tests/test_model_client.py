from app.core.model_client import ModelClient


def test_model_client_initializes():
    client = ModelClient()

    assert client.model == "openai/gpt-oss-20b:free"
    assert client.client is not None