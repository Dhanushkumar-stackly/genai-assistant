import pytest
from pydantic import ValidationError

from app.models.outputs import (
    SummarizerOutput,
    ExtractorOutput,
    ClassifierOutput,
)


def test_summarizer_output_valid():

    result = SummarizerOutput(
        summary="AI is used to process information."
    )

    assert result.summary == "AI is used to process information."


def test_extractor_output_valid():

    result = ExtractorOutput(
        invoice_number="INV-001",
        customer_name="Ravi",
        customer_email=None,
        invoice_date=None,
        total_amount=5000,
    )

    assert result.invoice_number == "INV-001"
    assert result.total_amount == 5000


def test_classifier_output_valid():

    result = ClassifierOutput(
        label="invoice",
        reason="Invoice information is present."
    )

    assert result.label == "invoice"


def test_classifier_rejects_invalid_label():

    with pytest.raises(ValidationError):

        ClassifierOutput(
            label="financial_document",
            reason="Invalid label."
        )