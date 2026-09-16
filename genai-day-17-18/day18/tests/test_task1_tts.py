from pathlib import Path

import pytest

from app.tts import (
    GroundedAnswer,
    TTSProviderError,
    synthesize_grounded_answer,
)


def test_tts_generates_wav_from_validated_grounded_answer(
    tmp_path: Path,
):
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
        output_dir=tmp_path,
        request_id="test-valid-answer",
    )

    output_file = Path(result.audio_path)

    assert output_file.exists()
    assert output_file.stat().st_size > 0

    assert result.audio_format == "wav"
    assert result.mime_type == "audio/wav"
    assert result.voice_is_synthetic is True
    assert result.request_id == "test-valid-answer"


def test_tts_rejects_unvalidated_answer(
    tmp_path: Path,
):
    grounded = GroundedAnswer(
        answer="This answer has not been validated.",
        sources=[
            {
                "document_id": "DOC001",
                "title": "Test Document",
            }
        ],
        validated=False,
    )

    with pytest.raises(TTSProviderError) as exc:

        synthesize_grounded_answer(
            grounded=grounded,
            output_dir=tmp_path,
            request_id="test-unvalidated",
        )

    assert "not validated" in str(
        exc.value
    )


def test_tts_rejects_empty_answer(
    tmp_path: Path,
):
    grounded = GroundedAnswer(
        answer="   ",
        sources=[
            {
                "document_id": "DOC001",
                "title": "Test Document",
            }
        ],
        validated=True,
    )

    with pytest.raises(TTSProviderError) as exc:

        synthesize_grounded_answer(
            grounded=grounded,
            output_dir=tmp_path,
            request_id="test-empty-answer",
        )

    assert "empty" in str(
        exc.value
    ).lower()


def test_tts_rejects_answer_without_sources(
    tmp_path: Path,
):
    grounded = GroundedAnswer(
        answer="An answer without source evidence.",
        sources=[],
        validated=True,
    )

    with pytest.raises(TTSProviderError) as exc:

        synthesize_grounded_answer(
            grounded=grounded,
            output_dir=tmp_path,
            request_id="test-no-sources",
        )

    assert "no sources" in str(
        exc.value
    ).lower()