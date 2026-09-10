from eval.report import (
    build_evaluation_report,
    get_overall_score,
    is_evaluation_passed,
)


def test_build_pass_report():
    scorecard = {
        "retrieval_score": 0.83,
        "answer_score": 1.0,
        "overall_score": 0.915,
    }

    regression = {
        "regression_detected": False,
        "threshold": 0.02,
        "metrics": {},
    }

    report = build_evaluation_report(
        scorecard=scorecard,
        regression=regression,
    )

    assert report["status"] == "PASS"
    assert report["scorecard"] == scorecard
    assert report["regression"] == regression


def test_build_regression_report():
    scorecard = {
        "retrieval_score": 0.70,
        "answer_score": 0.80,
        "overall_score": 0.75,
    }

    regression = {
        "regression_detected": True,
        "threshold": 0.02,
        "metrics": {},
    }

    report = build_evaluation_report(
        scorecard=scorecard,
        regression=regression,
    )

    assert report["status"] == "REGRESSION"


def test_passed_report():
    report = {
        "status": "PASS",
        "scorecard": {},
        "regression": {},
    }

    assert is_evaluation_passed(report) is True


def test_regression_report_not_passed():
    report = {
        "status": "REGRESSION",
        "scorecard": {},
        "regression": {},
    }

    assert is_evaluation_passed(report) is False


def test_get_overall_score():
    report = {
        "status": "PASS",
        "scorecard": {
            "overall_score": 0.9166666666666667,
        },
        "regression": {},
    }

    assert get_overall_score(report) == 0.9166666666666667


def test_missing_overall_score():
    report = {
        "status": "PASS",
        "scorecard": {},
        "regression": {},
    }

    assert get_overall_score(report) == 0.0


def test_report_preserves_regression_details():
    regression = {
        "regression_detected": True,
        "threshold": 0.01,
        "metrics": {
            "retrieval_score": {
                "baseline": 0.9,
                "current": 0.8,
                "difference": 0.1,
                "regression": True,
            }
        },
    }

    report = build_evaluation_report(
        scorecard={
            "retrieval_score": 0.8,
            "answer_score": 0.9,
            "overall_score": 0.85,
        },
        regression=regression,
    )

    assert (
        report["regression"]["metrics"]
        == regression["metrics"]
    )