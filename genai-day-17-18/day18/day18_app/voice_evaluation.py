from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class VoiceEvaluationCase:
    case_id: str
    question: str
    expected_source_id: str


@dataclass
class VoiceEvaluationResult:
    case_id: str
    question: str
    transcript: str | None
    answer: str | None
    sources: list[dict]
    audio: dict | None
    transcript_quality: bool
    task_completion: bool
    citation_correctness: bool
    response_delay_ms: float | None
    failure_stage: str | None
    status: str


def evaluate_voice_cases(
    cases: list[VoiceEvaluationCase],
    voice_function: Callable,
) -> list[VoiceEvaluationResult]:

    results = []

    for case in cases:

        result = voice_function(
            question=case.question,
            expected_source_id=case.expected_source_id,
        )

        transcript = result.get("transcript")
        answer = result.get("answer")
        sources = result.get("sources", [])
        audio = result.get("audio")

        transcript_quality = bool(
            transcript
            and transcript.strip()
        )

        task_completion = bool(
            result.get("status")
            in {"completed", "completed_text_only"}
            and answer
            and answer.strip()
        )

        source_ids = {
            source.get("document_id")
            for source in sources
        }

        citation_correctness = (
            case.expected_source_id in source_ids
        )

        response_delay = result.get(
            "total_latency_ms"
        )

        failure_stage = result.get(
            "failure_stage"
        )

        if task_completion and citation_correctness:
            status = "PASS"
        else:
            status = "FAIL"

        results.append(
            VoiceEvaluationResult(
                case_id=case.case_id,
                question=case.question,
                transcript=transcript,
                answer=answer,
                sources=sources,
                audio=audio,
                transcript_quality=transcript_quality,
                task_completion=task_completion,
                citation_correctness=citation_correctness,
                response_delay_ms=response_delay,
                failure_stage=failure_stage,
                status=status,
            )
        )

    return results


def build_summary(
    results: list[VoiceEvaluationResult],
) -> dict:

    total = len(results)

    transcript_pass = sum(
        result.transcript_quality
        for result in results
    )

    completion_pass = sum(
        result.task_completion
        for result in results
    )

    citation_pass = sum(
        result.citation_correctness
        for result in results
    )

    overall_pass = sum(
        result.status == "PASS"
        for result in results
    )

    latencies = [
        result.response_delay_ms
        for result in results
        if result.response_delay_ms is not None
    ]

    average_latency = (
        round(sum(latencies) / len(latencies), 3)
        if latencies
        else None
    )

    return {
        "total_cases": total,
        "transcript_quality_pass": transcript_pass,
        "task_completion_pass": completion_pass,
        "citation_correctness_pass": citation_pass,
        "overall_pass": overall_pass,
        "average_response_delay_ms": average_latency,
    }


def save_report(
    results: list[VoiceEvaluationResult],
    output_path: str | Path,
) -> None:

    import json

    summary = build_summary(results)

    report = {
        "summary": summary,
        "cases": [
            {
                "case_id": result.case_id,
                "question": result.question,
                "transcript": result.transcript,
                "answer": result.answer,
                "sources": result.sources,
                "audio": result.audio,
                "transcript_quality": result.transcript_quality,
                "task_completion": result.task_completion,
                "citation_correctness": result.citation_correctness,
                "response_delay_ms": result.response_delay_ms,
                "failure_stage": result.failure_stage,
                "status": result.status,
            }
            for result in results
        ],
    }

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )
