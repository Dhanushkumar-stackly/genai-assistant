from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass

import httpx


class RAGConnectionError(Exception):
    """Raised when the existing /ask service cannot be reached."""


class EmptyTranscriptError(Exception):
    """Raised when STT produces no usable question."""


@dataclass(frozen=True)
class RAGAnswer:
    answer: str
    sources: list[dict]
    rag_latency_ms: float


def clean_transcript(transcript: str) -> str:
    """
    Normalize the STT transcript before sending it to /ask.
    """

    if not transcript:
        raise EmptyTranscriptError(
            "Transcript is empty"
        )

    cleaned = re.sub(
        r"\s+",
        " ",
        transcript,
    ).strip()

    if not cleaned:
        raise EmptyTranscriptError(
            "Transcript is empty"
        )

    return cleaned


class ExistingRAGClient:

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:

        self.base_url = (
            base_url
            or os.getenv(
                "RAG_API_URL",
                "http://127.0.0.1:8000",
            )
        ).rstrip("/")

        self.timeout = timeout

    async def ask(
        self,
        transcript: str,
        filters: dict | None = None,
    ) -> RAGAnswer:

        question = clean_transcript(
            transcript
        )

        payload = {
            "question": question,
        }

        if filters is not None:
            payload["filters"] = filters

        started = time.perf_counter()

        try:

            async with httpx.AsyncClient(
                timeout=self.timeout
            ) as client:

                response = await client.post(
                    f"{self.base_url}/ask",
                    json=payload,
                )

                response.raise_for_status()

        except (
            httpx.HTTPError,
            httpx.TimeoutException,
        ) as exc:

            raise RAGConnectionError(
                f"Existing /ask service failed: {exc}"
            ) from exc

        latency_ms = (
            time.perf_counter() - started
        ) * 1000

        data = response.json()

        return RAGAnswer(
            answer=data["answer"],
            sources=data.get(
                "sources",
                [],
            ),
            rag_latency_ms=round(
                latency_ms,
                3,
            ),
        )


rag_client = ExistingRAGClient()


def get_rag_client() -> ExistingRAGClient:
    return rag_client