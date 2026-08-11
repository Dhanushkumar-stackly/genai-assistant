import json

from app.core.model_client import ModelClient


class Extractor:
    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def extract(self, text: str) -> dict:
        prompt = f"""
Extract the following fields from the document.

Required fields:
- invoice_number
- customer_name
- customer_email
- invoice_date
- total_amount

Rules:
1. Extract only information explicitly present in the document.
2. Do not guess or infer missing values.
3. If a field is missing, return null.
4. Return only valid JSON.
5. Use exactly the field names specified above.

DOCUMENT:
{text}

JSON:
"""

        response = self.model_client.generate(prompt)

        return json.loads(response["text"])