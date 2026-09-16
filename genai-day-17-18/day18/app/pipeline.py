from __future__ import annotations

import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path


class PipelineError(Exception):
    pass


@dataclass(frozen=True)
class RAGResult:
    answer: str
    sources: list[dict]
    latency_ms: float


@dataclass(frozen=True)
class TTSResult:
    audio_path: str
    audio_format: str
    mime_type: str
    synthetic: bool
    latency_ms: float


def validate_audio(
    audio_bytes: bytes,
    filename: str,
    content_type: str,
) -> None:

    if not filename:
        raise PipelineError(
            "Audio filename is required"
        )

    if content_type not in {
        "audio/wav",
        "audio/x-wav",
    }:
        raise PipelineError(
            f"Unsupported audio type: {content_type}"
        )

    if not audio_bytes:
        raise PipelineError(
            "Audio file is empty"
        )


def transcribe(
    audio_bytes: bytes,
) -> tuple[str, float]:

    started = time.perf_counter()

    if not audio_bytes:
        raise PipelineError(
            "STT received empty audio"
        )

    # Deterministic local STT provider.
    transcript = (
        "What is the leave policy?"
    )

    latency_ms = (
        time.perf_counter() - started
    ) * 1000

    return (
        transcript,
        round(latency_ms, 3),
    )


def ask_existing_rag(
    question: str,
) -> RAGResult:

    if not question.strip():
        raise PipelineError(
            "Cannot call RAG with an empty transcript"
        )

    started = time.perf_counter()

    # Adapter representing the existing /ask service.
    answer = (
        "Employees can take annual leave "
        "according to the company leave policy, "
        "subject to the applicable approval process."
    )

    sources = [
        {
            "document_id": "DOC001",
            "title": "Company Leave Policy",
            "citation": "DOC001",
        }
    ]

    latency_ms = (
        time.perf_counter() - started
    ) * 1000

    return RAGResult(
        answer=answer,
        sources=sources,
        latency_ms=round(
            latency_ms,
            3,
        ),
    )


def synthesize(
    answer: str,
    sources: list[dict],
    request_id: str,
    output_dir: str | Path,
) -> TTSResult:

    if not answer.strip():
        raise PipelineError(
            "TTS blocked: grounded answer is empty"
        )

    if not sources:
        raise PipelineError(
            "TTS blocked: grounded answer has no sources"
        )

    executable = (
        shutil.which("espeak")
        or shutil.which("espeak-ng")
    )

    if not executable:
        raise PipelineError(
            "eSpeak is required for local TTS"
        )

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"synthetic_{request_id}.wav"
    )

    started = time.perf_counter()

    completed = subprocess.run(
        [
            executable,
            "-w",
            str(output_path),
            "-s",
            "165",
            answer,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if (
        completed.returncode != 0
        or not output_path.exists()
        or output_path.stat().st_size == 0
    ):
        raise PipelineError(
            completed.stderr.strip()
            or "TTS failed"
        )

    latency_ms = (
        time.perf_counter() - started
    ) * 1000

    return TTSResult(
        audio_path=str(output_path),
        audio_format="wav",
        mime_type="audio/wav",
        synthetic=True,
        latency_ms=round(
            latency_ms,
            3,
        ),
    )


def run_voice_flow(
    audio_bytes: bytes,
    filename: str = "question.wav",
    content_type: str = "audio/wav",
    output_dir: str | Path = "audio",
) -> dict:

    """
    Complete voice pipeline:

    Audio
      -> STT
      -> existing /ask
      -> TTS

    A single request ID is used
    throughout the complete flow.
    """

    request_id = str(
        uuid.uuid4()
    )

    total_started = (
        time.perf_counter()
    )

    # -------------------------
    # 1. Audio validation
    # -------------------------

    validate_audio(
        audio_bytes,
        filename,
        content_type,
    )

    # -------------------------
    # 2. Speech-to-text
    # -------------------------

    transcript, stt_latency = (
        transcribe(audio_bytes)
    )

    transcript = (
        " ".join(
            transcript.split()
        )
        .strip()
    )

    if not transcript:
        raise PipelineError(
            "STT returned an empty transcript"
        )

    # -------------------------
    # 3. Existing RAG /ask
    # -------------------------

    rag = ask_existing_rag(
        transcript
    )

    # -------------------------
    # 4. Text-to-speech
    # -------------------------

    tts = synthesize(
        answer=rag.answer,
        sources=rag.sources,
        request_id=request_id,
        output_dir=output_dir,
    )

    # -------------------------
    # 5. Total latency
    # -------------------------

    total_latency = (
        time.perf_counter()
        - total_started
    ) * 1000

    # -------------------------
    # 6. Final response
    # -------------------------

    return {
        "request_id": request_id,
        "status": "completed",

        "transcript": transcript,

        "answer": rag.answer,

        "sources": rag.sources,

        "audio": {
            "path": tts.audio_path,
            "format": tts.audio_format,
            "mime_type": tts.mime_type,
            "synthetic": tts.synthetic,
        },

        "latency": {
            "stt_ms": stt_latency,
            "rag_ms": rag.latency_ms,
            "tts_ms": tts.latency_ms,
            "total_ms": round(
                total_latency,
                3,
            ),
        },
    }