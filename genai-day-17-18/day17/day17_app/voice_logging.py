from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "voice_requests.jsonl"


logger = logging.getLogger("voice_pipeline")


if not logger.handlers:

    handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    handler.setFormatter(
        logging.Formatter("%(message)s")
    )

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class VoiceRequestLog:

    request_id: str

    filename: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None

    transcript: str | None = None

    stt_latency_ms: float | None = None
    rag_latency_ms: float | None = None
    total_latency_ms: float | None = None

    stage: str = "input"
    status: str = "started"

    error: str | None = None


def write_voice_log(
    entry: VoiceRequestLog,
) -> None:

    record = asdict(entry)

    logger.info(
        json.dumps(
            record,
            ensure_ascii=False,
        )
    )


def start_request_log(
    request_id: str,
    filename: str,
    content_type: str,
    size_bytes: int,
) -> VoiceRequestLog:

    entry = VoiceRequestLog(
        request_id=request_id,
        filename=filename,
        content_type=content_type,
        size_bytes=size_bytes,
        stage="input",
        status="accepted",
    )

    write_voice_log(entry)

    return entry


def redact_transcript(
    transcript: str,
) -> str:

    """
    Basic redaction for common sensitive fields.

    This is intentionally conservative and does not
    claim to be a complete PII detector.
    """

    replacements = {
        "password": "[REDACTED]",
        "api key": "[REDACTED]",
        "secret": "[REDACTED]",
    }

    redacted = transcript

    for value, replacement in replacements.items():

        redacted = redacted.replace(
            value,
            replacement,
        )

    return redacted


class StageTimer:

    def __init__(
        self,
        stage: str,
    ) -> None:

        self.stage = stage
        self.started = time.perf_counter()

    def elapsed_ms(self) -> float:

        return round(
            (
                time.perf_counter()
                - self.started
            )
            * 1000,
            3,
        )

