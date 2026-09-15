import io

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


response = client.post(
    "/voice/transcribe",
    files={
        "file": (
            "clear_question.wav",
            io.BytesIO(
                b"RIFF" + b"0" * 100
            ),
            "audio/wav",
        )
    },
)


print("STATUS:", response.status_code)
print("RESPONSE:")
print(response.json())