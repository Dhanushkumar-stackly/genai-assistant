import io

from fastapi.testclient import TestClient

from day17_app.main import app


client = TestClient(app)


def test_valid_audio_is_transcribed():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "question.wav",
                io.BytesIO(
                    b"RIFF" + b"0" * 100
                ),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "transcribed"

    assert (
        body["transcript"]
        == "What is the leave policy?"
    )

    assert body["language"] == "en"

    assert body["provider"] == "demo"

    assert body["stt_latency_ms"] >= 0


def test_mp3_is_transcribed():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "question.mp3",
                io.BytesIO(
                    b"ID3" + b"0" * 100
                ),
                "audio/mpeg",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "transcribed"


def test_empty_audio_is_rejected_before_stt():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "empty.wav",
                io.BytesIO(b""),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Audio file is empty"
    )


def test_unsupported_file_is_rejected():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "question.txt",
                io.BytesIO(b"hello"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 415


def test_stt_latency_is_recorded():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "latency.wav",
                io.BytesIO(
                    b"RIFF" + b"0" * 100
                ),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "stt_latency_ms" in body
    assert isinstance(
        body["stt_latency_ms"],
        (int, float),
    )
    assert body["stt_latency_ms"] >= 0

