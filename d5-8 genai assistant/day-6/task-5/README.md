# Day-6 — Task-5: Create a retrieval test set

**Roadmap task:** Create a retrieval test set

**Mapped source:** `data/retrieval_questions.json + scripts/evaluate_retrieval.py`

Files are copied from the supplied project for task-wise organization. No missing implementation is fabricated.

## Roadmap Testing
The Day 6 roadmap requires a retrieval test set with expected source documents and a top-three evaluation. This task contains the 30-question dataset, a pytest schema check, and the executable top-3 evaluation.

```powershell
python -m pytest -v
python .\scripts\evaluate_retrieval.py
```
