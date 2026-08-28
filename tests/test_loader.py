import pytest
from pydantic import ValidationError

from app.models.document import Document


def test_valid_document():
    document = Document(
        document_id="DOC001",
        title="Company Leave Policy",
        content="Employees are eligible for annual leave.",
        source_path="data/company_leave.txt",
        updated_at="2026-08-10T10:00:00",
    )

    assert document.document_id == "DOC001"
    assert document.title == "Company Leave Policy"


def test_missing_required_field():
    with pytest.raises(ValidationError):
        Document(
            document_id="DOC002",
            content="Some content",
            source_path="data/test.txt",
            updated_at="2026-08-10T10:00:00",
        )