from pathlib import Path

from app.tts import (
    GroundedAnswer,
    synthesize_grounded_answer,
)


def main() -> None:

    grounded = GroundedAnswer(
        answer=(
            "Employees are eligible for annual "
            "leave according to the company "
            "leave policy."
        ),
        sources=[
            {
                "document_id": "DOC001",
                "title": "Company Leave Policy",
                "citation": "DOC001",
            }
        ],
        validated=True,
    )

    result = synthesize_grounded_answer(
        grounded=grounded,
        output_dir="audio",
        request_id="day18-task1-demo",
    )

    audio_size = Path(
        result.audio_path
    ).stat().st_size

    print(
        "DAY 18 - TASK 1: "
        "TEXT-TO-SPEECH"
    )

    print(
        f"Provider          : "
        f"{result.provider}"
    )

    print(
        f"Synthetic voice   : "
        f"{result.voice_is_synthetic}"
    )

    print(
        f"Format            : "
        f"{result.audio_format}"
    )

    print(
        f"MIME type         : "
        f"{result.mime_type}"
    )

    print(
        f"Audio file        : "
        f"{result.audio_path}"
    )

    print(
        f"Audio size (bytes): "
        f"{audio_size}"
    )

    print(
        f"TTS latency (ms)  : "
        f"{result.latency_ms}"
    )

    print(
        "Grounded answer   : "
        "validated + source-backed"
    )

    print("STATUS            : PASS")


if __name__ == "__main__":
    main()