from app.core.classifier import Classifier


class FakeModelClient:

    def generate(self, prompt):
        return {
            "text": '{"label": "invoice", "reason": "The text contains an invoice number."}',
            "model": "test-model",
            "latency_ms": 10.0,
        }


def test_classifier_returns_label_and_reason():

    client = FakeModelClient()

    classifier = Classifier(client)

    result = classifier.classify(
        "Invoice Number: INV-1001"
    )

    assert result.label == "invoice"
    assert result.reason