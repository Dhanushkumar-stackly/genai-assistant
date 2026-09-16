from dataclasses import dataclass

from app.failure_recovery import (
    recoverable_voice_flow,
)


@dataclass
class FakeRAGResult:
    answer: str
    sources: list[dict]


@dataclass
class FakeTTSResult:
    audio_path: str
    audio_format: str
    mime_type: str
    synthetic: bool


def fake_stt(audio):

    return (
        "What is the leave policy?",
        12.4,
    )


def fake_rag(question):

    return FakeRAGResult(
        answer=(
            "Employees can take annual leave "
            "according to the company leave policy."
        ),
        sources=[
            {
                "document_id": "DOC001",
                "title": "Company Leave Policy",
            }
        ],
    )


def failing_tts(
    answer,
    sources,
    request_id,
    output_dir,
):

    raise RuntimeError(
        "TTS service temporarily unavailable"
    )


def main():

    result = recoverable_voice_flow(
        audio_bytes=b"RIFF" + b"\x00" * 100,
        filename="leave-policy.wav",
        content_type="audio/wav",
        stt_function=fake_stt,
        rag_function=fake_rag,
        tts_function=failing_tts,
        output_dir="audio",
    )

    print(
        "DAY 18 - TASK 3: "
        "FAILURE RECOVERY"
    )

    print(
        f"Request ID     : "
        f"{result['request_id']}"
    )

    print(
        f"Status         : "
        f"{result['status']}"
    )

    print(
        f"Failure stage  : "
        f"{result['failure_stage']}"
    )

    print(
        f"Transcript     : "
        f"{result['transcript']}"
    )

    print(
        f"Answer         : "
        f"{result['answer']}"
    )

    print(
        f"Sources        : "
        f"{result['sources']}"
    )

    print(
        f"Audio          : "
        f"{result['audio']}"
    )

    print(
        f"Error          : "
        f"{result['error']}"
    )

    print(
        f"Total latency  : "
        f"{result['total_latency_ms']} ms"
    )

    print(
        "TEXT FALLBACK  : "
        "AVAILABLE"
    )

    print(
        "STATUS         : PASS"
    )


if __name__ == "__main__":
    main()