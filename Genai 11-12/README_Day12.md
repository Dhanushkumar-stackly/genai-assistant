# GenAI RAG API — Day 12 README

## 1. Day 12 Overview

Day 12 extends the Day 11 FastAPI RAG service with **SQL-based observability, request tracing, retrieved-source tracing, structured errors, and metrics**.

The Day 12 implementation provides:

- Async SQLite database
- SQLAlchemy models
- Request logging
- Retrieved-source logging
- Request IDs
- Latency measurement
- Model version tracking
- Prompt version tracking
- Outcome classification
- Error categorization
- Consistent 422/404/500 error responses
- Safe exception handling
- Request metrics
- Automated async database tests

> **Image reference:** The supplied `Genai 11-12(2).zip` contains no image files. The four images mentioned in the request are therefore not available in the supplied ZIP. This README uses the actual Day 12 implementation and acceptance tests as the source of truth instead of inventing screenshot details.

---

# 2. Day 12 Tasks

## Task 1 — Async SQLite Database

**File:**

```text
src/day11/database.py
```

Database URL:

```text
sqlite+aiosqlite:///./genai.db
```

The project uses:

- SQLAlchemy async engine
- `aiosqlite`
- Async sessions
- SQLite database

The database initialization creates:

```text
documents
request_logs
retrieved_source_logs
```

---

## Task 2 — Request Log Database Model

**File:**

```text
src/day11/db_models.py
```

`RequestLog` stores:

```text
request_id
endpoint
start_time
total_latency_ms
model_version
prompt_version
outcome
error_category
```

This provides persistent request-level observability.

---

## Task 3 — Retrieved Source Log Model

`RetrievedSourceLog` stores:

```text
request_id
source_id
score
created_at
```

The same request ID connects the source retrieval information to the original API request.

---

## Task 4 — Request Logging Middleware

**File:**

```text
src/day11/main.py
```

Every HTTP request receives a UUID request ID.

The middleware measures:

```text
start time
total latency
HTTP status
outcome
error category
```

The request is persisted into `request_logs`.

Example successful outcome:

```text
outcome = success
```

Example validation outcome:

```text
outcome = validation_error
error_category = validation
```

Example not-found outcome:

```text
outcome = not_found
error_category = not_found
```

---

## Task 5 — Model and Prompt Version Tracking

**File:**

```text
src/day11/logging_service.py
```

The current versions are:

```text
MODEL_VERSION = rag-model-v1
PROMPT_VERSION = prompt-v1
```

Every request log stores these values.

This makes it possible to identify which model/prompt version produced a request.

---

## Task 6 — Retrieved Source Tracing

When `/ask` successfully retrieves sources, the source information is persisted in:

```text
retrieved_source_logs
```

The following information is recorded:

```text
request_id
source_id
score
created_at
```

The request ID provides traceability between:

```text
API request
    ↓
RAG answer
    ↓
retrieved source
```

---

## Task 7 — Structured Validation Errors

Invalid requests return:

```text
HTTP 422
```

Example:

```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Request validation failed"
}
```

A request ID is included.

Internal validation details are placed in the `detail` field.

---

## Task 8 — Safe Not-Found Errors

An unknown document returns:

```text
HTTP 404
```

with:

```json
{
  "error_code": "DOCUMENT_NOT_FOUND",
  "message": "Document not found"
}
```

The implementation explicitly prevents a traceback from being exposed to the API client.

---

## Task 9 — Safe No-Evidence Error

If `/ask` has no available evidence, the RAG service raises:

```text
NoEvidenceError
```

The API converts this into:

```text
HTTP 404
```

with:

```json
{
  "error_code": "NO_EVIDENCE",
  "message": "No evidence is available for this question"
}
```

No traceback is exposed.

---

## Task 10 — Safe Internal Server Error

Unexpected exceptions are converted to:

```text
HTTP 500
```

with:

```json
{
  "error_code": "INTERNAL_ERROR",
  "message": "An internal server error occurred"
}
```

The actual internal exception message is not exposed.

For example, a simulated:

```text
simulated provider failure
```

must not appear in the client response.

---

## Task 11 — Request Metrics

**File:**

```text
src/day11/metrics.py
```

The metrics service tracks:

```text
total_requests
successful_requests
failed_requests
total_latency_ms
average_latency_ms
```

Endpoint:

```text
GET /metrics
```

Expected response structure:

```json
{
  "total_requests": 3,
  "successful_requests": 2,
  "failed_requests": 1,
  "average_latency_ms": 5.0
}
```

The exact numbers depend on runtime traffic.

---

## Task 12 — Automated Day 12 Verification

The acceptance test file is:

```text
tests/test_day11_day12_complete.py
```

Day 12 tests verify:

- database tables
- required database columns
- successful request tracing
- model version
- prompt version
- retrieved source tracing
- validation-error tracing
- unknown-document error tracing
- no-evidence safety
- simulated dependency failure
- safe 500 response
- metrics

---

# 3. Day 12 Complete Flow

```text
Client Request
      ↓
FastAPI Middleware
      ↓
Generate request_id
      ↓
Record start time
      ↓
Route
      ↓
RAG operation
      ↓
Success / Validation / 404 / 500
      ↓
Measure latency
      ↓
Classify outcome
      ↓
Write request_logs
      ↓
Return safe API response
```

For `/ask`:

```text
POST /ask
   ↓
RAG retrieval
   ↓
Answer + sources
   ↓
retrieved_source_logs
   ↓
request_id links request + source
```

---

# 4. Database Schema

## request_logs

```text
id
request_id
endpoint
start_time
total_latency_ms
model_version
prompt_version
outcome
error_category
```

## retrieved_source_logs

```text
id
request_id
source_id
score
created_at
```

---

# 5. Required Packages

The supplied `requirements.txt` contains:

```text
aiosqlite==0.22.1
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.15.0
certifi==2026.7.22
click==8.5.0
colorama==0.4.6
fastapi==0.141.1
greenlet==3.5.5
h11==0.16.0
httpcore==1.0.9
httpcore2==2.12.0
httpx==0.28.1
httpx2==2.12.0
idna==3.19
iniconfig==2.3.0
packaging==26.3
pluggy==1.6.0
pydantic==2.13.5
pydantic-settings==2.15.0
pydantic_core==2.46.5
Pygments==2.21.0
pytest==9.1.1
pytest-asyncio==1.4.0
python-dotenv==1.2.3
SQLAlchemy==2.0.52
starlette==1.6.0
truststore==0.10.4
typing-inspection==0.4.4
typing_extensions==4.16.0
uvicorn==0.52.4
```

Critical Day 12 packages:

```text
SQLAlchemy
aiosqlite
fastapi
pydantic
pydantic-settings
pytest
pytest-asyncio
httpx
uvicorn
```

---

# 6. Environment Setup — All Terminal Commands

Go to the project:

```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\Genai 11-12"
```

Create venv if it does not exist:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify the interpreter:

```powershell
python -c "import sys; print(sys.executable)"
```

It should point to:

```text
...\Genai 11-12\venv\Scripts\python.exe
```

Install requirements:

```powershell
python -m pip install -r requirements.txt
```

Verify aiosqlite:

```powershell
python -c "import aiosqlite; print('aiosqlite:', aiosqlite.__version__)"
```

Verify SQLAlchemy:

```powershell
python -c "import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)"
```

Verify pytest:

```powershell
python -m pytest --version
```

Verify pytest-asyncio:

```powershell
python -c "import pytest_asyncio; print('pytest-asyncio installed')"
```

---

# 7. Important Pytest Command

Use:

```powershell
python -m pytest -v
```

Prefer this over:

```powershell
pytest -v
```

because `python -m pytest` guarantees pytest is launched through the Python interpreter selected by `python`.

---

# 8. Run Day 12 API

Start:

```powershell
python -m uvicorn src.day11.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 9. Runtime Output Commands

## Health

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Verify:

```text
status = ok
database = ready
rag = ready
```

## Ingest

```powershell
$body = @{
    title = "Day 12 Trace Demo"
    content = "First chunk.`n`nSecond chunk."
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri http://127.0.0.1:8000/ingest `
    -ContentType "application/json" `
    -Body $body
```

Verify that a `request_id` is returned.

## Ask

```powershell
$body = @{
    question = "What is this?"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri http://127.0.0.1:8000/ask `
    -ContentType "application/json" `
    -Body $body
```

Verify:

```text
request_id
answer
sources
sources[0].document_id
sources[0].score
```

## Metrics

```powershell
Invoke-RestMethod http://127.0.0.1:8000/metrics
```

Verify:

```text
total_requests
successful_requests
failed_requests
average_latency_ms
```

---

# 10. Error Runtime Tests

## Validation error

```powershell
$body = @{
    title = ""
    content = ""
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri http://127.0.0.1:8000/ingest `
    -ContentType "application/json" `
    -Body $body
```

Expected HTTP status:

```text
422
```

Expected:

```text
error_code = VALIDATION_ERROR
message = Request validation failed
```

## Unknown document

```powershell
try {
    Invoke-RestMethod http://127.0.0.1:8000/documents/unknown
}
catch {
    $_.ErrorDetails.Message
}
```

Expected:

```json
{
  "error_code": "DOCUMENT_NOT_FOUND",
  "message": "Document not found"
}
```

The response must not contain:

```text
Traceback
```

## No evidence

When no document exists:

```powershell
$body = @{
    question = "question"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri http://127.0.0.1:8000/ask `
    -ContentType "application/json" `
    -Body $body
```

Expected:

```text
HTTP 404
error_code = NO_EVIDENCE
message = No evidence is available for this question
```

---

# 11. Day 12 Tests — All Commands

Run complete suite:

```powershell
python -m pytest -v
```

Run database test:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_database_tables_and_columns
```

Run request tracing:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_successful_request_is_traced_in_sql
```

Run retrieved-source tracing:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_retrieved_sources_are_logged
```

Run validation-error tracing:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_validation_error_is_consistent_and_traced
```

Run unknown-document safety:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_unknown_document_has_safe_error_and_trace
```

Run no-evidence safety:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_missing_evidence_is_safe_error
```

Run simulated dependency failure:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_simulated_dependency_failure_is_500_and_safe
```

Run metrics:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_metrics_are_updated
```

---

# 12. Database Verification Commands

Check the database file:

```powershell
Get-Item .\genai.db
```

Run the database test:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day12_database_tables_and_columns
```

The test verifies:

```text
request_logs
retrieved_source_logs
```

and the required columns.

---

# 13. Expected Successful Test Result

A correct environment should produce:

```text
============================= test session starts =============================
...
collected 12 items

... PASSED ...
...
============================= XX passed in X.XXs ==============================
```

The exact number and timing must come from the actual terminal run.

Do **not** replace actual pytest output with fabricated numbers.

---

# 14. Day 12 Verification Checklist

```text
[ ] venv activated
[ ] Python points to venv
[ ] requirements installed
[ ] aiosqlite installed
[ ] pytest-asyncio installed
[ ] FastAPI starts
[ ] SQLite database initializes
[ ] request_logs exists
[ ] retrieved_source_logs exists
[ ] request ID generated
[ ] request latency logged
[ ] model version logged
[ ] prompt version logged
[ ] successful request traced
[ ] retrieved source traced
[ ] 422 validation error is safe
[ ] 404 document error is safe
[ ] 404 no-evidence error is safe
[ ] 500 internal error is safe
[ ] metrics are updated
[ ] all pytest tests pass
```

---

# 15. Final Day 12 Verification Rule

Do not mark Day 12 as complete merely because the source code exists.

The final acceptance condition is:

```text
Dependencies installed
        +
API runtime successful
        +
Database initialized
        +
Runtime outputs verified
        +
pytest -v passes
        =
Day 12 verified
```
