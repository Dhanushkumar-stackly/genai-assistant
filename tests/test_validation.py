import pytest
from pydantic import ValidationError

from app.core.response_validator import validate_response
from app.models.outputs import (
    ExtractorOutput,
    ClassifierOutput,
)


def test_valid_classifier_response():

    response = """
    {
        "label": "invoice",
        "reason": "Invoice number is present."
    }
    """

    result = validate_response(
        response,
        ClassifierOutput,
    )

    assert result.label == "invoice"


def test_invalid_classifier_label():

    response = """
    {
        "label": "unknown",
        "reason": "Test"
    }
    """

    with pytest.raises(ValidationError):

        validate_response(
            response,
            ClassifierOutput,
        )


def test_invalid_json():

    response = """
    {
        "label": "invoice",
    """

    with pytest.raises(Exception):

        validate_response(
            response,
            ClassifierOutput,
        )


def test_extractor_missing_values():

    response = """
    {
        "invoice_number": "INV-1001",
        "customer_name": "Ravi",
        "customer_email": null,
        "invoice_date": null,
        "total_amount": null
    }
    """

    result = validate_response(
        response,
        ExtractorOutput,
    )

    assert result.invoice_number == "INV-1001"
    assert result.customer_email is None