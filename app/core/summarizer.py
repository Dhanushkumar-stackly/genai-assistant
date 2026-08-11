from app.core.model_client import ModelClient


class Summarizer:
    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def summarize(self, text: str) -> str:
        prompt = f"""
Summarize the following text concisely.

TEXT:
{text}

SUMMARY:
"""

        response = self.model_client.generate(prompt)

        return response["text"]