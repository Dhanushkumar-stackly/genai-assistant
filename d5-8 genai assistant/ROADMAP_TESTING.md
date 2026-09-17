# Day 5–7 Testing — Roadmap Aligned

## Day 5
The roadmap requires chunk-quality evidence. Pytest checks the resulting chunk dataset for non-empty chunks, unique IDs, traceability metadata, and the configured 500-character limit. The existing `inspect_chunks.py` and `chunk_quality_review.md` remain the primary review evidence.

Run:

```powershell
cd .\day-5\task-5
python -m pytest -v
python .\scripts\inspect_chunks.py
```

## Day 6
The roadmap requires a 10-question retrieval test set with expected source documents and top-three evaluation. The project contains 30 questions. Pytest validates the dataset structure; `evaluate_retrieval.py` performs the actual top-3 retrieval evaluation.

Run:

```powershell
cd .\day-6\task-5
python -m pytest -v
python .\scripts\evaluate_retrieval.py
```

## Day 7
The roadmap explicitly requires integration tests for ingest-then-retrieve behavior. The Day 7 Task 5 project is self-contained with the RAG retrieval/generation modules, integration tests, and vector index needed for the test run.

Run:

```powershell
cd .\day-7\task-5
python -m pytest -v
python .\scripts\test_rag_pipeline.py
```

## Master validation

Run each task from its own project root. Do not run one recursive pytest command from the common parent because the task projects intentionally contain separate `src` packages.
