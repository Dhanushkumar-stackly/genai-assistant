# Day 19 - Task 1 Fresh Clone Rehearsal

## BEFORE FIX

### Audio Input

Status: PASS

### STT

Status: PASS

Transcript:

What is the leave policy?

### RAG /ask

Status: FAIL

Error:

404 Not Found

URL:

http://127.0.0.1:8000/ask

## Root Cause

The Day 17 voice client depends on the existing Day 11–12
RAG API `/ask` endpoint.

The RAG API was not started during the fresh-clone setup.

## FIX

Start the Day 11–12 FastAPI service:

python -m uvicorn src.day11.main:app --reload

## Verification

Health endpoint:

/health

RAG endpoint:

/ask

## AFTER FIX

Audio Input:
Record actual result.

STT:
Record actual result.

RAG /ask:
Record actual result.

Day 17 Task 3:
Record actual result.

Day 17 pytest:
Record actual result.

## Final Status

PASS only after all required checks succeed.