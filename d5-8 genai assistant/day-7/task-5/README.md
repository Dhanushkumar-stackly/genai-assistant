# Day-7 — Task-5: Add pipeline-level checks

**Roadmap task:** Add pipeline-level checks

**Mapped source:** `scripts/test_rag_pipeline.py`

Files are copied from the supplied project for task-wise organization. No missing implementation is fabricated.

## Roadmap Testing
The Day 7 roadmap explicitly requires integration tests for ingest-then-retrieve behavior. This task contains a self-contained RAG test project with retrieval/generation modules, integration tests, and the vector index required for the test run.

```powershell
python -m pytest -v
python .\scripts\test_rag_pipeline.py
```
