"""
Day 15 - Task 3
Strict input validation for user questions.
"""

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator


MAX_QUESTION_LENGTH = 500


class QueryRequest(BaseModel):
    """Validated request model for user questions."""

    model_config = ConfigDict(extra="forbid")

    question: StrictStr = Field(
        ...,
        min_length=1,
        max_length=MAX_QUESTION_LENGTH,
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        """Reject empty or whitespace-only questions."""

        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty")

        return value


def validate_query(payload) -> QueryRequest:
    """Validate and return a QueryRequest model."""

    return QueryRequest.model_validate(payload)