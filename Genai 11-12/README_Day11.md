# GenAI RAG API — Day 11 README

## 1. Day 11 Overview

Day 11 implements the core **FastAPI service layer for a GenAI RAG API**.

The Day 11 implementation provides:

- FastAPI application setup
- Application configuration
- Request/response validation with Pydantic
- RAG document ingestion
- Document lookup
- RAG question/answer endpoint
- Source/citation information in responses
- Health/readiness endpoint
- Metrics endpoint
- OpenAPI documentation
- Request IDs for API calls

> **Image reference:** The supplied `Genai 11-12(2).zip` contains the Day 11 source code and tests, but it does **not contain the four image files** mentioned in the request. Therefore, this README maps the Day 11 tasks from the actual implementation and acceptance tests rather than inventing screenshot-specific task names.

---

## 2. Day 11 Tasks

### Task 1 — FastAPI Application and Configuration

**Files:**
- `src/day11/main.py`
- `src/day11/config.py`

The application is created with:

- FastAPI
- Application name: `GenAI RAG API`
- Version: `0.1.0`
- Development environment configuration
- Application lifespan startup/shutdown

The lifespan initializes the database and starts the RAG service when the application starts.

### Task 2 — Root and Health Endpoints

**Endpoints:**

```text
GET /
GET /health
```

`GET /` returns service information.

`GET /health` verifies:

- API status
- Database readiness
- RAG service readiness
- Application version
- Request ID

Expected health dependency status:

```json
{
  "database": "ready",
  "rag": "ready"
}
```

### Task 3 — Document Ingestion and Chunking

**Endpoint:**

```text
POST /ingest
```

Request:

```json
{
  "title": "Runtime Demo",
  "content": "First chunk.\n\nSecond chunk."
}
```

The RAG service:

1. Generates a document UUID.
2. Stores the document.
3. Splits content using blank lines.
4. Counts the resulting chunks.
5. Returns processing status.

Expected response structure:

```json
{
  "request_id": "<uuid>",
  "document_id": "<uuid>",
  "chunk_count": 2,
  "status": "processed"
}
```

### Task 4 — Document Lookup

**Endpoint:**

```text
GET /documents/{document_id}
```

Returns:

- request ID
- document ID
- title
- chunk count
- processing status

An unknown document produces HTTP `404`.

### Task 5 — RAG Ask Endpoint and Sources

**Endpoint:**

```text
POST /ask
```

Request:

```json
{
  "question": "What is this about?"
}
```

The endpoint calls the RAG service and returns:

- request ID
- answer
- source list
- source document ID
- source title
- relevance score

Expected source score in the current implementation:

```text
1.0
```

### Task 6 — Pydantic API Contracts

**File:**

```text
src/day11/models.py
```

The implementation defines validated models for:

- `HealthResponse`
- `IngestRequest`
- `IngestResponse`
- `AskRequest`
- `AskResponse`
- `Source`
- `DocumentResponse`
- `MetricsResponse`
- `ErrorResponse`

Required text fields use minimum-length validation where applicable.

### Task 7 — OpenAPI Contract

The application exposes the FastAPI OpenAPI schema.

Required paths include:

```text
/health
/ingest
/ask
/documents/{document_id}
```

Required schemas include:

```text
IngestRequest
IngestResponse
AskRequest
AskResponse
DocumentResponse
HealthResponse
```

---

# 3. Day 11 Complete Flow

```text
Client
  ↓
FastAPI
  ↓
Request validation
  ↓
Request ID middleware
  ↓
Route
  ↓
RAG Service
  ↓
Document ingest / retrieval / answer
  ↓
Pydantic response
  ↓
Client
```

For health:

```text
GET /health
  ↓
Database check
  ↓
RAG readiness check
  ↓
HealthResponse
```

---

# 4. Project Structure

```text
Genai 11-12/
│
├── src/
│   └── day11/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── db_models.py
│       ├── logging_service.py
│       ├── main.py
│       ├── metrics.py
│       ├── models.py
│       ├── rag.py
│       └── routes.py
│
├── tests/
│   └── test_day11_day12_complete.py
│
├── genai.db
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# 5. Required Packages

The supplied `requirements.txt` contains these pinned packages:

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

Critical Day 11 packages:

```text
fastapi
pydantic
pydantic-settings
uvicorn
sqlalchemy
aiosqlite
pytest
pytest-asyncio
httpx
```

---

# 6. Environment Setup — All Terminal Commands

Open PowerShell in the project folder:

```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\Genai 11-12"
```

Create the virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify the Python interpreter:

```powershell
python -c "import sys; print(sys.executable)"
```

The result should point to:

```text
...\Genai 11-12\venv\Scripts\python.exe
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install all requirements:

```powershell
python -m pip install -r requirements.txt
```

Verify FastAPI:

```powershell
python -c "import fastapi; print(fastapi.__version__)"
```

Verify SQLAlchemy:

```powershell
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

Verify aiosqlite:

```powershell
python -c "import aiosqlite; print(aiosqlite.__version__)"
```

Verify pytest-asyncio:

```powershell
python -c "import pytest_asyncio; print('pytest-asyncio installed')"
```

---

# 7. Run Day 11 API

Start the API:

```powershell
python -m uvicorn src.day11.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 8. Runtime Outputs to Verify

### Root

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

Expected:

```text
message     : GenAI RAG API is running
service     : GenAI RAG API
version     : 0.1.0
environment : development
status      : running
```

### Health

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected:

```text
status : ok
service : GenAI RAG API
version : 0.1.0
dependencies.database : ready
dependencies.rag : ready
```

### Ingest

```powershell
$body = @{
    title = "Runtime Demo"
    content = "First chunk.`n`nSecond chunk."
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri http://127.0.0.1:8000/ingest `
    -ContentType "application/json" `
    -Body $body
```

Expected:

```text
status      : processed
chunk_count : 2
document_id : <generated UUID>
request_id  : <generated UUID>
```

Save the returned `document_id`.

### Document lookup

```powershell
Invoke-RestMethod http://127.0.0.1:8000/documents/<DOCUMENT_ID>
```

Expected:

```text
title       : Runtime Demo
chunk_count : 2
status      : processed
```

### Ask

```powershell
$body = @{
    question = "What is this about?"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri http://127.0.0.1:8000/ask `
    -ContentType "application/json" `
    -Body $body
```

Expected:

```text
answer : Answer based on document: Runtime Demo
sources : one source containing document_id, title and score 1.0
```

---

# 9. Day 11 Tests

Run all tests:

```powershell
python -m pytest -v
```

Run only the Day 11 tests:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py -k "day11 or openapi"
```

Run root/health:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day11_root_and_health
```

Run ingest/document:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day11_ingest_and_document_lookup
```

Run ask/source validation:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_day11_ask_returns_validated_answer_and_sources
```

Run OpenAPI verification:

```powershell
python -m pytest -v tests/test_day11_day12_complete.py::test_openapi_has_required_endpoints_and_schemas
```

---

# 10. Day 11 Verification Checklist

```text
[ ] Virtual environment activated
[ ] Python points to venv
[ ] requirements.txt installed
[ ] aiosqlite installed
[ ] pytest-asyncio installed
[ ] API starts successfully
[ ] GET / works
[ ] GET /health works
[ ] POST /ingest works
[ ] GET /documents/{document_id} works
[ ] POST /ask works
[ ] OpenAPI contains required endpoints
[ ] Day 11 pytest tests pass
```

---

# 11. Day 11 Expected Test Result

A successful Day 11 verification should show the Day 11 tests as:

```text
PASSED
```

Do not claim the test is successful unless the terminal actually reports `PASSED`.

