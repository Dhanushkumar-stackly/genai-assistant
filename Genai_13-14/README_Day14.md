# GenAI Evaluation Framework — Day 14

## 1. Day 14 Objective

Day 14 adds **automated RAG quality grading, scorecards, regression detection, and final evaluation reporting**.

Day 14 contains **5 tasks**:

1. Retrieval Grading
2. Answer Grading
3. Evaluation Scorecard
4. Regression Detection
5. PASS / REGRESSION Evaluation Report

---

# 2. Task 1 — Retrieval Grading

### File

```text
eval/graders/retrieval_grader.py
tests/test_day14_task1.py
```

The retrieval grader evaluates whether the RAG system retrieved the correct source documents.

It implements:

```text
Hit@K
Recall@K
Reciprocal Rank
Mean Reciprocal Rank
```

## Hit@K

Returns:

```text
1.0 → expected source appears in top K
0.0 → expected source does not appear
```

Example:

```text
Expected:  doc-A
Retrieved: doc-B, doc-A, doc-C
K = 3

Hit@3 = 1.0
```

## Recall@K

Measures the fraction of expected sources retrieved in the top K.

Example:

```text
Expected:  doc-A, doc-B
Retrieved: doc-A, doc-C
K = 2

Recall@2 = 0.5
```

## Reciprocal Rank

Measures the reciprocal position of the first expected source.

```text
Rank 1 → 1.0
Rank 2 → 0.5
Rank 3 → 0.333...
```

## Mean Reciprocal Rank

Averages reciprocal rank across cases.

### Combined result

```python
{
    "hit_at_k": 1.0,
    "recall_at_k": 1.0,
    "reciprocal_rank": 0.5
}
```

### Test

```powershell
python -m pytest -v tests/test_day14_task1.py
```

---

# 3. Task 2 — Answer Grading

### File

```text
eval/graders/answer_grader.py
tests/test_day14_task2.py
```

The answer grader evaluates response quality.

It checks:

```text
answerability correctness
citation presence
citation validity
required facts
correct abstention
```

## Answerability

An answerable case requires a non-empty answer.

An unanswerable case should produce an abstention.

## Citation Presence

Checks whether the answer has at least one citation ID.

## Citation Validity

Every cited source must exist in the retrieved source IDs.

## Required Facts

Checks whether every required fact occurs in the answer using case-insensitive normalized matching.

## Abstention Detection

Recognizes phrases such as:

```text
I don't know
I do not know
I don't have enough information
cannot answer
unable to answer
insufficient information
no information available
```

## Complete answer grading result

```python
{
    "answerability_correct": True,
    "citation_present": True,
    "citation_valid": True,
    "required_facts_correct": True,
    "abstention_correct": True
}
```

### Test

```powershell
python -m pytest -v tests/test_day14_task2.py
```

---

# 4. Task 3 — Evaluation Scorecard

### File

```text
eval/scorecard.py
tests/test_day14_task3.py
```

The scorecard combines retrieval and answer-quality measurements.

## Retrieval Score

Average of:

```text
Hit@K
Recall@K
Reciprocal Rank
```

For:

```text
1.0
1.0
0.5
```

the retrieval score is:

```text
0.8333333333333334
```

## Answer Score

Average of five boolean quality metrics:

```text
answerability_correct
citation_present
citation_valid
required_facts_correct
abstention_correct
```

All five correct:

```text
1.0
```

## Overall Score

The overall score is the average of:

```text
retrieval_score
answer_score
```

Example:

```text
retrieval_score = 0.8333333333333334
answer_score    = 1.0

overall_score   = 0.9166666666666667
```

### Scorecard output

```python
{
    "retrieval_score": 0.8333333333333334,
    "answer_score": 1.0,
    "overall_score": 0.9166666666666667
}
```

### Test

```powershell
python -m pytest -v tests/test_day14_task3.py
```

---

# 5. Task 4 — Regression Detection

### File

```text
eval/regression.py
tests/test_day14_task4.py
```

Regression detection compares a baseline scorecard with the current scorecard.

Metrics compared:

```text
retrieval_score
answer_score
overall_score
```

## Difference

The implementation calculates:

```text
baseline - current
```

Example:

```text
baseline = 0.90
current  = 0.85

difference = 0.05
```

## Regression

Without a threshold:

```text
baseline 0.90
current  0.80

→ regression detected
```

With threshold:

```text
baseline = 0.90
current  = 0.89
threshold = 0.02

→ no regression
```

But:

```text
baseline = 0.90
current  = 0.85
threshold = 0.02

→ regression
```

## Scorecard comparison output

The comparison includes:

```text
baseline
current
difference
regression
```

for each metric, plus:

```text
regression_detected
```

### Test

```powershell
python -m pytest -v tests/test_day14_task4.py
```

---

# 6. Task 5 — Final Evaluation Report

### File

```text
eval/report.py
tests/test_day14_task5.py
```

The final report combines:

```text
scorecard
regression result
```

## PASS

When:

```text
regression_detected = false
```

the report status is:

```text
PASS
```

## REGRESSION

When:

```text
regression_detected = true
```

the report status is:

```text
REGRESSION
```

Example:

```python
{
    "status": "PASS",
    "scorecard": {
        "retrieval_score": 0.83,
        "answer_score": 1.0,
        "overall_score": 0.915
    },
    "regression": {
        "regression_detected": False,
        "threshold": 0.02,
        "metrics": {}
    }
}
```

The helper:

```text
is_evaluation_passed()
```

returns:

```text
True → PASS
False → REGRESSION
```

The helper:

```text
get_overall_score()
```

returns the scorecard's `overall_score`, or `0.0` when it is missing.

### Test

```powershell
python -m pytest -v tests/test_day14_task5.py
```

---

# 7. Day 14 Complete Flow

```text
RAG Retrieval
      ↓
Retrieval Grader
      ↓
Hit@K / Recall@K / RR / MRR
      ↓
Answer
      ↓
Answer Grader
      ↓
Answerability / Citation / Facts / Abstention
      ↓
Scorecard
      ↓
Retrieval Score + Answer Score
      ↓
Overall Score
      ↓
Compare with Baseline
      ↓
Regression Detection
      ↓
Final Report
      ↓
PASS / REGRESSION
```

---

# 8. Day 14 Project Structure

```text
Genai_13-14/
│
├── eval/
│   ├── graders/
│   │   ├── __init__.py
│   │   ├── answer_grader.py
│   │   └── retrieval_grader.py
│   │
│   ├── regression.py
│   ├── report.py
│   └── scorecard.py
│
└── tests/
    ├── test_day14_task1.py
    ├── test_day14_task2.py
    ├── test_day14_task3.py
    ├── test_day14_task4.py
    └── test_day14_task5.py
```

---

# 9. Requirements — Day 14

The Day 14 implementation uses Python standard-library functionality for its grading, scorecard, regression, and report logic.

The tests require:

```text
pytest
```

Recommended pinned requirement:

```text
pytest==9.1.1
```

No FastAPI, SQLAlchemy, ChromaDB, or other Day 11/12 runtime dependencies are required by the Day 14 evaluation modules.

---

# 10. Environment Setup — All Terminal Commands

Go to the project:

```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\Genai_13-14"
```

Create venv:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify interpreter:

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

# 11. Day 14 Runtime Demonstrations

The Day 14 modules are evaluation utilities rather than a web server, so runtime verification is performed with Python commands and pytest.

### Retrieval grading

```powershell
python -c "from eval.graders.retrieval_grader import grade_retrieval_case; print(grade_retrieval_case(['doc-A'], ['doc-B','doc-A','doc-C'], 3))"
```

Expected:

```text
{'hit_at_k': 1.0, 'recall_at_k': 1.0, 'reciprocal_rank': 0.5}
```

### Answer grading

```powershell
python -c "from eval.graders.answer_grader import grade_answer_case; print(grade_answer_case(expected_answerable=True, answer='Employees get 20 days of leave.', citation_ids=['doc-leave'], retrieved_source_ids=['doc-leave','doc-benefits'], required_facts=['20 days']))"
```

Expected:

```text
{
  'answerability_correct': True,
  'citation_present': True,
  'citation_valid': True,
  'required_facts_correct': True,
  'abstention_correct': True
}
```

### Scorecard

```powershell
python -c "from eval.scorecard import build_scorecard; print(build_scorecard([{'hit_at_k':1.0,'recall_at_k':1.0,'reciprocal_rank':0.5}], [{'answerability_correct':True,'citation_present':True,'citation_valid':True,'required_facts_correct':True,'abstention_correct':True}]))"
```

Expected:

```text
{
  'retrieval_score': 0.8333333333333334,
  'answer_score': 1.0,
  'overall_score': 0.9166666666666667
}
```

### Regression

```powershell
python -c "from eval.regression import compare_scorecards; print(compare_scorecards({'retrieval_score':0.90,'answer_score':0.95,'overall_score':0.925},{'retrieval_score':0.85,'answer_score':0.96,'overall_score':0.905},threshold=0.02))"
```

Expected:

```text
regression_detected = True
```

### Final report

```powershell
python -c "from eval.report import build_evaluation_report; print(build_evaluation_report(scorecard={'retrieval_score':0.83,'answer_score':1.0,'overall_score':0.915}, regression={'regression_detected':False,'threshold':0.02,'metrics':{}}))"
```

Expected:

```text
status = PASS
```

---

# 12. Day 14 Tests — All Commands

Task 1:

```powershell
python -m pytest -v tests/test_day14_task1.py
```

Task 2:

```powershell
python -m pytest -v tests/test_day14_task2.py
```

Task 3:

```powershell
python -m pytest -v tests/test_day14_task3.py
```

Task 4:

```powershell
python -m pytest -v tests/test_day14_task4.py
```

Task 5:

```powershell
python -m pytest -v tests/test_day14_task5.py
```

All Day 14 tests:

```powershell
python -m pytest -v tests/test_day14_*.py
```

Full project:

```powershell
python -m pytest -v
```

---

# 13. Day 14 Test Count

The supplied test files contain:

```text
Task 1 → 9 tests
Task 2 → 13 tests
Task 3 → 7 tests
Task 4 → 8 tests
Task 5 → 7 tests
-----------------
Day 14 → 44 tests
```

Combined with Day 13:

```text
Day 13 → 38 tests
Day 14 → 44 tests
-----------------
Total  → 82 tests
```

---

# 14. Day 14 Completion Checklist

```text
[ ] Hit@K implemented
[ ] Recall@K implemented
[ ] Reciprocal Rank implemented
[ ] Mean Reciprocal Rank implemented
[ ] Answerability grading implemented
[ ] Citation presence implemented
[ ] Citation validation implemented
[ ] Required-fact checking implemented
[ ] Abstention detection implemented
[ ] Retrieval score implemented
[ ] Answer score implemented
[ ] Overall score implemented
[ ] Baseline comparison implemented
[ ] Regression threshold implemented
[ ] Regression detection implemented
[ ] PASS report implemented
[ ] REGRESSION report implemented
[ ] Overall-score extraction implemented
[ ] Day 14 tests pass
```

Day 14 is verified only after the actual terminal run reports all Day 14 tests as `PASSED`.
