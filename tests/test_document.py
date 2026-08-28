from app.models.document import Document


document = Document(
    document_id="DOC001",
    title="Company Leave Policy",
    content="Employees are eligible for annual leave.",
    source_path="data/company_policy.txt",
    updated_at="2026-08-10T10:00:00"
)

print(document)