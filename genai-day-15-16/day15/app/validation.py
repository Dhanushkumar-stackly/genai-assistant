"""
Day 15 - Task 3
Input validation and safe parsing.
"""

from pydantic import BaseModel, ConfigDict, Field, ValidationError


MAX_QUESTION_LENGTH = 2000


class QueryRequest(BaseModel):
    """
    Valid request accepted by the RAG API.
    """

    model_config = ConfigDict(extra="forbid")

    question: str = Field(
        ...,
        min_length=1,
        max_length=MAX_QUESTION_LENGTH,
    )


def validate_query(payload: object) -> QueryRequest:
    """
    Safely validate an incoming request payload.

    Raises:
        ValidationError: when the payload is invalid.
    """
    return QueryRequest.model_validate(payload)