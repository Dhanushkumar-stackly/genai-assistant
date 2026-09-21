from __future__ import annotations

import time

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)
from pydantic import BaseModel

from .rag_client import (
    EmptyTranscriptError,
    RAGConnectionError,
    clean_transcript,
    get_rag_client,
)
from .transcription import (
    STTProviderError,
    transcribe_audio,
)
from .voice_input import validate_audio_upload
from .voice_logging import (
    VoiceRequestLog,
    redact_transcript,
    write_voice_log,
)


app = FastAPI(
    title="GenAI Assistant - Day 17",
)


class VoiceAskRequest(BaseModel):

    transcript: str

    filters: dict | None = None


@app.get("/")
def root():

    return {
        "message": "Day 17 voice API is running"
    }


@app.post("/voice/transcribe")
async def transcribe(
    file: UploadFile = File(...),
) -> dict:

    total_started = time.perf_counter()

    try:

        audio = await validate_audio_upload(
            file
        )

    except HTTPException as exc:

        write_voice_log(
            VoiceRequestLog(
                request_id="validation-failed",
                stage="audio_validation",
                status="failed",
                error=str(exc.detail),
                total_latency_ms=round(
                    (
                        time.perf_counter()
                        - total_started
                    )
                    * 1000,
                    3,
                ),
            )
        )

        raise

    await file.seek(0)

    audio_bytes = await file.read()

    try:

        stt_result = transcribe_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename,
            content_type=audio.content_type,
        )

    except STTProviderError as exc:

        write_voice_log(
            VoiceRequestLog(
                request_id=audio.request_id,
                filename=audio.filename,
                content_type=audio.content_type,
                size_bytes=audio.size_bytes,
                stage="stt",
                status="failed",
                total_latency_ms=round(
                    (
                        time.perf_counter()
                        - total_started
                    )
                    * 1000,
                    3,
                ),
                error=str(exc),
            )
        )

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    write_voice_log(
        VoiceRequestLog(
            request_id=audio.request_id,
            filename=audio.filename,
            content_type=audio.content_type,
            size_bytes=audio.size_bytes,
            transcript=redact_transcript(
                stt_result.transcript
            ),
            stt_latency_ms=stt_result.latency_ms,
            total_latency_ms=round(
                (
                    time.perf_counter()
                    - total_started
                )
                * 1000,
                3,
            ),
            stage="stt",
            status="success",
        )
    )

    return {
        "request_id": audio.request_id,
        "status": "transcribed",
        "filename": audio.filename,
        "content_type": audio.content_type,
        "size_bytes": audio.size_bytes,
        "transcript": stt_result.transcript,
        "language": stt_result.language,
        "stt_latency_ms": stt_result.latency_ms,
        "provider": stt_result.provider,
    }


@app.post("/voice/ask")
async def voice_ask(
    payload: VoiceAskRequest,
) -> dict:

    total_started = time.perf_counter()
    request_id = f"voice-ask-{int(time.time() * 1000)}"

    rag = get_rag_client()

    try:
        cleaned_transcript = clean_transcript(
            payload.transcript
        )

        result = await rag.ask(
            transcript=cleaned_transcript,
            filters=payload.filters,
        )

    except EmptyTranscriptError as exc:

        write_voice_log(
            VoiceRequestLog(
                request_id=request_id,
                transcript="[EMPTY]",
                stage="transcript_validation",
                status="failed",
                total_latency_ms=round(
                    (
                        time.perf_counter()
                        - total_started
                    )
                    * 1000,
                    3,
                ),
                error=str(exc),
            )
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RAGConnectionError as exc:

        write_voice_log(
            VoiceRequestLog(
                request_id=request_id,
                transcript=redact_transcript(
                    cleaned_transcript
                ),
                stage="rag",
                status="failed",
                total_latency_ms=round(
                    (
                        time.perf_counter()
                        - total_started
                    )
                    * 1000,
                    3,
                ),
                error=str(exc),
            )
        )

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    total_latency = round(
        (
            time.perf_counter()
            - total_started
        )
        * 1000,
        3,
    )

    write_voice_log(
        VoiceRequestLog(
            request_id=request_id,
            transcript=redact_transcript(
                cleaned_transcript
            ),
            rag_latency_ms=result.rag_latency_ms,
            total_latency_ms=total_latency,
            stage="rag",
            status="success",
        )
    )

    return {
        "status": "answered",
        "question": cleaned_transcript,
        "answer": result.answer,
        "sources": result.sources,
        "rag_latency_ms": result.rag_latency_ms,
        "total_latency_ms": total_latency,
    }
@app.post("/voice/input")
async def voice_input(file: UploadFile = File(...)) -> dict:
    audio = await validate_audio_upload(file)

    return {
        "request_id": audio.request_id,
        "status": "accepted",
        "filename": audio.filename,
        "content_type": audio.content_type,
        "size_bytes": audio.size_bytes,
    }

