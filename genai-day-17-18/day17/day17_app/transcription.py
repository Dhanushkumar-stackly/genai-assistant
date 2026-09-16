from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Protocol


class STTProviderError(Exception):
    """Raised when the speech-to-text provider fails."""


@dataclass(frozen=True)
class TranscriptionResult:
    transcript: str
    language: str | None
    latency_ms: float
    provider: str


class STTProvider(Protocol):

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> tuple[str, str | None]:
        ...


class DemoSTTProvider:

    name = "demo"

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> tuple[str, str | None]:

        if not audio_bytes:
            raise STTProviderError(
                "STT provider received empty audio"
            )

        # Deterministic demo transcription.
        # Used for local development/testing.
        transcript = (
            "What is the leave policy?"
        )

        return transcript, "en"


class OpenAISTTProvider:

    name = "openai"

    def __init__(self) -> None:

        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise STTProviderError(
                "OPENAI_API_KEY is not configured"
            )

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> tuple[str, str | None]:

        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=self.api_key
            )

            response = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=(
                    filename,
                    audio_bytes,
                    content_type,
                ),
            )

            transcript = getattr(
                response,
                "text",
                "",
            ).strip()

            if not transcript:
                raise STTProviderError(
                    "STT provider returned an empty transcript"
                )

            language = getattr(
                response,
                "language",
                None,
            )

            return transcript, language

        except STTProviderError:
            raise

        except Exception as exc:
            raise STTProviderError(
                f"STT provider error: {exc}"
            ) from exc


def get_stt_provider() -> STTProvider:

    provider_name = os.getenv(
        "STT_PROVIDER",
        "demo",
    ).lower()

    if provider_name == "openai":
        return OpenAISTTProvider()

    if provider_name == "demo":
        return DemoSTTProvider()

    raise STTProviderError(
        f"Unsupported STT provider: {provider_name}"
    )


def transcribe_audio(
    audio_bytes: bytes,
    filename: str,
    content_type: str,
) -> TranscriptionResult:

    provider = get_stt_provider()

    started = time.perf_counter()

    try:

        transcript, language = provider.transcribe(
            audio_bytes=audio_bytes,
            filename=filename,
            content_type=content_type,
        )

    except STTProviderError:
        raise

    except Exception as exc:
        raise STTProviderError(
            f"Unexpected STT failure: {exc}"
        ) from exc

    latency_ms = (
        time.perf_counter() - started
    ) * 1000

    return TranscriptionResult(
        transcript=transcript,
        language=language,
        latency_ms=round(latency_ms, 3),
        provider=provider.name,
    )

