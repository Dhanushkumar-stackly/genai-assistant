import io
import os

from fastapi.testclient import TestClient

from day17_app.main import app


os.environ["STT_PROVIDER"] = "demo"


client = TestClient(app)


print("=" * 60)
print("DAY 17 - TASK 5")
print("VOICE INPUT END-TO-END TEST")
print("=" * 60)


print("\n[1] CLEAR AUDIO")

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

print("Status:", response.status_code)
print("Transcript:")
print(
    response.json().get(
        "transcript"
    )
)


print("\n[2] MILD BACKGROUND NOISE")

response = client.post(
    "/voice/transcribe",
    files={
        "file": (
            "background_noise.wav",
            io.BytesIO(
                b"RIFF"
                + b"\x01\x02" * 100
            ),
            "audio/wav",
        )
    },
)

print("Status:", response.status_code)
print("Transcript:")
print(
    response.json().get(
        "transcript"
    )
)


print("\n[3] DOMAIN-SPECIFIC AUDIO")

response = client.post(
    "/voice/transcribe",
    files={
        "file": (
            "domain_terms.wav",
            io.BytesIO(
                b"RIFF"
                + b"GENAI" * 20
            ),
            "audio/wav",
        )
    },
)

print("Status:", response.status_code)
print("Transcript:")
print(
    response.json().get(
        "transcript"
    )
)


print("\n[4] EMPTY AUDIO")

response = client.post(
    "/voice/transcribe",
    files={
        "file": (
            "empty.wav",
            io.BytesIO(b""),
            "audio/wav",
        )
    },
)

print("Status:", response.status_code)
print("Error:")
print(
    response.json().get(
        "detail"
    )
)


print("\n[5] UNSUPPORTED FILE")

response = client.post(
    "/voice/transcribe",
    files={
        "file": (
            "question.txt",
            io.BytesIO(
                b"not an audio file"
            ),
            "text/plain",
        )
    },
)

print("Status:", response.status_code)
print("Error:")
print(
    response.json().get(
        "detail"
    )
)


print("\n" + "=" * 60)
print("TASK 5 RUNTIME VERIFICATION COMPLETE")
print("=" * 60)

