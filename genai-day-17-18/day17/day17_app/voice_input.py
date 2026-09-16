from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Final

from fastapi import APIRouter, File, HTTPException, UploadFile


MAX_AUDIO_BYTES: Final[int] = 5 * 1024 * 1024

ALLOWED_CONTENT_TYPES: Final[set[str]] = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/x-m4a",
    "audio/webm",
}


router = APIRouter(
    prefix="/voice",
    tags=["voice"],
)


@dataclass(frozen=True)
class AudioInput:
    request_id: str
    filename: str
    content_type: str
    size_bytes: int
    received_ms: float


async def validate_audio_upload(
    upload: UploadFile,
) -> AudioInput:

    request_id = str(uuid.uuid4())

    started = time.perf_counter()

    # Filename validation
    if not upload.filename:
        raise HTTPException(
            status_code=400,
            detail="Audio filename is required",
        )

    # Content-Type validation
    content_type = (
        upload.content_type or ""
    ).lower()

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=(
                "Unsupported audio type: "
                f"{content_type or 'missing'}"
            ),
        )

    # Size validation
    size = 0

    while True:

        chunk = await upload.read(1024 * 1024)

        if not chunk:
            break

        size += len(chunk)

        if size > MAX_AUDIO_BYTES:
            raise HTTPException(
                status_code=413,
                detail=(
                    "Audio exceeds maximum size "
                    f"of {MAX_AUDIO_BYTES} bytes"
                ),
            )

    # Empty file validation
    if size == 0:
        raise HTTPException(
            status_code=400,
            detail="Audio file is empty",
        )

    received_ms = (
        time.perf_counter() - started
    ) * 1000

    return AudioInput(
        request_id=request_id,
        filename=upload.filename,
        content_type=content_type,
        size_bytes=size,
        received_ms=round(received_ms, 3),
    )


@router.post("/input")
async def audio_input(
    file: UploadFile = File(...),
) -> dict:

    audio = await validate_audio_upload(file)

    return {
        "request_id": audio.request_id,
        "status": "accepted",
        "filename": audio.filename,
        "content_type": audio.content_type,
        "size_bytes": audio.size_bytes,
        "message": (
            "Audio input accepted for "
            "the speech-to-text stage"
        ),
    }

