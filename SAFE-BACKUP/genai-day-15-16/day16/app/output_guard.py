"""
Day 16 - Task 2: Final response validation.
"""

from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    model_validator,
)


class SourceReference(BaseModel):
    """
    Validated source reference returned to the client.
    """

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(..., min_length=1)
    score: float = Field(..., ge=0.0, le=1.0)


class FinalResponse(BaseModel):
    """
    Strict response schema.

    Only a completely validated response is allowed
    to leave the output guardrail.
    """

    model_config = ConfigDict(extra="forbid")

    status: Literal["answered", "abstained"]

    answer: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )

    sources: list[SourceReference]

    reason_code: str = Field(
        ...,
        min_length=1,
    )

    @model_validator(mode="after")
    def validate_source_requirement(self) -> "FinalResponse":
        """
        An answered response must contain
        at least one source.
        """

        if self.status == "answered" and not self.sources:
            raise ValueError(
                "answered responses require at least one source"
            )

        return self


def validate_final_output(
    payload: Any,
) -> dict[str, Any]:
    """
    Validate the complete model output atomically.

    If validation fails, no partial model output
    is returned.
    """

    try:
        validated = FinalResponse.model_validate(payload)

    except ValidationError as exc:
        raise ValueError(
            "INVALID_FINAL_OUTPUT"
        ) from exc

    return validated.model_dump()