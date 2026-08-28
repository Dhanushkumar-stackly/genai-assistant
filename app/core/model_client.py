import os
import time

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class ModelClient:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

        self.model = os.getenv(
            "openrouter_model",
            "openai/gpt-oss-20b:free"
        )

    def generate(self, prompt: str) -> dict:

        start_time = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        end_time = time.perf_counter()

        latency_ms = round(
            (end_time - start_time) * 1000,
            2
        )

        return {
            "text": response.choices[0].message.content,
            "model": self.model,
            "latency_ms": latency_ms,
        }