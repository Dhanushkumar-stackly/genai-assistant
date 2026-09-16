from app.voice_evaluation import (
    VoiceEvaluationCase,
    evaluate_voice_cases,
    build_summary,
)


def fake_voice_function(
    question: str,
    expected_source_id: str,
) -> dict:

    return {
        "status": "completed",
        "transcript": question,
        "answer": "Validated grounded answer.",
        "sources": [
            {
                "document_id": expected_source_id,
                "title": "Test document",
            }
        ],
        "audio": {
            "path": "audio/test.wav",
            "format": "wav",
            "mime_type": "audio/wav",
            "synthetic": True,
        },
        "total_latency_ms": 100.0,
        "failure_stage": None,
    }


def test_five_voice_cases_are_evaluated():

    cases = [
        VoiceEvaluationCase(
            case_id=f"voice_{index}",
            question=f"Question {index}",
            expected_source_id="DOC001",
        )
        for index in range(1, 6)
    ]

    results = evaluate_voice_cases(
        cases,
        fake_voice_function,
    )

    assert len(results) == 5

    assert all(
        result.status == "PASS"
        for result in results
    )


def test_transcript_quality_is_recorded():

    case = VoiceEvaluationCase(
        case_id="voice_01",
        question="What is the leave policy?",
        expected_source_id="DOC001",
    )

    result = evaluate_voice_cases(
        [case],
        fake_voice_function,
    )[0]

    assert result.transcript_quality is True


def test_citation_correctness_is_checked():

    case = VoiceEvaluationCase(
        case_id="voice_01",
        question="What is the leave policy?",
        expected_source_id="DOC001",
    )

    result = evaluate_voice_cases(
        [case],
        fake_voice_function,
    )[0]

    assert result.citation_correctness is True


def test_evaluation_summary():

    cases = [
        VoiceEvaluationCase(
            case_id=f"voice_{index}",
            question=f"Question {index}",
            expected_source_id="DOC001",
        )
        for index in range(1, 6)
    ]

    results = evaluate_voice_cases(
        cases,
        fake_voice_function,
    )

    summary = build_summary(results)

    assert summary["total_cases"] == 5
    assert summary["transcript_quality_pass"] == 5
    assert summary["task_completion_pass"] == 5
    assert summary["citation_correctness_pass"] == 5
    assert summary["overall_pass"] == 5