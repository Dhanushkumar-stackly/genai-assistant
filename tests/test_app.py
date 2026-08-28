
from fastapi.testclient import TestClient

from src.day11.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Day 11 API is running"
    }
