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
    get_rag_client,
)
from .transcription import (
    STTProviderError,
    transcribe_audio,
)
from .voice_input import validate_audio_upload


app = FastAPI(
    title="GenAI Assistant - Day 17",
)


class VoiceAskRequest(BaseModel):

    transcript: str

    filters: dict | None = None


@app.get("/")
def root():

    return {
        "message": (
            "Day 17 voice API is running"
        )
    }


@app.post("/voice/transcribe")
async def transcribe(
    file: UploadFile = File(...),
) -> dict:

    audio = await validate_audio_upload(
        file
    )

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


@app.post("/voice/ask")
async def voice_ask(
    payload: VoiceAskRequest,
) -> dict:

    rag = get_rag_client()

    try:

        result = await rag.ask(
            transcript=payload.transcript,
            filters=payload.filters,
        )

    except EmptyTranscriptError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RAGConnectionError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    return {
        "status": "answered",
        "question": payload.transcript.strip(),
        "answer": result.answer,
        "sources": result.sources,
        "rag_latency_ms": result.rag_latency_ms,
    }