import json
import time
from pathlib import Path


PROMPT_VERSION = "v1"
MODEL_VERSION = "test-model-v1"

TEST_CASES = [
    {
        "case_id": "case_01",
        "input": "Summarize this document.",
        "expected_label": "valid",
    },
    {
        "case_id": "case_02",
        "input": "Classify this text.",
        "expected_label": "valid",
    },
    {
        "case_id": "case_03",
        "input": "What does this mean?",
        "expected_label": "ambiguous",
    },
    {
        "case_id": "case_04",
        "input": "Can you process this?",
        "expected_label": "ambiguous",
    },
    {
        "case_id": "case_05",
        "input": None,
        "expected_label": "malformed",
    },
    {
        "case_id": "case_06",
        "input": 12345,
        "expected_label": "malformed",
    },
    {
        "case_id": "case_07",
        "input": "",
        "expected_label": "empty",
    },
    {
        "case_id": "case_08",
        "input": "   ",
        "expected_label": "empty",
    },
    {
        "case_id": "case_09",
        "input": "Give a short summary of the text.",
        "expected_label": "valid",
    },
    {
        "case_id": "case_10",
        "input": "Please classify this document.",
        "expected_label": "valid",
    },
]


def validate_input(value):
    """Validate the test input and return a failure category if invalid."""

    if value is None:
        return False, "malformed_input"

    if not isinstance(value, str):
        return False, "malformed_input"

    if not value.strip():
        return False, "empty_input"

    return True, None


def run_case(case):
    """Run one prompt test case."""

    start_time = time.perf_counter()

    valid, failure_reason = validate_input(case["input"])

    if valid:
        validation_result = "PASS"
        failure_reason = None
    else:
        validation_result = "FAIL"

    latency_ms = round(
        (time.perf_counter() - start_time) * 1000,
        3,
    )

    return {
        "case_id": case["case_id"],
        "prompt_version": PROMPT_VERSION,
        "model_version": MODEL_VERSION,
        "latency_ms": latency_ms,
        "validation_result": validation_result,
        "failure_reason": failure_reason,
        "expected_label": case["expected_label"],
    }


def main():
    print("=" * 60)
    print("PROMPT TEST RUNNER")
    print("=" * 60)

    results = []

    for case in TEST_CASES:
        result = run_case(case)
        results.append(result)

        print()
        print(f"Case ID: {result['case_id']}")
        print(f"Expected Label: {result['expected_label']}")
        print(f"Prompt Version: {result['prompt_version']}")
        print(f"Model Version: {result['model_version']}")
        print(f"Latency: {result['latency_ms']} ms")
        print(f"Validation: {result['validation_result']}")

        if result["failure_reason"]:
            print(f"Failure Reason: {result['failure_reason']}")

    passed = sum(
        1
        for result in results
        if result["validation_result"] == "PASS"
    )

    failed = len(results) - passed

    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "prompt_test_results.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "prompt_version": PROMPT_VERSION,
                "model_version": MODEL_VERSION,
                "total_cases": len(results),
                "passed": passed,
                "failed": failed,
                "results": results,
            },
            file,
            indent=2,
        )

    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Cases: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Result File: {output_file}")


if __name__ == "__main__":
    main()