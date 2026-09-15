import io

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_clear_audio_voice_path():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "clear_question.wav",
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

    assert body["transcript"] == (
        "What is the leave policy?"
    )


def test_mild_background_noise_audio():

    noisy_audio = (
        b"RIFF"
        + b"\x01\x02\x03\x04" * 50
        + b"NOISE"
    )

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "background_noise.wav",
                io.BytesIO(noisy_audio),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "transcribed"

    assert body["transcript"]


def test_domain_specific_audio():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "domain_terms.wav",
                io.BytesIO(
                    b"RIFF" + b"GENAI" * 20
                ),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "transcribed"

    assert body["transcript"]


def test_empty_audio():

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


def test_unsupported_audio_type():

    response = client.post(
        "/voice/transcribe",
        files={
            "file": (
                "question.txt",
                io.BytesIO(
                    b"this is not audio"
                ),
                "text/plain",
            )
        },
    )

    assert response.status_code == 415
def test_voice_and_text_have_same_grounded_answer(
    monkeypatch,
):

    from app import rag_client

    class FakeResponse:

        def raise_for_status(self):
            pass

        def json(self):

            return {
                "answer": (
                    "Answer based on document: "
                    "Company Leave Policy"
                ),
                "sources": [
                    {
                        "document_id": "leave-001",
                        "title": (
                            "Company Leave Policy"
                        ),
                        "score": 1.0,
                    }
                ],
            }


    class FakeAsyncClient:

        async def __aenter__(self):
            return self

        async def __aexit__(
            self,
            exc_type,
            exc_value,
            traceback,
        ):
            pass

        async def post(
            self,
            url,
            json,
        ):

            assert url.endswith("/ask")

            return FakeResponse()


    monkeypatch.setattr(
        rag_client.httpx,
        "AsyncClient",
        lambda timeout: FakeAsyncClient(),
    )

    import asyncio

    client_instance = (
        rag_client.ExistingRAGClient(
            base_url="http://existing-rag"
        )
    )

    voice_result = asyncio.run(
        client_instance.ask(
            "  What   is   the   leave   policy? "
        )
    )

    text_result = asyncio.run(
        client_instance.ask(
            "What is the leave policy?"
        )
    )

    assert (
        voice_result.answer
        == text_result.answer
    )

    assert (
        voice_result.sources
        == text_result.sources
    )
def test_voice_and_text_use_same_question():
    from app.rag_client import clean_transcript

    voice_transcript = (
        "  What   is   the   leave   policy? "
    )

    text_question = (
        "What is the leave policy?"
    )

    assert (
        clean_transcript(voice_transcript)
        == text_question
    )