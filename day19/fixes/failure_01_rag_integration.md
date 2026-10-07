# Failure Category 1 - RAG Integration

## Category

RAG service availability / integration

## Severity

HIGH

## Before Fix

Voice input:
PASS

STT:
PASS

Transcript:
"What is the leave policy?"

RAG:
FAIL

HTTP:
404 Not Found

Endpoint:
http://127.0.0.1:8000/ask

## Root Cause

The Day 17 voice client depends on the existing Day 11-12
RAG `/ask` API, but the RAG service was not running during
the fresh-clone setup.

## Controlled Fix

Start the Day 11-12 FastAPI application before executing
the voice workflow.

Command:

python -m uvicorn src.day11.main:app --reload

## Verification

Health check:

GET /health

RAG check:

POST /ask

Voice regression:

python run_task3.py

## Regression Tests

pytest -v

## Result

Record actual output here.

## Status

PASS only when /ask and Day 17 regression tests succeed.