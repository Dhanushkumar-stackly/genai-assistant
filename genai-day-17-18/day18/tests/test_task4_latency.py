import time

from day18_app.latency_tracker import (
    LatencyTracker,
)


def test_latency_tracker_records_stage():

    tracker = LatencyTracker(
        request_id="test-request-001"
    )

    started = tracker.start_stage()

    time.sleep(0.01)

    latency = tracker.record(
        "stt",
        started,
    )

    assert latency >= 0

    report = tracker.report()

    assert report.request_id == (
        "test-request-001"
    )

    assert len(report.stages) == 1

    assert report.stages[0].stage == (
        "stt"
    )

    assert report.stages[0].latency_ms >= 0


def test_latency_tracker_records_all_voice_stages():

    tracker = LatencyTracker(
        request_id="voice-request-001"
    )

    for stage in (
        "stt",
        "rag",
        "tts",
    ):

        started = tracker.start_stage()

        time.sleep(0.005)

        tracker.record(
            stage,
            started,
        )

    report = tracker.report()

    assert [
        stage.stage
        for stage in report.stages
    ] == [
        "stt",
        "rag",
        "tts",
    ]

    assert report.total_latency_ms >= 0


def test_latency_report_as_dict():

    tracker = LatencyTracker(
        request_id="dict-test-001"
    )

    started = tracker.start_stage()

    tracker.record(
        "stt",
        started,
    )

    data = tracker.report().as_dict()

    assert data["request_id"] == (
        "dict-test-001"
    )

    assert "stages" in data

    assert "stt" in data["stages"]

    assert "total_latency_ms" in data


def test_request_id_remains_consistent():

    tracker = LatencyTracker(
        request_id="same-request-123"
    )

    started = tracker.start_stage()

    tracker.record(
        "stt",
        started,
    )

    started = tracker.start_stage()

    tracker.record(
        "rag",
        started,
    )

    started = tracker.start_stage()

    tracker.record(
        "tts",
        started,
    )

    report = tracker.report()

    assert report.request_id == (
        "same-request-123"
    )
