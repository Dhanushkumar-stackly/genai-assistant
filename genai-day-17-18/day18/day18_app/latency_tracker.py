from __future__ import annotations

import time
import uuid
from dataclasses import dataclass


@dataclass
class StageLatency:
    stage: str
    latency_ms: float


@dataclass
class LatencyReport:
    request_id: str
    stages: list[StageLatency]
    total_latency_ms: float

    def as_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "stages": {
                item.stage: item.latency_ms
                for item in self.stages
            },
            "total_latency_ms": self.total_latency_ms,
        }


class LatencyTracker:

    def __init__(
        self,
        request_id: str | None = None,
    ) -> None:

        self.request_id = (
            request_id
            or str(uuid.uuid4())
        )

        self.started = time.perf_counter()

        self.stages: list[StageLatency] = []

    def record(
        self,
        stage: str,
        started: float,
    ) -> float:

        latency_ms = (
            time.perf_counter()
            - started
        ) * 1000

        latency_ms = round(
            latency_ms,
            3,
        )

        self.stages.append(
            StageLatency(
                stage=stage,
                latency_ms=latency_ms,
            )
        )

        return latency_ms

    def start_stage(self) -> float:

        return time.perf_counter()

    def total_latency(self) -> float:

        return round(
            (
                time.perf_counter()
                - self.started
            )
            * 1000,
            3,
        )

    def report(self) -> LatencyReport:

        return LatencyReport(
            request_id=self.request_id,
            stages=self.stages.copy(),
            total_latency_ms=self.total_latency(),
        )
