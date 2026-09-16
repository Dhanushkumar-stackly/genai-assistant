from dataclasses import dataclass
from time import perf_counter

@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    latency_ms: float

class ModelClient:
    """Small provider-agnostic wrapper with an offline deterministic mode."""
    def __init__(self, model: str = "offline-test-model"):
        self.model = model

    def generate(self, prompt: str) -> ModelResponse:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string.")
        start = perf_counter()
        text = prompt.strip()
        return ModelResponse(text=text, model=self.model, latency_ms=round((perf_counter()-start)*1000, 3))
