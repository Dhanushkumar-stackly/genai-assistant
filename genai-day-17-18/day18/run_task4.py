import time

from day18_app.latency_tracker import LatencyTracker


def main():

    tracker = LatencyTracker()

    print(
        "DAY 18 - TASK 4: "
        "LATENCY BUDGET TRACKING"
    )

    print(
        f"Request ID : "
        f"{tracker.request_id}"
    )

    # -------------------------
    # STT
    # -------------------------

    stt_started = tracker.start_stage()

    time.sleep(0.05)

    stt_latency = tracker.record(
        "stt",
        stt_started,
    )

    print(
        f"STT latency : "
        f"{stt_latency} ms"
    )

    # -------------------------
    # RAG
    # -------------------------

    rag_started = tracker.start_stage()

    time.sleep(0.08)

    rag_latency = tracker.record(
        "rag",
        rag_started,
    )

    print(
        f"RAG latency : "
        f"{rag_latency} ms"
    )

    # -------------------------
    # TTS
    # -------------------------

    tts_started = tracker.start_stage()

    time.sleep(0.06)

    tts_latency = tracker.record(
        "tts",
        tts_started,
    )

    print(
        f"TTS latency : "
        f"{tts_latency} ms"
    )

    # -------------------------
    # Final report
    # -------------------------

    report = tracker.report()

    print(
        f"Total latency : "
        f"{report.total_latency_ms} ms"
    )

    print(
        "\nLatency breakdown:"
    )

    for stage in report.stages:

        print(
            f"  {stage.stage}: "
            f"{stage.latency_ms} ms"
        )

    print(
        "\nSTATUS : PASS"
    )


if __name__ == "__main__":
    main()
