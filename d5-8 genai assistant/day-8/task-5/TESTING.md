# Day 08 Task 5 - Testing

Run from this directory:

```bash
pytest -v
```

The unit tests for abstention, citation mapping, grounded generation,
grounded prompts, and response schema are included under `tests/`.

The integration test `test_day08_pipeline.py` requires the packages in
`requirements.txt` (`chromadb` and `sentence-transformers`) and the
provided ChromaDB data under `outputs/chroma_db`.
