from unittest.mock import Mock

from app.core.extractor import Extractor


def test_extractor_returns_structured_fields():
    mock_model_client = Mock()

    mock_model_client.generate.return_value = {
        "text": """
        {
            "invoice_number": "INV-1001",
            "customer_name": "Ravi Kumar",
            "customer_email": "ravi@example.com",
            "invoice_date": "10-Aug-2026",
            "total_amount": "₹5,500"
        }
        """,
        "model": "openai/gpt-oss-20b:free",
        "latency_ms": 100.0,
    }

    extractor = Extractor(mock_model_client)

    result = extractor.extract(
        "Invoice Number: INV-1001"
    )

    assert result["invoice_number"] == "INV-1001"
    assert result["customer_name"] == "Ravi Kumar"
    assert result["customer_email"] == "ravi@example.com"
    assert result["invoice_date"] == "10-Aug-2026"
    assert result["total_amount"] == "₹5,500"

    mock_model_client.generate.assert_called_once()

def test_extractor_returns_null_for_missing_fields():
    mock_model_client = Mock()

    mock_model_client.generate.return_value = {
        "text": """
        {
            "invoice_number": "INV-1002",
            "customer_name": "Arun Kumar",
            "customer_email": null,
            "invoice_date": "11-Aug-2026",
            "total_amount": "₹2,500"
        }
        """,
        "model": "openai/gpt-oss-20b:free",
        "latency_ms": 100.0,
    }

    extractor = Extractor(mock_model_client)

    result = extractor.extract(
        "Invoice Number: INV-1002"
    )

    assert result["customer_email"] is None