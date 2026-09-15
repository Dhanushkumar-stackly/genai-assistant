from fastapi import FastAPI, File, HTTPException, UploadFile

from .transcription import (
    STTProviderError,
    transcribe_audio,
)
from .voice_input import validate_audio_upload


app = FastAPI(
    title="GenAI Assistant - Day 17",
)


@app.get("/")
def root():
    return {
        "message": "Day 17 voice API is running"
    }


@app.post("/voice/input")
async def voice_input(
    file: UploadFile = File(...),
) -> dict:

    audio = await validate_audio_upload(file)

    return {
        "request_id": audio.request_id,
        "status": "accepted",
        "filename": audio.filename,
        "content_type": audio.content_type,
        "size_bytes": audio.size_bytes,
    }


@app.post("/voice/transcribe")
async def transcribe(
    file: UploadFile = File(...),
) -> dict:

    try:
        audio = await validate_audio_upload(file)

    except HTTPException:
        raise

    await file.seek(0)

    audio_bytes = await file.read()

    try:
        result = transcribe_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename,
            content_type=audio.content_type,
        )

    except STTProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    return {
        "request_id": audio.request_id,
        "status": "transcribed",
        "filename": audio.filename,
        "content_type": audio.content_type,
        "size_bytes": audio.size_bytes,
        "transcript": result.transcript,
        "language": result.language,
        "stt_latency_ms": result.latency_ms,
        "provider": result.provider,
    }