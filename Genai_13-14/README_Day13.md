# GenAI Evaluation Framework — Day 13

## 1. Day 13 Objective

Day 13 builds the **Golden Evaluation Dataset and Evaluation Runner** for a GenAI/RAG system.

The implementation is located under:

```text
eval/
```

Day 13 contains **5 tasks**:

1. Evaluation Case Schema
2. Golden Dataset
3. Dataset Review and Consistency Checks
4. Evaluation Runner
5. Versioned Configuration and Evaluation Artifacts

---

# 2. Task 1 — Evaluation Case Schema

### Files

```text
eval/evaluation_case.schema.json
tests/test_day13_task1.py
```

The JSON Schema defines the structure of one evaluation case.

### Required fields

```text
case_id
question
category
expected_source_ids
answerability
```

### Optional fields

```text
expected_facts
answer_notes
```

### Supported categories

```text
answerable
unanswerable
ambiguous
multi_document
adversarial
```

### Answerability values

```text
answerable
unanswerable
ambiguous
```

### Case ID format

```text
D13-001
D13-002
...
```

Pattern:

```text
^D13-[0-9]{3}$
```

Additional properties are disabled so unexpected fields are rejected.

### Test

```powershell
python -m pytest -v tests/test_day13_task1.py
```

---

# 3. Task 2 — Golden Evaluation Dataset

### Files

```text
eval/golden_dataset.json
tests/test_day13_task2.py
```

The dataset contains exactly **25 cases**.

Distribution:

| Category | Cases |
|---|---:|
| answerable | 5 |
| unanswerable | 5 |
| ambiguous | 5 |
| multi_document | 5 |
| adversarial | 5 |
| **Total** | **25** |

The tests verify:

- Dataset exists.
- At least 25 cases exist.
- Case IDs are unique.
- All five categories are represented.
- Required fields exist in every case.
- Answerable cases contain expected sources.
- Unanswerable cases contain no expected sources.
- Multi-document cases contain at least two expected sources.
- Ambiguous cases have no expected sources.
- Adversarial cases have source grounding.
- Optional review fields exist.

### Test

```powershell
python -m pytest -v tests/test_day13_task2.py
```

---

# 4. Task 3 — Dataset Review

### Files

```text
eval/dataset_review.md
tests/test_day13_task3.py
```

The review document contains:

```text
# Day 13 Golden Dataset Review
Review Objective
Category Review
Review Findings
Dataset Consistency Checks
```

The implementation validates that evaluation cases contain scoreable metadata.

Important consistency rules:

```text
answerable
    → at least one expected source

unanswerable
    → no expected sources

multi_document
    → multiple expected sources

ambiguous
    → answerability = ambiguous
    → no expected sources

adversarial
    → at least one expected source
    → answerability = answerable
```

### Test

```powershell
python -m pytest -v tests/test_day13_task3.py
```

---

# 5. Task 4 — Evaluation Runner

### Files

```text
eval/evaluation_runner.py
tests/test_day13_task4.py
```

The evaluation runner:

1. Loads the golden dataset.
2. Sends every question to a responder.
3. Compares returned source IDs with expected source IDs.
4. Evaluates answerability.
5. Produces per-case results.
6. Counts passed and failed cases.

### Core evaluation behavior

For `unanswerable` cases:

```text
No retrieved sources → pass
Retrieved sources → fail
```

For `ambiguous` cases:

```text
No retrieved sources → pass
Retrieved sources → fail
```

For answerable cases:

```text
Expected sources must be included in actual sources.
```

### Report structure

```json
{
  "total_cases": 25,
  "passed": 0,
  "failed": 25,
  "results": []
}
```

The actual counts depend on the responder used.

### Test

```powershell
python -m pytest -v tests/test_day13_task4.py
```

---

# 6. Task 5 — Versioned Configuration and Result Artifacts

### Files

```text
eval/config/evaluation_config.json
eval/results/
tests/test_day13_task5.py
```

Current configuration:

```json
{
  "runner_version": "1.0.0",
  "dataset_version": "day13-v1",
  "dataset_path": "eval/golden_dataset.json",
  "results_dir": "eval/results"
}
```

The runner creates unique timestamped result files:

```text
evaluation_YYYYMMDDTHHMMSS_microsecondsZ.json
```

Each saved artifact contains:

```text
run_metadata
configuration
report
```

Metadata includes:

```text
timestamp_utc
runner_version
dataset_version
config_path
```

### Test

```powershell
python -m pytest -v tests/test_day13_task5.py
```

---

# 7. Day 13 Complete Flow

```text
Evaluation Case Schema
        ↓
Golden Dataset
        ↓
Dataset Review
        ↓
Evaluation Runner
        ↓
Case-by-case evaluation
        ↓
Pass / Fail report
        ↓
Timestamped JSON artifact
```

---

# 8. Day 13 Project Structure

```text
Genai_13-14/
│
├── eval/
│   ├── config/
│   │   └── evaluation_config.json
│   │
│   ├── graders/
│   │   ├── __init__.py
│   │   ├── answer_grader.py
│   │   └── retrieval_grader.py
│   │
│   ├── results/
│   ├── __init__.py
│   ├── dataset_review.md
│   ├── evaluation_case.schema.json
│   ├── evaluation_runner.py
│   ├── golden_dataset.json
│   ├── regression.py
│   ├── report.py
│   └── scorecard.py
│
├── tests/
│   ├── test_day13_task1.py
│   ├── test_day13_task2.py
│   ├── test_day13_task3.py
│   ├── test_day13_task4.py
│   ├── test_day13_task5.py
│   ├── test_day14_task1.py
│   ├── test_day14_task2.py
│   ├── test_day14_task3.py
│   ├── test_day14_task4.py
│   └── test_day14_task5.py
│
└── pytest.ini
```

---

# 9. Requirements — Day 13

The Day 13 implementation uses Python standard-library modules for its evaluation logic.

The test framework requires:

```text
pytest
```

Recommended pinned requirements for this project:

```text
pytest==9.1.1
```

No FastAPI, SQLAlchemy, ChromaDB, or other Day 11/12 dependencies are imported by the Day 13 evaluation implementation.

---

# 10. Environment Setup — All Terminal Commands

Go to the project:

```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\Genai_13-14"
```

Create virtual environment:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify Python:

```powershell
python -c "import sys; print(sys.executable)"
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install requirements:

```powershell
python -m pip install -r requirements.txt
```

Verify pytest:

```powershell
python -m pytest --version
```

---

# 11. Day 13 Runtime Output

Run the evaluation runner:

```powershell
python -m eval.evaluation_runner
```

The built-in CLI uses a **demo responder that returns no sources**.

Therefore, this is deliberately not a real RAG-quality result.

With the supplied 25-case dataset, the expected demo pattern is:

```text
Total cases: 25
Passed: 10
Failed: 15
Result artifact: eval/results/evaluation_<timestamp>.json
```

The 10 passing cases come from the five `unanswerable` and five `ambiguous` cases because the demo responder returns no sources.

The 15 source-grounded cases fail because the demo responder returns no sources.

This must not be reported as the actual performance of a real RAG system.

---

# 12. Day 13 Result Artifact

After running:

```powershell
python -m eval.evaluation_runner
```

list result files:

```powershell
Get-ChildItem .\eval\results\
```

Read the newest result:

```powershell
Get-ChildItem .\eval\results\ | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

Open a result:

```powershell
Get-Content .\eval\results\<RESULT_FILE>.json
```

---

# 13. Day 13 Tests — All Commands

Task 1:

```powershell
python -m pytest -v tests/test_day13_task1.py
```

Task 2:

```powershell
python -m pytest -v tests/test_day13_task2.py
```

Task 3:

```powershell
python -m pytest -v tests/test_day13_task3.py
```

Task 4:

```powershell
python -m pytest -v tests/test_day13_task4.py
```

Task 5:

```powershell
python -m pytest -v tests/test_day13_task5.py
```

All Day 13 tests:

```powershell
python -m pytest -v tests/test_day13_*.py
```

Full project suite:

```powershell
python -m pytest -v
```

---

# 14. Day 13 Test Count

The supplied test files contain:

```text
Task 1 → 7 tests
Task 2 → 9 tests
Task 3 → 8 tests
Task 4 → 7 tests
Task 5 → 7 tests
-----------------
Day 13 → 38 tests
```

The complete Day 13 + Day 14 suite contains **82 tests**.

---

# 15. Day 13 Completion Checklist

```text
[ ] Evaluation schema exists
[ ] Required schema fields defined
[ ] Optional schema fields defined
[ ] Five evaluation categories defined
[ ] Answerability values defined
[ ] Case ID pattern defined
[ ] Additional properties disabled
[ ] Golden dataset contains 25 cases
[ ] Case IDs are unique
[ ] Five categories have 5 cases each
[ ] Dataset review exists
[ ] Evaluation runner loads all cases
[ ] Evaluation results contain required fields
[ ] Configuration file exists
[ ] Dataset version is day13-v1
[ ] Runner version is 1.0.0
[ ] Timestamped artifacts are created
[ ] Day 13 tests pass
```

Day 13 is verified only after the actual terminal run reports all Day 13 tests as `PASSED`.
