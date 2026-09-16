# Day 4 — Task 4: Build a Prompt Test Runner

The supplied implementation includes:

- `run_prompt_tests.py`
- `test_run_prompt_tests.py`
- `prompt_test_results.json`

The runner records case ID, prompt version, model version, latency,
validation result, and failure reason, and writes a machine-readable JSON
result file.

The supplied runner validates test **inputs** and records the resulting
validation categories.
