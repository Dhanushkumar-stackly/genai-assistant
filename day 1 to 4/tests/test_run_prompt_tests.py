from scripts.run_prompt_tests import (
    TEST_CASES,
    PROMPT_VERSION,
    MODEL_VERSION,
    validate_input,
    run_case,
)


def test_validate_input_valid():
    valid, reason = validate_input("Summarize this document.")

    assert valid is True
    assert reason is None


def test_validate_input_none():
    valid, reason = validate_input(None)

    assert valid is False
    assert reason == "malformed_input"


def test_validate_input_non_string():
    valid, reason = validate_input(12345)

    assert valid is False
    assert reason == "malformed_input"


def test_validate_input_empty():
    valid, reason = validate_input("")

    assert valid is False
    assert reason == "empty_input"


def test_validate_input_whitespace():
    valid, reason = validate_input("   ")

    assert valid is False
    assert reason == "empty_input"


def test_run_case_valid():
    case = {
        "case_id": "test_valid",
        "input": "Summarize this document.",
        "expected_label": "valid",
    }

    result = run_case(case)

    assert result["case_id"] == "test_valid"
    assert result["prompt_version"] == PROMPT_VERSION
    assert result["model_version"] == MODEL_VERSION
    assert result["validation_result"] == "PASS"
    assert result["failure_reason"] is None


def test_run_case_malformed():
    case = {
        "case_id": "test_malformed",
        "input": None,
        "expected_label": "malformed",
    }

    result = run_case(case)

    assert result["validation_result"] == "FAIL"
    assert result["failure_reason"] == "malformed_input"


def test_run_case_empty():
    case = {
        "case_id": "test_empty",
        "input": "",
        "expected_label": "empty",
    }

    result = run_case(case)

    assert result["validation_result"] == "FAIL"
    assert result["failure_reason"] == "empty_input"


def test_all_defined_cases():
    assert len(TEST_CASES) == 10

    for case in TEST_CASES:
        result = run_case(case)

        assert result["case_id"] == case["case_id"]
        assert result["expected_label"] == case["expected_label"]
        assert "latency_ms" in result
        assert result["validation_result"] in {"PASS", "FAIL"}