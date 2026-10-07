# Rollback Guide

## Purpose

Use this procedure when a release candidate introduces
a regression.

---

## 1. Identify Current Version

git status

git log --oneline -10

---

## 2. Identify Last Known Good Commit

git log --oneline

Select the last verified commit.

---

## 3. Create a Safety Branch

git checkout -b rollback-investigation

---

## 4. Restore Known Good Version

Use the approved rollback commit/version.

Do not delete the current release evidence.

---

## 5. Reinstall Dependencies if Required

python -m pip install -r requirements.txt

---

## 6. Run Health Check

Invoke-RestMethod http://127.0.0.1:8000/health

---

## 7. Run Regression Tests

pytest -v

Run the required evaluation suites.

---

## 8. Verify API

Test:

GET /health

POST /ask

---

## 9. Verify Voice

Run the Day 17/18 voice regression tests.

---

## 10. Record Rollback

Record:

- Failed version
- Rollback version
- Reason
- Date/time
- Failed tests
- Recovery result

---

## 11. Do Not Delete Evidence

Keep the failed release evidence so the failure
can be investigated later.