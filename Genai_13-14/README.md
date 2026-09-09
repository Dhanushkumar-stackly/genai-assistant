# GenAI Evaluation Framework — Day 13 & Day 14

This project contains the Day 13 and Day 14 evaluation framework for a RAG system.

## Day 13 — Golden Evaluation Dataset

- Defines a JSON evaluation-case schema.
- Contains 25 golden cases.
- Covers five categories:
  - answerable
  - unanswerable
  - ambiguous
  - multi_document
  - adversarial
- Includes dataset review notes.
- Provides an evaluation runner.
- Stores timestamped JSON evaluation artifacts.
- Uses a versioned configuration file.

## Day 14 — Evaluation Grading

- Retrieval grading:
  - Hit@K
  - Recall@K
  - Reciprocal Rank
  - Mean Reciprocal Rank
- Answer grading:
  - answerability
  - citation presence
  - citation validity
  - required facts
  - correct abstention
- Scorecard:
  - retrieval score
  - answer score
  - overall score
- Regression detection with configurable threshold.
- Consolidated PASS / REGRESSION reporting.

## Project Structure

```text
Genai 13 & 14/
├── eval/
│   ├── config/
│   │   └── evaluation_config.json
│   ├── graders/
│   │   ├── answer_grader.py
│   │   └── retrieval_grader.py
│   ├── results/
│   ├── dataset_review.md
│   ├── evaluation_case.schema.json
│   ├── evaluation_runner.py
│   ├── golden_dataset.json
│   ├── regression.py
│   ├── report.py
│   └── scorecard.py
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
└── pytest.ini
```

## Run Tests

```powershell
pytest -v
```

Expected verification for this package:

```text
82 passed
```

## Run the Evaluation Runner

```powershell
python -m eval.evaluation_runner
```

The runner uses the built-in demo responder. It intentionally returns no sources, so the demo run is **not** a real RAG-quality score. With the included 25-case dataset, unanswerable and ambiguous cases pass while source-grounded answerable cases fail.

A typical demo result is:

```text
Total cases: 25
Passed: 10
Failed: 15
Result artifact: eval/results/evaluation_<timestamp>.json
```

For a real evaluation, connect `run_evaluation()` or `run_configured_evaluation()` to the actual RAG responder so the returned `sources` contain document IDs from the golden dataset.

## Important Day 14 Flow

```text
RAG response
    ↓
Retrieval grader
    ↓
Answer grader
    ↓
Scorecard
    ↓
Baseline comparison
    ↓
Regression detection
    ↓
PASS / REGRESSION report
```

## Verification Status

- All Day 13 tests pass.
- All Day 14 tests pass.
- Full suite: 82 tests passed.
- The evaluation runner executes successfully and creates a timestamped JSON artifact.
- The included CLI runner is a demonstration runner, not a claim that the underlying RAG system achieved a passing evaluation score.
