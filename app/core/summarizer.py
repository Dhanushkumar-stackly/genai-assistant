from pathlib import Path


class Summarizer:

    def __init__(self, model_client):
        self.model_client = model_client

    def summarize(self, text: str) -> str:

        prompt_path = (
            Path(__file__).resolve().parents[2]
            / "prompts"
            / "summarizer"
            / "v1.txt"
        )

        prompt_template = prompt_path.read_text(
            encoding="utf-8"
        )

        prompt = prompt_template.format(text=text)

        response = self.model_client.generate(prompt)

        return response["text"]