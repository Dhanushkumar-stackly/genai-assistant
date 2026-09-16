from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from pathlib import Path


class STTFailure(Exception):
    """Raised when speech-to-text fails."""


class TTSFailure(Exception):
    """Raised when text-to-speech fails."""


@dataclass(frozen=True)
class RecoveryResult:
    request_id: str
    status: str
    transcript: str | None
    answer: str | None
    sources: list[dict]
    audio: dict | None
    failure_stage: str | None
    error: str | None
    total_latency_ms: float


def recoverable_voice_flow(
    audio_bytes: bytes,
    filename: str,
    content_type: str,
    stt_function,
    rag_function,
    tts_function,
    output_dir: str | Path = "audio",
) -> dict:

    request_id = str(uuid.uuid4())

    total_started = time.perf_counter()

    # ------------------------------------------------
    # 1. Validate audio
    # ------------------------------------------------

    if not audio_bytes:
        raise STTFailure(
            "Audio file is empty"
        )

    # ------------------------------------------------
    # 2. STT
    # ------------------------------------------------

    try:

        transcript, stt_latency = (
            stt_function(audio_bytes)
        )

    except Exception as exc:

        total_latency = (
            time.perf_counter()
            - total_started
        ) * 1000

        return {
            "request_id": request_id,
            "status": "failed",
            "transcript": None,
            "answer": None,
            "sources": [],
            "audio": None,
            "failure_stage": "stt",
            "error": str(exc),
            "total_latency_ms": round(
                total_latency,
                3,
            ),
        }

    # ------------------------------------------------
    # 3. Validate transcript
    # ------------------------------------------------

    if not transcript or not transcript.strip():

        total_latency = (
            time.perf_counter()
            - total_started
        ) * 1000

        return {
            "request_id": request_id,
            "status": "failed",
            "transcript": None,
            "answer": None,
            "sources": [],
            "audio": None,
            "failure_stage": "stt",
            "error": (
                "STT returned an empty transcript"
            ),
            "total_latency_ms": round(
                total_latency,
                3,
            ),
        }

    transcript = " ".join(
        transcript.split()
    ).strip()

    # ------------------------------------------------
    # 4. RAG
    # ------------------------------------------------

    try:

        rag_result = rag_function(
            transcript
        )

    except Exception as exc:

        total_latency = (
            time.perf_counter()
            - total_started
        ) * 1000

        return {
            "request_id": request_id,
            "status": "failed",
            "transcript": transcript,
            "answer": None,
            "sources": [],
            "audio": None,
            "failure_stage": "rag",
            "error": str(exc),
            "total_latency_ms": round(
                total_latency,
                3,
            ),
        }

    answer = rag_result.answer
    sources = rag_result.sources

    # ------------------------------------------------
    # 5. TTS
    # ------------------------------------------------

    try:

        tts_result = tts_function(
            answer=answer,
            sources=sources,
            request_id=request_id,
            output_dir=output_dir,
        )

        audio = {
            "path": tts_result.audio_path,
            "format": tts_result.audio_format,
            "mime_type": tts_result.mime_type,
            "synthetic": tts_result.synthetic,
        }

        status = "completed"
        failure_stage = None
        error = None

    except Exception as exc:

        # --------------------------------------------
        # TTS failure recovery
        # --------------------------------------------

        audio = None

        status = "completed_text_only"

        failure_stage = "tts"

        error = str(exc)

    # ------------------------------------------------
    # 6. Total latency
    # ------------------------------------------------

    total_latency = (
        time.perf_counter()
        - total_started
    ) * 1000

    # ------------------------------------------------
    # 7. Return result
    # ------------------------------------------------

    return {
        "request_id": request_id,
        "status": status,
        "transcript": transcript,
        "answer": answer,
        "sources": sources,
        "audio": audio,
        "failure_stage": failure_stage,
        "error": error,
        "total_latency_ms": round(
            total_latency,
            3,
        ),
    }
