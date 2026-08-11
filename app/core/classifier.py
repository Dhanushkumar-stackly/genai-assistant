from app.core.model_client import ModelClient


class Classifier:

    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def classify(self, text: str) -> dict:

        prompt = f"""
Classify the following document.

Allowed labels:
- invoice
- receipt
- other

Rules:
1. Return only one valid label.
2. Do not create a new label.
3. Give a short reason.
4. Return the result as valid JSON.
5. Use exactly these field names: label, reason.

DOCUMENT:
{text}

JSON:
"""

        response = self.model_client.generate(prompt)

        return response