from fastapi.testclient import TestClient

from src.day11.main import app
from src.day11.metrics import request_metrics


client = TestClient(app)


def test_metrics_endpoint_initially_returns_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "total_requests" in data
    assert "successful_requests" in data
    assert "failed_requests" in data
    assert "average_latency_ms" in data


def test_health_updates_metrics():
    before = request_metrics.total_requests

    response = client.get("/health")

    assert response.status_code == 200

    after = request_metrics.total_requests

    assert after == before + 1
    assert request_metrics.successful_requests >= 1
    assert request_metrics.average_latency_ms >= 0


def test_metrics_endpoint_returns_updated_values():
    client.get("/health")
    client.get("/health")

    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert data["total_requests"] >= 2
    assert data["successful_requests"] >= 2
    assert data["average_latency_ms"] >= 0


def test_unknown_document_counts_as_failed_request():
    before_failed = request_metrics.failed_requests

    response = client.get(
        "/documents/does-not-exist"
    )

    assert response.status_code == 404

    assert (
        request_metrics.failed_requests
        == before_failed + 1
    )