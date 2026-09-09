# GenAI RAG API — Day 11 & Day 12

FastAPI-based GenAI RAG service with document ingestion, document retrieval, ask endpoint, request logging, SQLite persistence, request metrics, validation handling, and pytest coverage.

## Run
`uvicorn src.day11.main:app --reload`

## Test
`pytest -v`

## Endpoints
- GET `/` — API information
- GET `/health` — health check with request ID
- POST `/ingest` — ingest and chunk a document
- GET `/documents/{document_id}` — retrieve a document summary
- POST `/ask` — ask against available documents
- GET `/metrics` — request metrics

## Day 12 verification
Database tables: `documents`, `request_logs`, `retrieved_source_logs`.
Request logs capture request ID, endpoint, latency, model version, prompt version, outcome, and error category.
