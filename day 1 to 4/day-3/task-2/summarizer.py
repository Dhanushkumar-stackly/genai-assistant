from pathlib import Path

PROMPT_PATH = Path(__file__).with_name("summarization.txt")

def build_summarization_prompt(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Source text must be non-empty.")
    instruction = PROMPT_PATH.read_text(encoding="utf-8").strip()
    return f"{instruction}\n\nSOURCE TEXT:\n{text.strip()}"

class Summarizer:
    def __init__(self, client):
        self.client = client

    def summarize(self, text: str):
        return self.client.generate(build_summarization_prompt(text))
