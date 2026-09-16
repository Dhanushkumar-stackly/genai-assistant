import json

from day17_app.voice_logging import (
    VoiceRequestLog,
    redact_transcript,
)


def test_voice_log_contains_required_fields():

    entry = VoiceRequestLog(
        request_id="req-001",
        filename="question.wav",
        content_type="audio/wav",
        size_bytes=100,
        transcript="What is the leave policy?",
        stt_latency_ms=100.0,
        rag_latency_ms=200.0,
        total_latency_ms=300.0,
        stage="complete",
        status="success",
    )

    assert entry.request_id == "req-001"
    assert entry.filename == "question.wav"
    assert entry.content_type == "audio/wav"
    assert entry.size_bytes == 100

    assert entry.transcript == (
        "What is the leave policy?"
    )

    assert entry.stt_latency_ms == 100.0
    assert entry.rag_latency_ms == 200.0
    assert entry.total_latency_ms == 300.0

    assert entry.stage == "complete"
    assert entry.status == "success"


def test_transcript_redaction():

    transcript = (
        "My password is secret"
    )

    result = redact_transcript(
        transcript
    )

    assert "password" not in result
    assert "secret" not in result
    assert "[REDACTED]" in result


def test_safe_transcript_is_preserved():

    transcript = (
        "What is the leave policy?"
    )

    result = redact_transcript(
        transcript
    )

    assert result == transcript


def test_failed_stage_is_recorded():

    entry = VoiceRequestLog(
        request_id="req-failed",
        stage="stt",
        status="failed",
        error="STT provider unavailable",
        total_latency_ms=900.0,
    )

    assert entry.stage == "stt"
    assert entry.status == "failed"

    assert (
        entry.error
        == "STT provider unavailable"
    )


def test_log_is_json_serializable():

    entry = VoiceRequestLog(
        request_id="req-json",
        transcript="Hello",
        stage="rag",
        status="success",
        rag_latency_ms=120.5,
    )

    serialized = json.dumps(
        entry.__dict__
    )

    data = json.loads(
        serialized
    )

    assert data["request_id"] == "req-json"
    assert data["rag_latency_ms"] == 120.5

