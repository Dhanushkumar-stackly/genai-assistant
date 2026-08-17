from typing import Optional, Literal, Union

from pydantic import BaseModel


class SummarizerOutput(BaseModel):
    summary: str


class ExtractorOutput(BaseModel):
    invoice_number: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[Union[str, float, int]] = None


class ClassifierOutput(BaseModel):
    label: Literal["invoice", "receipt", "other"]
    reason: str