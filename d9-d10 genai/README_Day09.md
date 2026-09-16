# Day 09 — Diagnose Retrieval Failures and Define Controlled Experiments

## Practical Goal

Use the weakest baseline questions to identify retrieval problems and design measurable **one-variable-at-a-time experiments**.

## Tasks to Complete

### Task 1 — Freeze the baseline configuration

Record the current retrieval configuration before making changes, including:

- Embedding model
- Chunk size
- Chunk overlap
- Top-k
- Metadata filters
- Score/evidence threshold
- Prompt version

The frozen baseline must remain available for comparison and auditability.

### Task 2 — Select the five weakest questions

Use the Day 6 and Day 8 retrieval/evaluation results to identify questions with:

- Missing expected sources
- Wrong ranking
- Incomplete context
- Unnecessary abstention

The selected weak questions are stored for controlled experimentation.

### Task 3 — Classify each failure

Give each weak retrieval case a failure label based on retrieved evidence, such as:

- Poor chunk boundary
- Vocabulary mismatch
- Broad query
- Missing metadata
- Low ranking
- Excessive context

The diagnosis must be evidence-based rather than guessed.

### Task 4 — Create an experiment matrix

For every weak question, define:

- Baseline configuration
- One proposed change
- Expected effect
- Measurement criteria

Candidate variables include:

- Chunk size
- Overlap
- Top-k
- Metadata filter
- Query rewrite

Only one primary variable should change in each experiment.

### Task 5 — Measure baseline retrieval metrics

Calculate and save baseline metrics such as:

- Hit rate
- Recall@k
- Mean Reciprocal Rank (MRR)
- Per-question retrieval result

Save the complete question-level results, not only aggregate metrics.

## Required Deliverables

- Frozen baseline configuration file.
- Five-question failure analysis.
- Controlled experiment plan showing the changed variable.
- Baseline metric report.

## Completion Gate

- Every experiment changes only one primary variable.
- Every weak question has an expected source document.
- Baseline measurements can be rerun from one command.
- Failure labels are based on retrieved evidence.

## End-of-Day Evidence

Explain the root-cause hypothesis for each weak question and the measurement that will confirm or reject it.

## Project Outputs

The Day 9 project contains artifacts such as:

```text
config/baseline_config.json
data/weak_questions.json
outputs/baseline_report.txt
outputs/retrieval_failure_diagnosis.json
outputs/controlled_experiment_results.json
outputs/day09_final_report.json
```

## Terminal Commands

Run from:

```powershell
cd "d9-d10 genai"
```

Freeze the baseline:

```powershell
python .\src\day09\freeze_baseline.py
```

Select weak questions:

```powershell
python .\src\day09\task2_weak_questions.py
```

Run retrieval-failure diagnosis:

```powershell
python .\src\diagnose_retrieval_failures.py
```

Run the controlled experiment:

```powershell
python .\src\run_controlled_experiment.py
```

Generate the experiment report:

```powershell
python .\src\generate_experiment_report.py
```

Run all tests:

```powershell
pytest -v
```

## Tests

```powershell
pytest -v .\tests\test_baseline.py
pytest -v .\tests\test_select_weak_questions.py
pytest -v .\tests\test_diagnose_retrieval_failures.py
pytest -v .\tests\test_controlled_experiment.py
pytest -v
```

