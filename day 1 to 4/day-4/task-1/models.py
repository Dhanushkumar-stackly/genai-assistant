from pydantic import BaseModel, Field
from typing import Literal, Optional

class SummaryOutput(BaseModel):
    summary: list[str] = Field(min_length=1)
class ExtractionOutput(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
class ClassificationOutput(BaseModel):
    label: Literal["business", "technical", "general"]
    reason: str = Field(min_length=1)
