import json
from pathlib import Path

from app.core.model_client import ModelClient
from app.models.outputs import ExtractorOutput


class Extractor:

    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def extract(self, text: str) -> ExtractorOutput:

        prompt_path = (
            Path(__file__).resolve().parents[2]
            / "prompts"
            / "extractor"
            / "v1.txt"
        )

        prompt_template = prompt_path.read_text(
            encoding="utf-8"
        )

        prompt = prompt_template.format(text=text)

        response = self.model_client.generate(prompt)

        data = json.loads(response["text"])

        return ExtractorOutput.model_validate(data)