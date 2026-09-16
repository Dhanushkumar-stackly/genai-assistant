# Day 1–4 Taskwise Fixed Project

This package keeps `main`, Day 1, Day 2, Day 3, and Day 4 separate and provides executable tests for the supplied task split.

## Test

From this project root:

```bash
pytest -q
```

Expected result for the included task tests: **20 passed**.

Day 1 and Day 2 contain documentation only because the supplied taskwise source did not contain their implementation files. Missing implementation was not silently invented.

Day 3 includes an offline model-client wrapper and prompt builders so the prompt work can be tested without an API key.

Day 4 includes output models, response validation, a populated 10-case dataset, a repeatable prompt test runner, and version comparison fixtures.
