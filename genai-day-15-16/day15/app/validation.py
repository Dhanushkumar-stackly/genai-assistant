"""
Day 15 - Task 3
Input validation and safe parsing.
"""

from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictStr,
    ValidationError,
    field_validator,
)


MAX_QUESTION_LENGTH = 2000


class QueryRequest(BaseModel):
    """
    Strict request schema for the RAG API.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    question: StrictStr = Field(
        ...,
        min_length=1,
        max_length=MAX_QUESTION_LENGTH,
        description="User question for the RAG system.",
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Question must contain meaningful text."
            )

        return value


def validate_query(payload: Any) -> QueryRequest:
    """
    Safely validate incoming request data.

    Raises:
        ValidationError: when the payload is invalid.
    """

    return QueryRequest.model_validate(payload)