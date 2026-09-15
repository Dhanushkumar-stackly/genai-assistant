# GenAI Assistant - Day 17

## Topic

Integrate Speech-to-Text with the RAG API.

Day 17 extends the existing GenAI Assistant application with
voice/audio input.

The implementation is divided into five tasks:

1. Create Audio Input Path
2. Implement Speech-to-Text Transcription
3. Connect Transcript to Existing `/ask` Flow
4. Store Stage-Level Logs
5. Create Voice Input Tests

---

# Project Structure

```text
day17/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── voice_input.py
│   └── transcription.py
│
├── tests/
│   ├── test_task1_audio_input.py
│   └── test_task2_transcription.py
│
├── requirements.txt
├── pytest.ini
├── .env.example
├── README.md
└── run_task1.py