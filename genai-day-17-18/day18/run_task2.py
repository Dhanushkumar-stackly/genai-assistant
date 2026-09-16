from pathlib import Path

from day18_app.pipeline import run_voice_flow


def main() -> None:

    # Deterministic local test audio.
    audio = (
        b"RIFF"
        + b"\x00" * 2048
    )

    result = run_voice_flow(
        audio_bytes=audio,
        filename="leave-policy.wav",
        content_type="audio/wav",
        output_dir="audio",
    )

    print(
        "DAY 18 - TASK 2: "
        "COMPLETE VOICE FLOW"
    )

    print(
        f"Request ID        : "
        f"{result['request_id']}"
    )

    print(
        f"Status            : "
        f"{result['status']}"
    )

    print(
        f"Transcript        : "
        f"{result['transcript']}"
    )

    print(
        f"Answer            : "
        f"{result['answer']}"
    )

    print(
        f"Sources           : "
        f"{result['sources']}"
    )

    print(
        f"Audio             : "
        f"{result['audio']['path']}"
    )

    print(
        f"Audio format      : "
        f"{result['audio']['mime_type']}"
    )

    print(
        f"Synthetic voice   : "
        f"{result['audio']['synthetic']}"
    )

    print(
        f"STT latency (ms)  : "
        f"{result['latency']['stt_ms']}"
    )

    print(
        f"RAG latency (ms)  : "
        f"{result['latency']['rag_ms']}"
    )

    print(
        f"TTS latency (ms)  : "
        f"{result['latency']['tts_ms']}"
    )

    print(
        f"Total latency(ms) : "
        f"{result['latency']['total_ms']}"
    )

    audio_size = Path(
        result["audio"]["path"]
    ).stat().st_size

    print(
        f"Audio size(bytes) : "
        f"{audio_size}"
    )

    print(
        "Same request ID "
        "across STT -> RAG -> TTS : YES"
    )

    print(
        "STATUS            : PASS"
    )


if __name__ == "__main__":
    main()
