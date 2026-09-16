from dataclasses import dataclass

from day18_app.failure_recovery import (
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


def test_tts_failure_returns_text_answer_and_sources(
    tmp_path,
):

    audio = b"RIFF" + b"\x00" * 100

    rag_called = False

    def fake_stt(audio_bytes):

        return (
            "What is the leave policy?",
            10.0,
        )

    def fake_rag(question):

        nonlocal rag_called

        rag_called = True

        return FakeRAGResult(
            answer=(
                "Employees can take annual leave "
                "according to the company policy."
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
            "TTS service unavailable"
        )

    result = recoverable_voice_flow(
        audio_bytes=audio,
        filename="question.wav",
        content_type="audio/wav",
        stt_function=fake_stt,
        rag_function=fake_rag,
        tts_function=failing_tts,
        output_dir=tmp_path,
    )

    assert rag_called is True

    assert result["status"] == (
        "completed_text_only"
    )

    assert result["failure_stage"] == "tts"

    assert result["answer"] == (
        "Employees can take annual leave "
        "according to the company policy."
    )

    assert result["sources"]

    assert result["audio"] is None

    assert (
        "TTS service unavailable"
        in result["error"]
    )


def test_stt_failure_does_not_call_rag(
    tmp_path,
):

    audio = b"RIFF" + b"\x00" * 100

    rag_called = False

    def failing_stt(audio_bytes):

        raise RuntimeError(
            "STT service unavailable"
        )

    def fake_rag(question):

        nonlocal rag_called

        rag_called = True

        return FakeRAGResult(
            answer="This must not be returned.",
            sources=[],
        )

    def fake_tts(
        answer,
        sources,
        request_id,
        output_dir,
    ):

        return FakeTTSResult(
            audio_path="unused.wav",
            audio_format="wav",
            mime_type="audio/wav",
            synthetic=True,
        )

    result = recoverable_voice_flow(
        audio_bytes=audio,
        filename="question.wav",
        content_type="audio/wav",
        stt_function=failing_stt,
        rag_function=fake_rag,
        tts_function=fake_tts,
        output_dir=tmp_path,
    )

    assert result["status"] == "failed"

    assert result["failure_stage"] == "stt"

    assert result["answer"] is None

    assert result["sources"] == []

    assert result["audio"] is None

    assert rag_called is False


def test_empty_transcript_does_not_call_rag(
    tmp_path,
):

    audio = b"RIFF" + b"\x00" * 100

    rag_called = False

    def empty_stt(audio_bytes):

        return (
            "   ",
            5.0,
        )

    def fake_rag(question):

        nonlocal rag_called

        rag_called = True

        return FakeRAGResult(
            answer="Invalid",
            sources=[],
        )

    def fake_tts(
        answer,
        sources,
        request_id,
        output_dir,
    ):

        return FakeTTSResult(
            audio_path="unused.wav",
            audio_format="wav",
            mime_type="audio/wav",
            synthetic=True,
        )

    result = recoverable_voice_flow(
        audio_bytes=audio,
        filename="question.wav",
        content_type="audio/wav",
        stt_function=empty_stt,
        rag_function=fake_rag,
        tts_function=fake_tts,
        output_dir=tmp_path,
    )

    assert result["status"] == "failed"

    assert result["failure_stage"] == "stt"

    assert result["answer"] is None

    assert rag_called is False
