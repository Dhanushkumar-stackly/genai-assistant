import time

from openai import OpenAI



class ModelClient:

    def __init__(self, model: str = "gpt-5"):
        self.client = OpenAI()
        self.model = model

    def generate(self, prompt: str) -> dict:
        start_time = time.perf_counter()

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        latency = time.perf_counter() - start_time

        return {
            "text": response.output_text,
            "model": self.model,
            "latency_seconds": round(latency, 3),
        }