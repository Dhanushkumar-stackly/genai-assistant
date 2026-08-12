import json
from pathlib import Path

from app.core.model_client import ModelClient
from app.models.outputs import SummarizerOutput


class Summarizer:

    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def summarize(self, text: str) -> SummarizerOutput:

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

        data = json.loads(response["text"])

        return SummarizerOutput.model_validate(data)