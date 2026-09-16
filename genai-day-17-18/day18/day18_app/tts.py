from __future__ import annotations

import os
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class TTSProviderError(Exception):
    """Raised when the selected TTS provider cannot synthesize audio."""


@dataclass(frozen=True)
class GroundedAnswer:
    """Validated answer produced by the existing grounded RAG flow."""

    answer: str
    sources: list[dict]
    validated: bool = True


@dataclass(frozen=True)
class TTSResult:
    request_id: str
    audio_path: str
    audio_format: str
    mime_type: str
    provider: str
    voice_is_synthetic: bool
    latency_ms: float


class TTSProvider(Protocol):
    name: str
    synthetic: bool

    def synthesize(
        self,
        text: str,
        output_path: Path,
    ) -> None:
        ...


class DemoTTSProvider:
    """Local deterministic TTS provider using eSpeak."""

    name = "demo-espeak"
    synthetic = True

    def synthesize(
        self,
        text: str,
        output_path: Path,
    ) -> None:

        executable = (
            shutil.which("espeak")
            or shutil.which("espeak-ng")
        )

        if not executable:
            raise TTSProviderError(
                "Demo TTS requires "
                "'espeak' or 'espeak-ng' "
                "to be installed"
            )

        command = [
            executable,
            "-w",
            str(output_path),
            "-s",
            os.getenv(
                "DEMO_TTS_SPEED",
                "165",
            ),
            text,
        ]

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if (
            completed.returncode != 0
            or not output_path.exists()
        ):
            detail = (
                completed.stderr.strip()
                or "unknown eSpeak error"
            )

            raise TTSProviderError(
                f"Demo TTS failed: {detail}"
            )


class OpenAITTSProvider:
    """Production TTS provider."""

    name = "openai-gpt-4o-mini-tts"
    synthetic = True

    def __init__(self) -> None:

        self.api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not self.api_key:
            raise TTSProviderError(
                "OPENAI_API_KEY is not configured"
            )

    def synthesize(
        self,
        text: str,
        output_path: Path,
    ) -> None:

        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=self.api_key
            )

            response = client.audio.speech.create(
                model=os.getenv(
                    "TTS_MODEL",
                    "gpt-4o-mini-tts",
                ),
                voice=os.getenv(
                    "TTS_VOICE",
                    "alloy",
                ),
                input=text,
                response_format="wav",
            )

            response.write_to_file(
                str(output_path)
            )

        except TTSProviderError:
            raise

        except Exception as exc:
            raise TTSProviderError(
                f"OpenAI TTS provider error: {exc}"
            ) from exc


def get_tts_provider() -> TTSProvider:

    provider = os.getenv(
        "TTS_PROVIDER",
        "demo",
    ).lower()

    if provider == "demo":
        return DemoTTSProvider()

    if provider == "openai":
        return OpenAITTSProvider()

    raise TTSProviderError(
        f"Unsupported TTS provider: {provider}"
    )


def _validate_grounded_answer(
    grounded: GroundedAnswer,
) -> str:

    if not grounded.validated:
        raise TTSProviderError(
            "TTS blocked: answer is not validated"
        )

    answer = grounded.answer.strip()

    if not answer:
        raise TTSProviderError(
            "TTS blocked: grounded answer is empty"
        )

    if not grounded.sources:
        raise TTSProviderError(
            "TTS blocked: grounded answer has no sources"
        )

    return answer


def synthesize_grounded_answer(
    grounded: GroundedAnswer,
    output_dir: str | Path = "audio",
    request_id: str | None = None,
) -> TTSResult:

    answer = _validate_grounded_answer(
        grounded
    )

    request_id = (
        request_id
        or str(uuid.uuid4())
    )

    output_directory = Path(
        output_dir
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory
        / f"synthetic_{request_id}.wav"
    )

    provider = get_tts_provider()

    started = time.perf_counter()

    try:

        provider.synthesize(
            answer,
            output_path,
        )

    except TTSProviderError:
        raise

    except Exception as exc:

        raise TTSProviderError(
            f"Unexpected TTS failure: {exc}"
        ) from exc

    if (
        not output_path.exists()
        or output_path.stat().st_size == 0
    ):
        raise TTSProviderError(
            "TTS provider produced "
            "an empty audio file"
        )

    return TTSResult(
        request_id=request_id,
        audio_path=str(output_path),
        audio_format="wav",
        mime_type="audio/wav",
        provider=provider.name,
        voice_is_synthetic=provider.synthetic,
        latency_ms=round(
            (
                time.perf_counter()
                - started
            )
            * 1000,
            3,
        ),
    )
