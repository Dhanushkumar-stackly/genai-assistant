# Day 10 — Implement Advanced Retrieval and Prove Improvement

## Practical Goal

Improve weak retrieval cases using measured experiments such as **query rewriting, multi-query retrieval, hybrid search, reranking, or context selection**.

## Tasks to Complete

### Task 1 — Run chunking and top-k experiments

Execute planned configuration changes and compare them against the frozen baseline.

The experiment results must remain auditable and should record the configurations and metrics used.

The project includes:

- Baseline retrieval results
- Chunking experiment
- Experiment comparison

### Task 2 — Add query rewriting or multi-query retrieval

Generate a clearer search query or several related queries.

The process should:

1. Generate rewritten/related queries.
2. Retrieve candidate chunks.
3. Combine candidate results.
4. Remove duplicates.
5. Rank the combined candidates.

### Task 3 — Add hybrid retrieval or reranking

Combine keyword/vector candidates or rerank a candidate set.

The project implements reranking using a cross-encoder configuration and preserves original retrieval scores together with the final selected order.

Configured reranker:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

### Task 4 — Choose the best configuration

Select the configuration that improves weak cases without creating unacceptable regressions on previously successful questions.

The selection considers:

- Retrieval recall
- Top-1 accuracy
- MRR
- Question-level regressions
- Question-level improvements

The final configuration must be documented and versioned.

### Task 5 — Produce a before-and-after report

Show:

- Per-question results
- Aggregate retrieval metrics
- Latency impact
- Selected trade-off
- Rejected approaches and why they were rejected

## Required Deliverables

- At least two implemented retrieval improvements/experiments.
- Selected retrieval configuration used by the RAG pipeline.
- Before-and-after metric report.
- Regression analysis.

## Completion Gate

- Selected approach demonstrates measured retrieval gain.
- Previously passing questions are checked for regression.
- Latency and quality impact are recorded.
- Final configuration is versioned and documented.

## End-of-Day Evidence

Demonstrate one question that improved and one experiment rejected because the evidence did not support it.

## Project Outputs

The Day 10 project contains artifacts such as:

```text
outputs/day10_task1_baseline_results.json
outputs/day10_task1_chunking_experiment.json
outputs/day10_task1_experiment_results.json
outputs/day10_task2_multi_query_results.json
outputs/day10/task3/reranking_results.json
outputs/day10_task4_best_configuration.json
outputs/day10_task5_before_after_report.json
outputs/day10_task5_before_after_report.txt
```

## Terminal Commands

Run from:

```powershell
cd "d9-d10 genai"
```

### Task 1 — Experiments

```powershell
python .\src\day10\task1_experiments.py
python .\src\day10\task1_chunking_experiment.py
```

### Task 2 — Multi-query retrieval

```powershell
python .\src\day10\task2_multi_query.py
```

### Task 3 — Reranking

```powershell
python .\src\day10\task3_reranking.py
```

### Task 4 — Select best configuration

```powershell
python .\src\day10\task4_choose_best_configuration.py
```

### Task 5 — Before/after report

```powershell
python .\src\day10\task5_before_after_report.py
```

### Run all Day 10 tests

```powershell
pytest -v .\tests\test_task1_experiments.py
pytest -v .\tests\test_task1_chunking_experiment.py
pytest -v .\tests\test_task2_multi_query.py
pytest -v .\tests\test_day10_task3.py
pytest -v .\tests\test_task4_choose_best_configuration.py
pytest -v .\tests\test_task5_before_after_report.py
pytest -v
```

