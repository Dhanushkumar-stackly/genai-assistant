# GenAI Assistant — Day 1 to Day 4

## Overview

This README documents only the **Day 1 to Day 4** work contained in this project.

The practical work covers:

- Prompt design
- Classification
- Information extraction
- Summarization
- Prompt versioning
- Sample input preparation
- Input validation
- Prompt test execution
- JSON test-result reporting
- Basic safety/guardrail scaffolding
- Runtime verification

---

# Day 1–4 Tasks

## Task 1 — Classification Prompt

### Objective

Create a prompt that classifies a document into an allowed category.

The classification prompt uses the following labels:

```text
invoice
receipt
other
```

The prompt is designed to:

- Return one allowed label
- Avoid inventing new labels
- Provide a brief reason
- Return JSON
- Use the supplied document as input

### Prompt

```text
prompts/classification.txt
```

### Expected Output Format

```json
{
  "label": "invoice",
  "reason": "The document contains invoice-specific information."
}
```

### Sample Inputs

```text
samples/classification/
├── normal.txt
├── ambiguous.txt
├── incomplete.txt
└── long.txt
```

---

# Task 2 — Information Extraction Prompt

### Objective

Extract structured information from a document.

The extraction prompt requests:

```text
invoice_number
customer_name
customer_email
invoice_date
total_amount
```

### Extraction Rules

The prompt requires the model to:

- Extract only information explicitly present
- Return `null` for missing fields
- Return valid JSON
- Use the requested field names

### Prompt

```text
prompts/extraction.txt
```

### Expected Output Format

```json
{
  "invoice_number": "INV-2025-1023",
  "customer_name": "Maria Lopez",
  "customer_email": "maria.lopez@example.com",
  "invoice_date": "2025-03-12",
  "total_amount": "$2,340.50"
}
```

### Sample Inputs

```text
samples/extraction/
├── normal.txt
├── ambiguous.txt
├── incomplete.txt
└── long.txt
```

---

# Task 3 — Summarization Prompt

### Objective

Create a concise summarization prompt.

The summarization prompt is designed to:

- Keep the summary short and clear
- Focus on the main topic and key facts
- Avoid adding unsupported information

### Prompt

```text
prompts/summarization.txt
```

### Input Placeholder

```text
{document}
```

### Sample Inputs

```text
samples/summarization/
├── normal.txt
├── ambiguous.txt
├── incomplete.txt
└── long.txt
```

---

# Task 4 — Prompt Versioning

The project contains versioned prompt folders.

```text
prompts/
├── classifier/
│   └── v1.txt
│
├── extractor/
│   ├── v1.txt
│   └── v2.txt
│
└── summarizer/
    └── v1.txt
```

The prompt test runner also records:

```text
PROMPT_VERSION = "v1"
MODEL_VERSION = "test-model-v1"
```

### Purpose

Prompt versioning allows different prompt configurations to be tracked
separately and makes test results reproducible.

---

# Task 5 — Sample Data

The project contains:

```text
data/sample.json
```

The sample document record contains fields such as:

```json
{
    "document_id": "DOC001",
    "title": "Company Leave Policy",
    "content": "Employees are eligible for annual leave.",
    "source_path": "data/company_leave.txt",
    "updated_at": "2026-08-10T10:00:00"
}
```

This demonstrates a structured document containing:

- Document ID
- Title
- Content
- Source path
- Updated timestamp

---

# Task 6 — Prompt Test Cases

The prompt testing workflow contains 10 cases.

The cases cover:

- Valid input
- Ambiguous input
- Malformed input
- Empty input
- Whitespace-only input

### Test Case Categories

```text
case_01 → valid
case_02 → valid
case_03 → ambiguous
case_04 → ambiguous
case_05 → malformed
case_06 → malformed
case_07 → empty
case_08 → empty
case_09 → valid
case_10 → valid
```

---

# Task 7 — Input Validation

The validation logic is implemented in:

```text
scripts/run_prompt_tests.py
```

The validation function checks the input before processing.

## None

```python
None
```

Result:

```text
malformed_input
```

## Non-String Input

Example:

```python
12345
```

Result:

```text
malformed_input
```

## Empty Input

```text
""
```

Result:

```text
empty_input
```

## Whitespace-Only Input

```text
"   "
```

Result:

```text
empty_input
```

## Valid Input

A non-empty string is accepted.

---

# Task 8 — Prompt Test Runner

The main test runner is:

```text
scripts/run_prompt_tests.py
```

The runner:

1. Defines the test cases
2. Validates each input
3. Measures validation latency
4. Records prompt version
5. Records model version
6. Records validation result
7. Records failure reason
8. Writes JSON results
9. Prints a summary

---

# Task 9 — Prompt Test Result Report

The generated result file is:

```text
results/prompt_test_results.json
```

The report contains:

```text
prompt_version
model_version
total_cases
passed
failed
results
```

Each individual result contains fields such as:

```text
case_id
prompt_version
model_version
latency_ms
validation_result
failure_reason
expected_label
```

---

# Actual Result Verification

The generated result artifact records:

```text
Total Cases: 10
Passed: 6
Failed: 4
```

The four failures correspond to intentionally invalid inputs:

```text
case_05 → malformed_input
case_06 → malformed_input
case_07 → empty_input
case_08 → empty_input
```

This demonstrates that the validation layer distinguishes valid,
malformed, and empty inputs.

---

# Task 10 — Summarization Runtime

The project contains:

```text
scripts/summarizer_runner.py
```

The runner is intended to:

1. Define sample text
2. Validate that the input is not empty
3. Create the model client
4. Create the summarizer
5. Generate a summary
6. Print the result

### Runtime Command

```powershell
python scripts/summarizer_runner.py
```

### Expected Output Structure

```text
============================================================
SUMMARIZER
============================================================

Input text:
...

============================================================
SUMMARY
============================================================
...

============================================================
Execution completed successfully.
============================================================
```

---

# Task 11 — Safety / Guardrail Scaffolding

The Day 1–4 project contains:

```text
safety/guardrails.py
```

This file provides the safety/guardrail location in the project structure.

---

# Task 12 — Voice / Audio Scaffolding

The project contains:

```text
voice/audio.py
```

This provides the voice/audio component location for the project.

---

# Prompt and Sample File Structure

```text
prompts/
├── classification.txt
├── extraction.txt
├── summarization.txt
│
├── classifier/
│   └── v1.txt
│
├── extractor/
│   ├── v1.txt
│   └── v2.txt
│
└── summarizer/
    └── v1.txt
```

Sample data:

```text
samples/
├── classification/
│   ├── normal.txt
│   ├── ambiguous.txt
│   ├── incomplete.txt
│   └── long.txt
│
├── extraction/
│   ├── normal.txt
│   ├── ambiguous.txt
│   ├── incomplete.txt
│   └── long.txt
│
└── summarization/
    ├── normal.txt
    ├── ambiguous.txt
    ├── incomplete.txt
    └── long.txt
```

---

# Complete Project Structure — Day 1 to Day 4

```text
Genai day 1 to 4/
│
├── data/
│   └── sample.json
│
├── datasets/
│   └── prompt_cases.json
│
├── prompts/
│   ├── classification.txt
│   ├── extraction.txt
│   ├── summarization.txt
│   ├── classifier/
│   │   └── v1.txt
│   ├── extractor/
│   │   ├── v1.txt
│   │   └── v2.txt
│   └── summarizer/
│       └── v1.txt
│
├── samples/
│   ├── classification/
│   ├── extraction/
│   └── summarization/
│
├── scripts/
│   ├── run_prompt_tests.py
│   └── summarizer_runner.py
│
├── safety/
│   └── guardrails.py
│
├── voice/
│   └── audio.py
│
├── results/
│   └── prompt_test_results.json
│
├── tests/
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# File-by-File Purpose

| File / Folder | Purpose |
|---|---|
| `prompts/classification.txt` | Classification prompt |
| `prompts/extraction.txt` | Information extraction prompt |
| `prompts/summarization.txt` | Summarization prompt |
| `prompts/classifier/v1.txt` | Versioned classifier prompt |
| `prompts/extractor/v1.txt` | Versioned extractor prompt |
| `prompts/extractor/v2.txt` | Second extractor prompt version |
| `prompts/summarizer/v1.txt` | Versioned summarizer prompt |
| `samples/` | Test documents for the three prompt types |
| `data/sample.json` | Structured sample document |
| `scripts/run_prompt_tests.py` | Prompt/input validation test runner |
| `scripts/summarizer_runner.py` | Summarization runtime runner |
| `results/prompt_test_results.json` | Generated prompt-test report |
| `safety/guardrails.py` | Safety/guardrail scaffolding |
| `voice/audio.py` | Voice/audio scaffolding |
| `pytest.ini` | Pytest configuration |
| `datasets/prompt_cases.json` | Prompt test-case data file |

---

# Pytest Configuration

The project contains:

```text
pytest.ini
```

with:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

This configures pytest to:

- Search the `tests` directory
- Discover files named `test_*.py`
- Discover test classes beginning with `Test`
- Discover functions beginning with `test_`

---

# Required Packages

The project uses Python packages for its prompt/testing workflow.

A clean `requirements.txt` for the dependencies represented by the project
should contain the packages actually required by the implemented runtime and
tests.

At minimum for the prompt-test workflow:

```text
pytest
```

If the complete project environment uses the other imported application
components, install the corresponding packages listed in the project's
final, resolved `requirements.txt`.

---

# Environment Setup

## 1. Open Project

```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\Genai day 1 to 4"
```

## 2. Create Virtual Environment

If required:

```powershell
python -m venv venv
```

## 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

## 4. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

## 5. Install Requirements

After resolving the project's `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

---

# Verify Python Environment

```powershell
python --version
```

```powershell
python -m pip --version
```

```powershell
pytest --version
```

---

# Runtime Commands

## Prompt Test Runner

```powershell
python scripts/run_prompt_tests.py
```

## View Prompt Test Results

```powershell
Get-Content .\results\prompt_test_results.json
```

## Summarization Runner

```powershell
python scripts/summarizer_runner.py
```

---

# Pytest Commands

## Run All Tests

```powershell
pytest -v
```

or:

```powershell
python -m pytest -v
```

## Run With Cache Cleared

```powershell
pytest -v --cache-clear
```

## Run Verbosely

```powershell
pytest -vv
```

## Stop at First Failure

```powershell
pytest -v -x
```

---

# Verify Prompt Test Output

Check that the JSON result file exists:

```powershell
Test-Path .\results\prompt_test_results.json
```

Expected:

```text
True
```

Display the report:

```powershell
Get-Content .\results\prompt_test_results.json
```

---

# Verify Prompt Files

```powershell
Get-ChildItem .\prompts -Recurse
```

---

# Verify Sample Files

```powershell
Get-ChildItem .\samples -Recurse
```

---

# Verify Scripts

```powershell
Get-ChildItem .\scripts
```

---

# Verify Tests

```powershell
Get-ChildItem .\tests -Recurse
```

---

# Complete Runtime Verification

Run the prompt test runner:

```powershell
python scripts/run_prompt_tests.py
```

Check the generated report:

```powershell
Get-Content .\results\prompt_test_results.json
```

Run automated tests:

```powershell
python -m pytest -v
```

Run the summarization runner:

```powershell
python scripts/summarizer_runner.py
```

---

# Expected Prompt Test Verification

The generated result should contain:

```text
Total Cases: 10
Passed: 6
Failed: 4
```

The expected invalid-input reasons are:

```text
case_05 → malformed_input
case_06 → malformed_input
case_07 → empty_input
case_08 → empty_input
```

---

# Git Workflow

## 1. Check Current Branch

```powershell
git branch --show-current
```

For the Day 1–4 work, the expected branch is:

```text
day-1-4
```

## 2. Check Status

```powershell
git status
```

## 3. Review Changes

```powershell
git diff
```

## 4. Review Staged Changes

```powershell
git diff --cached
```

---

# Stage Day 1–4 Work

Because multiple Day folders exist in the same repository, do not blindly use:

```powershell
git add .
```

Stage only the intended Day 1–4 files.

For example:

```powershell
git add "Genai day 1 to 4/"
```

Then verify:

```powershell
git status
```

---

# Commit Day 1–4

After the runtime and tests are verified:

```powershell
git commit -m "feat(day1-4): complete GenAI prompt and validation work"
```

Verify:

```powershell
git log -1 --oneline
```

---

# Push Day 1–4 Branch

```powershell
git push origin day-1-4
```

Verify:

```powershell
git fetch origin
```

```powershell
git log origin/day-1-4..day-1-4 --oneline
```

If there is no output, the local Day 1–4 branch has no unpushed commits.

---

# Merge Day 1–4 Into Main

After Day 1–4 testing and branch push are complete:

```powershell
git switch main
```

Update main safely:

```powershell
git pull --ff-only origin main
```

Merge:

```powershell
git merge --no-ff day-1-4
```

Push:

```powershell
git push origin main
```

---

# Final Git Verification

```powershell
git fetch origin
```

```powershell
git status
```

Check Day 1–4 versus main:

```powershell
git log main..day-1-4 --oneline
```

Check local main versus remote main:

```powershell
git log origin/main..main --oneline
```

When the branches are synchronized, both comparison commands should produce no
output.

---

# Complete Terminal Command List

## Setup

```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\Genai day 1 to 4"

python -m venv venv

.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

## Prompt Test Runner

```powershell
python scripts/run_prompt_tests.py
```

## Check Results

```powershell
Get-Content .\results\prompt_test_results.json
```

## Run Tests

```powershell
python -m pytest -v
```

## Clear Pytest Cache

```powershell
pytest -v --cache-clear
```

## Summarization

```powershell
python scripts/summarizer_runner.py
```

## Git Status

```powershell
git status
```

## Git Diff

```powershell
git diff
```

## Stage

```powershell
git add "Genai day 1 to 4/"
```

## Verify

```powershell
git status
```

## Commit

```powershell
git commit -m "feat(day1-4): complete GenAI prompt and validation work"
```

## Verify Commit

```powershell
git log -1 --oneline
```

## Push

```powershell
git push origin day-1-4
```

## Merge to Main

```powershell
git switch main

git pull --ff-only origin main

git merge --no-ff day-1-4

git push origin main
```

## Final Verification

```powershell
git fetch origin

git status

git log main..day-1-4 --oneline

git log origin/main..main --oneline
```

---

# Day 1–4 Final Checklist

## Prompt Work

- [ ] Classification prompt completed
- [ ] Extraction prompt completed
- [ ] Summarization prompt completed
- [ ] Prompt placeholders verified
- [ ] Prompt versions reviewed

## Sample Data

- [ ] Classification samples available
- [ ] Extraction samples available
- [ ] Summarization samples available
- [ ] Structured sample document available

## Validation

- [ ] Valid input accepted
- [ ] Ambiguous input represented
- [ ] Malformed input rejected
- [ ] Non-string input rejected
- [ ] Empty input rejected
- [ ] Whitespace-only input rejected

## Testing

- [ ] 10 prompt-test cases executed
- [ ] JSON result generated
- [ ] Total cases = 10
- [ ] Passed = 6
- [ ] Failed = 4
- [ ] Failure reasons verified

## Runtime

- [ ] Prompt test runner executed
- [ ] Result JSON inspected
- [ ] Summarization runner checked

## Project Quality

- [ ] Prompt files reviewed
- [ ] Sample files reviewed
- [ ] Versioned prompts reviewed
- [ ] Safety scaffolding reviewed
- [ ] Voice/audio scaffolding reviewed
- [ ] Generated files excluded where appropriate

## Git

- [ ] Day 1–4 branch selected
- [ ] Intended files staged
- [ ] Commit created
- [ ] Branch pushed
- [ ] Main updated safely
- [ ] Day 1–4 merged into main
- [ ] Main pushed
- [ ] Final Git verification completed

---

# Day 1–4 Completion

The Day 1–4 workflow is:

```text
Prompt Design
      ↓
Classification / Extraction / Summarization
      ↓
Prompt Versioning
      ↓
Sample Inputs
      ↓
Input Validation
      ↓
10 Prompt Test Cases
      ↓
Runtime Test Runner
      ↓
JSON Result Report
      ↓
Automated Verification
      ↓
Git Commit
      ↓
day-1-4 Branch
      ↓
Main Merge
      ↓
DAY 1–4 COMPLETED
```
