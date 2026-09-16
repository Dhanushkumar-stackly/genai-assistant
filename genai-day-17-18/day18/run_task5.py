from day18_app.voice_evaluation import (
    VoiceEvaluationCase,
    evaluate_voice_cases,
    build_summary,
    save_report,
)


CASES = [
    VoiceEvaluationCase(
        case_id="voice_01",
        question="What is the leave policy?",
        expected_source_id="DOC001",
    ),
    VoiceEvaluationCase(
        case_id="voice_02",
        question="How do I apply for leave?",
        expected_source_id="DOC001",
    ),
    VoiceEvaluationCase(
        case_id="voice_03",
        question="What documents are required for onboarding?",
        expected_source_id="DOC002",
    ),
    VoiceEvaluationCase(
        case_id="voice_04",
        question="What is the work from home policy?",
        expected_source_id="DOC003",
    ),
    VoiceEvaluationCase(
        case_id="voice_05",
        question="Who approves annual leave?",
        expected_source_id="DOC001",
    ),
]


def fake_voice_function(
    question: str,
    expected_source_id: str,
) -> dict:

    answers = {
        "What is the leave policy?":
            "Employees can take annual leave according to the company leave policy.",

        "How do I apply for leave?":
            "Employees should submit a leave request through the approved process.",

        "What documents are required for onboarding?":
            "New employees must submit the required onboarding documents.",

        "What is the work from home policy?":
            "Employees may work from home according to the company work from home policy.",

        "Who approves annual leave?":
            "Annual leave requests are reviewed through the applicable approval process.",
    }

    return {
        "status": "completed",
        "transcript": question,
        "answer": answers[question],
        "sources": [
            {
                "document_id": expected_source_id,
                "title": f"Document {expected_source_id}",
            }
        ],
        "audio": {
            "path": f"audio/{expected_source_id}.wav",
            "format": "wav",
            "mime_type": "audio/wav",
            "synthetic": True,
        },
        "total_latency_ms": 190.0,
        "failure_stage": None,
    }


def main():

    print(
        "DAY 18 - TASK 5: "
        "VOICE-SPECIFIC EVALUATION"
    )

    results = evaluate_voice_cases(
        CASES,
        fake_voice_function,
    )

    for result in results:

        print(
            f"\n{result.case_id}"
        )

        print(
            f"Question              : "
            f"{result.question}"
        )

        print(
            f"Transcript quality    : "
            f"{'PASS' if result.transcript_quality else 'FAIL'}"
        )

        print(
            f"Task completion       : "
            f"{'PASS' if result.task_completion else 'FAIL'}"
        )

        print(
            f"Citation correctness  : "
            f"{'PASS' if result.citation_correctness else 'FAIL'}"
        )

        print(
            f"Response delay        : "
            f"{result.response_delay_ms} ms"
        )

        print(
            f"Failure stage         : "
            f"{result.failure_stage}"
        )

        print(
            f"Status                : "
            f"{result.status}"
        )

    summary = build_summary(results)

    save_report(
        results,
        "outputs/task5_voice_evaluation.json",
    )

    print("\n" + "=" * 50)
    print("VOICE EVALUATION SUMMARY")
    print("=" * 50)

    print(
        f"Total cases            : "
        f"{summary['total_cases']}"
    )

    print(
        f"Transcript quality     : "
        f"{summary['transcript_quality_pass']}/"
        f"{summary['total_cases']}"
    )

    print(
        f"Task completion        : "
        f"{summary['task_completion_pass']}/"
        f"{summary['total_cases']}"
    )

    print(
        f"Citation correctness   : "
        f"{summary['citation_correctness_pass']}/"
        f"{summary['total_cases']}"
    )

    print(
        f"Overall pass           : "
        f"{summary['overall_pass']}/"
        f"{summary['total_cases']}"
    )

    print(
        f"Average response delay: "
        f"{summary['average_response_delay_ms']} ms"
    )

    print(
        "\nEvaluation report     : "
        "outputs/task5_voice_evaluation.json"
    )

    if (
        summary["overall_pass"]
        == summary["total_cases"]
    ):
        print("\nSTATUS : PASS")
    else:
        print("\nSTATUS : FAIL")


if __name__ == "__main__":
    main()
