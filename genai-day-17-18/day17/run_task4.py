import json
from pathlib import Path

from day17_app.voice_logging import (
    VoiceRequestLog,
    redact_transcript,
    write_voice_log,
)


entry = VoiceRequestLog(
    request_id="day17-demo-001",
    filename="clear_question.wav",
    content_type="audio/wav",
    size_bytes=104,
    transcript=redact_transcript(
        "What is the leave policy?"
    ),
    stt_latency_ms=820.45,
    rag_latency_ms=315.22,
    total_latency_ms=1135.67,
    stage="complete",
    status="success",
)


write_voice_log(entry)


print("VOICE LOG CREATED")
print(json.dumps(
    entry.__dict__,
    indent=2,
))


log_file = Path(
    "logs/voice_requests.jsonl"
)

print("\nLOG FILE:")
print(log_file)

print("\nLAST LOG ENTRY:")

with log_file.open(
    "r",
    encoding="utf-8",
) as file:

    lines = file.readlines()

    print(
        lines[-1].strip()
    )

