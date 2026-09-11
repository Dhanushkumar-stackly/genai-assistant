"""
Day 16 - Task 4
Safe fallback and escalation handling.
"""

from dataclasses import dataclass
from typing import Literal


FallbackStatus = Literal[
    "abstained",
    "escalated",
]


@dataclass(frozen=True)
class FallbackResponse:
    """
    Consistent safe response returned when the
    application cannot safely provide an answer.
    """

    status: FallbackStatus
    message: str
    reason_code: str
    escalation_available: bool
    escalation_path: str | None


SAFE_ABSTENTION_MESSAGE = (
    "The available documents do not support this request. "
    "I cannot provide a reliable answer from the available evidence."
)

SAFE_ESCALATION_MESSAGE = (
    "The available documents do not support this request. "
    "Please contact the approved support team for further assistance."
)

APPROVED_SUPPORT_PATH = (
    "Approved Support Team / Human Review"
)


def build_abstention_response(
    reason_code: str,
) -> FallbackResponse:
    """
    Create a consistent safe abstention response.

    No model-generated unsupported answer is included.
    """

    return FallbackResponse(
        status="abstained",
        message=SAFE_ABSTENTION_MESSAGE,
        reason_code=reason_code,
        escalation_available=False,
        escalation_path=None,
    )


def build_escalation_response(
    reason_code: str,
) -> FallbackResponse:
    """
    Create a safe response that directs the user
    to the approved human-support path.
    """

    return FallbackResponse(
        status="escalated",
        message=SAFE_ESCALATION_MESSAGE,
        reason_code=reason_code,
        escalation_available=True,
        escalation_path=APPROVED_SUPPORT_PATH,
    )


def build_fallback(
    reason_code: str,
    escalate: bool = False,
) -> FallbackResponse:
    """
    Route the request to abstention or escalation.

    The fallback never invents an answer.
    """

    if not isinstance(reason_code, str) or not reason_code.strip():
        raise ValueError(
            "reason_code must be a non-empty string"
        )

    if escalate:
        return build_escalation_response(reason_code)

    return build_abstention_response(reason_code)


def response_to_dict(
    response: FallbackResponse,
) -> dict:
    """
    Convert the validated fallback response into
    a client-safe dictionary.
    """

    return {
        "status": response.status,
        "message": response.message,
        "reason_code": response.reason_code,
        "escalation_available": (
            response.escalation_available
        ),
        "escalation_path": response.escalation_path,
    }