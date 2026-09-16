"""
Day 16 - Task 3: Application-scoped content and policy checks.

The guard blocks requests to expose restricted information and flags
candidate responses that contain obvious secret/credential material.

The checks are intentionally limited to the application's security scope.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class PolicyDecision:
    """Decision returned by the application policy guard."""

    allowed: bool
    reason_code: str
    matched_rule: str | None = None


# ---------------------------------------------------------
# REQUEST POLICY RULES
# ---------------------------------------------------------
# These rules detect attempts to expose protected information.
# They do NOT block normal policy questions such as:
# "What is the password policy?"
#
REQUEST_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "SYSTEM_INSTRUCTION_EXPOSURE",
        re.compile(
            r"\b(?:reveal|show|print|give|provide|dump|leak|extract)\b"
            r".{0,80}\b(?:system prompt|system instructions|developer message)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "CREDENTIAL_EXPOSURE",
        re.compile(
            r"\b(?:reveal|show|print|give|provide|dump|leak|extract|tell me)\b"
            r".{0,80}\b(?:password|credential|credentials|access token|api key|secret key|private key)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "INTERNAL_SECRET_EXPOSURE",
        re.compile(
            r"\b(?:reveal|show|print|give|provide|dump|leak|extract|tell me)\b"
            r".{0,80}\b(?:internal secret|database password|connection string|security secret)\b",
            re.IGNORECASE,
        ),
    ),
)


# ---------------------------------------------------------
# OUTPUT POLICY RULES
# ---------------------------------------------------------
# Detect common secret/credential formats in candidate
# model output before returning it to the client.
#
OUTPUT_SECRET_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "PRIVATE_KEY_DETECTED",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----"
        ),
    ),
    (
        "AWS_ACCESS_KEY_DETECTED",
        re.compile(
            r"\bAKIA[0-9A-Z]{16}\b"
        ),
    ),
    (
        "BEARER_TOKEN_DETECTED",
        re.compile(
            r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "SECRET_ASSIGNMENT_DETECTED",
        re.compile(
            r"\b(?:password|api[_ -]?key|secret[_ -]?key|access[_ -]?token)"
            r"\s*[:=]\s*\S+",
            re.IGNORECASE,
        ),
    ),
)


def check_request(question: str) -> PolicyDecision:
    """
    Check whether a user request attempts to expose
    restricted information.
    """

    if not isinstance(question, str) or not question.strip():
        return PolicyDecision(
            False,
            "INVALID_REQUEST",
            "REQUEST_TYPE_OR_EMPTY",
        )

    for rule_name, pattern in REQUEST_RULES:
        if pattern.search(question):
            return PolicyDecision(
                False,
                "RESTRICTED_REQUEST",
                rule_name,
            )

    return PolicyDecision(
        True,
        "ALLOWED",
        None,
    )


def check_output(answer: str) -> PolicyDecision:
    """
    Check candidate model output for obvious
    secret or credential material.
    """

    if not isinstance(answer, str) or not answer.strip():
        return PolicyDecision(
            False,
            "INVALID_OUTPUT",
            "OUTPUT_TYPE_OR_EMPTY",
        )

    for rule_name, pattern in OUTPUT_SECRET_RULES:
        if pattern.search(answer):
            return PolicyDecision(
                False,
                "RESTRICTED_OUTPUT",
                rule_name,
            )

    return PolicyDecision(
        True,
        "ALLOWED",
        None,
    )


def apply_policy(
    question: str,
    answer: str | None = None,
) -> PolicyDecision:
    """
    Apply request policy first, then optional output policy.

    A restricted request is blocked before the answer
    is considered.

    A restricted candidate answer is also blocked.
    """

    request_decision = check_request(question)

    if not request_decision.allowed:
        return request_decision

    if answer is not None:
        return check_output(answer)

    return request_decision