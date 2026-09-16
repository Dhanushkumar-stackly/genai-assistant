import io

from fastapi.testclient import TestClient

from day17_app.main import app
from day17_app.voice_input import MAX_AUDIO_BYTES


client = TestClient(app)


def test_valid_wav_is_accepted():

    response = client.post(
        "/voice/input",
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

    assert body["status"] == "accepted"
    assert body["filename"] == "question.wav"
    assert body["content_type"] == "audio/wav"
    assert body["size_bytes"] == 104


def test_empty_audio_is_rejected():

    response = client.post(
        "/voice/input",
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


def test_unsupported_type_is_rejected():

    response = client.post(
        "/voice/input",
        files={
            "file": (
                "question.txt",
                io.BytesIO(b"hello"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 415


def test_oversized_audio_is_rejected():

    payload = io.BytesIO(
        b"x" * (MAX_AUDIO_BYTES + 1)
    )

    response = client.post(
        "/voice/input",
        files={
            "file": (
                "large.wav",
                payload,
                "audio/wav",
            )
        },
    )

    assert response.status_code == 413

    assert (
        "exceeds maximum size"
        in response.json()["detail"]
    )


def test_mpeg_is_accepted():

    response = client.post(
        "/voice/input",
        files={
            "file": (
                "question.mp3",
                io.BytesIO(
                    b"ID3" + b"1" * 20
                ),
                "audio/mpeg",
            )
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "accepted"
    )

