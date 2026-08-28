from datetime import datetime

from pydantic import BaseModel


class Document(BaseModel):
    document_id: str
    title: str
    content: str
    source_path: str
    updated_at: datetime