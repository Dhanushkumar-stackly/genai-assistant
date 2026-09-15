from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_audio():
    """
    Create a small valid WAV-like test file for Task 1.
    The Task 1 validation checks the audio content type,
    filename, size, and non-empty content.
    """
    audio_path = Path("sample_question.wav")

    # Minimal non-empty test bytes.
    audio_bytes = (
        b"RIFF"
        + (36).to_bytes(4, "little")
        + b"WAVE"
        + b"fmt "
        + (16).to_bytes(4, "little")
        + (1).to_bytes(2, "little")
        + (1).to_bytes(2, "little")
        + (16000).to_bytes(4, "little")
        + (32000).to_bytes(4, "little")
        + (2).to_bytes(2, "little")
        + (16).to_bytes(2, "little")
        + b"data"
        + (0).to_bytes(4, "little")
    )

    audio_path.write_bytes(audio_bytes)

    return audio_path


def run_task1_demo():
    print("=" * 60)
    print("DAY 17 - TASK 1 : AUDIO INPUT DEMO")
    print("=" * 60)

    audio_path = create_test_audio()

    print(f"\nAudio file created : {audio_path}")
    print(f"Audio file size    : {audio_path.stat().st_size} bytes")

    with audio_path.open("rb") as audio_file:
        response = client.post(
            "/voice/input",
            files={
                "file": (
                    "sample_question.wav",
                    audio_file,
                    "audio/wav",
                )
            },
        )

    print("\nHTTP Status:", response.status_code)
    print("Response:")
    print(response.json())

    if response.status_code == 200:
        print("\nTASK 1 AUDIO INPUT SUCCESS")
    else:
        print("\nTASK 1 AUDIO INPUT FAILED")

    audio_path.unlink(missing_ok=True)


if __name__ == "__main__":
    run_task1_demo()