from app.core.model_client import ModelClient


class Summarizer:

    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def summarize(self, text: str) -> str:

        if text is None or not str(text).strip():
            raise ValueError("Text cannot be empty.")

        text = str(text).strip()

        prompt = f"""
You are a helpful text summarization assistant.

Summarize the following text clearly and concisely.

TEXT:
{text}

SUMMARY:
""".strip()

        if not prompt:
            raise ValueError("Generated prompt cannot be empty.")

        response = self.model_client.generate(prompt)

        # ModelClient may return either:
        # 1. a plain string
        # 2. a response dictionary
        if isinstance(response, dict):
            summary = response.get("text", "")

            if not summary:
                raise ValueError("Model response contains no summary text.")

            return summary.strip()

        if isinstance(response, str):
            if not response.strip():
                raise ValueError("Model returned an empty summary.")

            return response.strip()

        raise TypeError(
            f"Unexpected model response type: {type(response).__name__}"
        )