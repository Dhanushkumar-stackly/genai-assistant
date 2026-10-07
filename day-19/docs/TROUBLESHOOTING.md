# Troubleshooting Guide

## 1. /ask Returns 404

### Symptom

HTTP 404 for:

http://127.0.0.1:8000/ask

### Cause

The RAG API is not running or the wrong application
is running on port 8000.

### Fix

Start:

python -m uvicorn src.day11.main:app --reload

Then verify:

Invoke-RestMethod http://127.0.0.1:8000/health

---

## 2. /health Fails

Check whether port 8000 is occupied:

Get-NetTCPConnection -LocalPort 8000

Check the running process:

Get-Process -Id <PID>

---

## 3. Import Error

Example:

ModuleNotFoundError

Check:

1. Virtual environment is active.
2. Dependencies are installed.
3. Command is executed from the correct project root.

Run:

python -m pip install -r requirements.txt

---

## 4. Empty Retrieval

### Symptom

/ask returns no useful sources.

### Check

Verify documents were ingested.

Run the ingestion workflow.

Then retry /ask.

---

## 5. Evaluation Failure

Run:

pytest -v

Identify the exact failing test.

Do not modify unrelated components.

Record:

- failing test
- error
- root cause
- fix
- regression result

---

## 6. Voice RAG Failure

Check in this order:

Audio
→ STT
→ /ask
→ RAG
→ Response
→ TTS

If STT succeeds but /ask fails,
check the RAG API first.

---

## 7. TTS Failure

Use the documented fallback behavior if available.

Verify that the text response is still generated.

---

## 8. Port Conflict

Check:

Get-NetTCPConnection -State Listen

Stop only the process that is confirmed to
own the required port.

---

## 9. Git Push Rejected

Check:

git status

git branch

git remote -v

Never disable repository security controls merely
to bypass a secret-detection failure.