from pathlib import Path

from src.day10.task5_before_after_report import (
    build_metric_summary,
    compare_questions,
    choose_configuration,
    create_text_report,
)


def test_baseline_and_experiment_metrics():

    baseline = {
        "retrieval_recall": 0.8000,
        "top1_accuracy": 0.6000,
        "mrr": 0.6700,
        "average_latency_ms": 0.81,
    }

    experiment = {
        "retrieval_recall": 0.8667,
        "top1_accuracy": 0.6333,
        "mrr": 0.7117,
        "average_latency_ms": 1.06,
    }

    summary = build_metric_summary(
        baseline,
        experiment,
    )

    assert summary["baseline"]["retrieval_recall"] == 0.8000
    assert summary["experiment"]["retrieval_recall"] == 0.8667


def test_metric_changes():

    baseline = {
        "retrieval_recall": 0.8000,
        "top1_accuracy": 0.6000,
        "mrr": 0.6700,
        "average_latency_ms": 0.81,
    }

    experiment = {
        "retrieval_recall": 0.8667,
        "top1_accuracy": 0.6333,
        "mrr": 0.7117,
        "average_latency_ms": 1.06,
    }

    summary = build_metric_summary(
        baseline,
        experiment,
    )

    assert round(
        summary["change"]["retrieval_recall"],
        4,
    ) == 0.0667

    assert round(
        summary["change"]["top1_accuracy"],
        4,
    ) == 0.0333

    assert round(
        summary["change"]["mrr"],
        4,
    ) == 0.0417

    assert round(
        summary["change"]["average_latency_ms"],
        2,
    ) == 0.25


def test_improved_question_is_detected():

    baseline = [
        {
            "question_number": 1,
            "question": "Test question",
            "retrieval_success": False,
            "top1": False,
            "rank": None,
            "latency_ms": 1.0,
        }
    ]

    experiment = [
        {
            "question_number": 1,
            "question": "Test question",
            "retrieval_success": True,
            "top1": True,
            "rank": 1,
            "latency_ms": 1.2,
        }
    ]

    result = compare_questions(
        baseline,
        experiment,
    )

    assert len(result) == 1
    assert result[0]["outcome"] == "improved"


def test_regressed_question_is_detected():

    baseline = [
        {
            "question_number": 1,
            "question": "Test question",
            "retrieval_success": True,
            "top1": True,
            "rank": 1,
            "latency_ms": 1.0,
        }
    ]

    experiment = [
        {
            "question_number": 1,
            "question": "Test question",
            "retrieval_success": False,
            "top1": False,
            "rank": None,
            "latency_ms": 1.2,
        }
    ]

    result = compare_questions(
        baseline,
        experiment,
    )

    assert len(result) == 1
    assert result[0]["outcome"] == "regressed"


def test_tradeoff_selects_experiment_when_improved():

    summary = {
        "baseline": {
            "retrieval_recall": 0.8000,
            "top1_accuracy": 0.6000,
            "mrr": 0.6700,
            "average_latency_ms": 0.81,
        },
        "experiment": {
            "retrieval_recall": 0.8667,
            "top1_accuracy": 0.6333,
            "mrr": 0.7117,
            "average_latency_ms": 1.06,
        },
        "change": {
            "retrieval_recall": 0.0667,
            "top1_accuracy": 0.0333,
            "mrr": 0.0417,
            "average_latency_ms": 0.25,
        },
    }

    comparison = [
        {
            "question_number": 1,
            "question": "Test",
            "baseline_retrieval_success": False,
            "baseline_top1": False,
            "baseline_rank": None,
            "experiment_retrieval_success": True,
            "experiment_top1": True,
            "experiment_rank": 1,
            "baseline_latency_ms": 0.8,
            "experiment_latency_ms": 1.0,
            "outcome": "improved",
        }
    ]

    decision = choose_configuration(
        summary,
        comparison,
    )

    assert decision["selected_configuration"] == "experiment"
    assert decision["accepted"] is True


def test_tradeoff_rejects_experiment_when_regressions_are_high():

    summary = {
        "baseline": {
            "retrieval_recall": 0.9000,
            "top1_accuracy": 0.8000,
            "mrr": 0.8500,
            "average_latency_ms": 0.80,
        },
        "experiment": {
            "retrieval_recall": 0.9100,
            "top1_accuracy": 0.6000,
            "mrr": 0.7000,
            "average_latency_ms": 1.50,
        },
        "change": {
            "retrieval_recall": 0.0100,
            "top1_accuracy": -0.2000,
            "mrr": -0.1500,
            "average_latency_ms": 0.70,
        },
    }

    comparison = [
        {
            "question_number": 1,
            "question": "Good question",
            "baseline_retrieval_success": True,
            "baseline_top1": True,
            "baseline_rank": 1,
            "experiment_retrieval_success": False,
            "experiment_top1": False,
            "experiment_rank": None,
            "baseline_latency_ms": 0.8,
            "experiment_latency_ms": 1.5,
            "outcome": "regressed",
        }
    ]

    decision = choose_configuration(
        summary,
        comparison,
    )

    assert decision["selected_configuration"] == "baseline"
    assert decision["accepted"] is False


def test_report_contains_required_sections():

    baseline = {
        "retrieval_recall": 0.8000,
        "top1_accuracy": 0.6000,
        "mrr": 0.6700,
        "average_latency_ms": 0.81,
    }

    experiment = {
        "retrieval_recall": 0.8667,
        "top1_accuracy": 0.6333,
        "mrr": 0.7117,
        "average_latency_ms": 1.06,
    }

    summary = build_metric_summary(
        baseline,
        experiment,
    )

    comparison = []

    decision = choose_configuration(
        summary,
        comparison,
    )

    # configuration intentionally omitted
    # to verify optional-field handling
    rejected = [
        {
            "approach": "top_k = 10",
            "status": "rejected",
            "reason": "No retrieval improvement",
        }
    ]

    report = create_text_report(
        summary,
        comparison,
        decision,
        rejected,
    )

    assert "DAY 10 - TASK 5" in report
    assert "BEFORE-AND-AFTER EXPERIMENT REPORT" in report
    assert "AGGREGATE METRICS" in report
    assert "PER-QUESTION RESULTS" in report
    assert "TRADE-OFF ANALYSIS" in report
    assert "SELECTED CONFIGURATION" in report
    assert "REJECTED APPROACHES" in report
    assert "top_k = 10" in report
    assert "No retrieval improvement" in report


def test_task5_output_files_exist_after_execution():

    output_dir = Path("outputs")

    assert output_dir.exists()

    possible_files = [
        output_dir / "day10_task5_before_after_report.txt",
        output_dir / "day10_task5_before_after_report.json",
        output_dir / "day10_task5_report.txt",
        output_dir / "day10_task5_report.json",
    ]

    assert any(
        file.exists()
        for file in possible_files
    )