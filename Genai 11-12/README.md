# GenAI RAG API — Day 11 & Day 12

## Overview

This project implements the Day 11 FastAPI service contracts and core RAG endpoints, followed by Day 12 SQL observability, structured error handling, and API tests.

## Project structure

```text
src/day11/
  config.py             # application settings
  database.py           # async SQLite engine and schema initialization
  db_models.py          # SQLAlchemy request/source log models
  logging_service.py    # request and retrieved-source persistence
  main.py               # FastAPI application, lifespan, middleware, errors
  metrics.py            # request metrics
  models.py             # Pydantic request/response/error models
  rag.py                # RAG service boundary
  routes.py             # API route handlers

tests/
  test_day11_day12_complete.py  # Day 11 + Day 12 acceptance tests

genai.db                 # SQLite database
pytest.ini               # pytest configuration
requirements.txt         # pinned Python dependencies
```

## Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the API

```powershell
uvicorn src.day11.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

OpenAPI UI: `http://127.0.0.1:8000/docs`

OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Service and dependency readiness |
| POST | `/ingest` | Validate and ingest a document |
| POST | `/ask` | Ask the RAG service and return cited sources |
| GET | `/documents/{document_id}` | Retrieve document metadata/status |
| GET | `/metrics` | Request metrics |

## Example requests

### Ingest

```json
{
  "title": "Runtime Demo",
  "content": "First chunk.\n\nSecond chunk."
}
```

### Ask

```json
{
  "question": "What is this about?"
}
```

## Error behavior

Validation failures return HTTP 422 with a request ID and `VALIDATION_ERROR`.

Unknown documents return HTTP 404 with `DOCUMENT_NOT_FOUND`.

Questions with no evidence return HTTP 404 with `NO_EVIDENCE`.

Unexpected failures return HTTP 500 with `INTERNAL_ERROR`; internal exception text and stack traces are not exposed to clients.

## Observability

Every HTTP request receives a UUID request ID. The middleware records endpoint, start time, latency, model version, prompt version, outcome, and error category in `request_logs`.

Successful `/ask` calls also write retrieved source IDs and scores to `retrieved_source_logs` using the same request ID.

## Tests

Run the complete suite:

```powershell
pytest -v
```

The acceptance suite covers endpoint contracts, OpenAPI schemas, database tables/columns, request tracing, source tracing, validation errors, not-found errors, missing evidence, simulated dependency failure, metrics, and application lifespan startup/shutdown.

## Important verification note

The implementation is designed to run with the pinned `aiosqlite` dependency from `requirements.txt`. The supplied verification environment did not have `aiosqlite` installed and had no network access, so runtime verification used a temporary local compatibility shim for `aiosqlite`. This shim is not part of the project and must not be added to the repository.
