# GenAI Assistant - Operations Guide

## 1. Overview

This document describes the complete operational workflow
for the GenAI Assistant.

The system supports:

- Document ingestion
- Retrieval-Augmented Generation
- Question answering
- Source citations
- Evaluation
- Adversarial testing
- Voice input/output

---

# 2. Prerequisites

Required:

- Python 3.x
- Git
- PowerShell
- Virtual environment support

Verify:

python --version

git --version

---

# 3. Clone

git clone <repository-url>

cd <repository-directory>

---

# 4. Create Virtual Environment

python -m venv venv

Activate:

.\venv\Scripts\Activate.ps1

---

# 5. Install Dependencies

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

---

# 6. Configuration

Configure required environment variables before startup.

Do not commit secrets.

Use:

.env

for local configuration.

---

# 7. Start RAG API

The RAG API provides:

- /health
- /ingest
- /ask
- /docs
- /openapi.json

Start:

python -m uvicorn src.day11.main:app --reload

Default:

http://127.0.0.1:8000

---

# 8. Health Check

Run:

Invoke-RestMethod http://127.0.0.1:8000/health

Expected:

HTTP 200

The service should report healthy dependencies.

---

# 9. API Documentation

Open:

http://127.0.0.1:8000/docs

OpenAPI:

http://127.0.0.1:8000/openapi.json

---

# 10. Ingest

Documents must be ingested before asking
questions about them.

Use the /ingest endpoint.

Example:

POST /ingest

Required document metadata/content must be supplied
according to the API schema.

Verify the ingestion response before continuing.

---

# 11. Ask

Use:

POST /ask

Example request:

{
  "question": "What is the leave policy?"
}

Expected:

- request_id
- answer
- sources

The answer should be grounded in the indexed documents.

---

# 12. Evaluation

Run the automated tests:

pytest -v

Run the evaluation:

python -m eval.evaluation_runner

Run adversarial validation:

pytest eval/tests/test_adversarial_cases.py -v

---

# 13. Voice Workflow

Start the required RAG API first.

Then run the voice workflow.

Verify:

1. Audio input
2. STT transcription
3. RAG /ask
4. Response generation
5. TTS/fallback
6. Source preservation

---

# 14. Logs

Check application logs for:

- request ID
- stage
- latency
- status
- errors

Do not log secrets or sensitive credentials.

---

# 15. Troubleshooting

See:

day19/docs/TROUBLESHOOTING.md

---

# 16. Rollback

See:

day19/docs/ROLLBACK.md

# Testing

## Unit Tests

pytest -v

## Full Test Suite

pytest -v -ra

## Compilation

python -m compileall -q eval tests

## 25-Case Evaluation

python -m eval.evaluation_runner

## 10-Case Adversarial Suite

pytest eval/tests/test_adversarial_cases.py -v

## Voice Tests

cd genai-day-17-18/day17
pytest -v

cd ../day18
pytest -v