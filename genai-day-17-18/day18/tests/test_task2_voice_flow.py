from pathlib import Path

import pytest

from day18_app.pipeline import (
    PipelineError,
    run_voice_flow,
)


def test_complete_voice_flow(tmp_path):
    audio = b"RIFF" + b"\x00" * 2048

    result = run_voice_flow(
        audio_bytes=audio,
        filename="question.wav",
        content_type="audio/wav",
        output_dir=tmp_path,
    )

    assert result["status"] == "completed"

    assert result["request_id"]
    assert result["transcript"]
    assert result["answer"]

    assert isinstance(
        result["sources"],
        list,
    )

    assert result["sources"]

    assert result["audio"]["mime_type"] == "audio/wav"
    assert result["audio"]["format"] == "wav"
    assert result["audio"]["synthetic"] is True

    audio_path = Path(
        result["audio"]["path"]
    )

    assert audio_path.exists()
    assert audio_path.stat().st_size > 0


def test_request_id_is_used_for_audio_filename(tmp_path):
    audio = b"RIFF" + b"\x00" * 2048

    result = run_voice_flow(
        audio_bytes=audio,
        filename="question.wav",
        content_type="audio/wav",
        output_dir=tmp_path,
    )

    request_id = result["request_id"]
    audio_path = Path(
        result["audio"]["path"]
    )

    assert request_id in audio_path.name


def test_empty_audio_does_not_call_pipeline(tmp_path):
    with pytest.raises(
        PipelineError,
        match="Audio file is empty",
    ):
        run_voice_flow(
            audio_bytes=b"",
            filename="empty.wav",
            content_type="audio/wav",
            output_dir=tmp_path,
        )


def test_unsupported_audio_does_not_call_stt(tmp_path):
    audio = b"some audio data"

    with pytest.raises(
        PipelineError,
        match="Unsupported audio type",
    ):
        run_voice_flow(
            audio_bytes=audio,
            filename="question.txt",
            content_type="text/plain",
            output_dir=tmp_path,
        )
