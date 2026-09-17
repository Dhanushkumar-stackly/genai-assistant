# Day-5 — Task-5: Inspect chunk quality

**Roadmap task:** Inspect chunk quality

**Mapped source:** `scripts/inspect_chunks.py + outputs/chunk_quality_review.md`

Files are copied from the supplied project for task-wise organization. No missing implementation is fabricated.

## Roadmap Testing
The Day 5 roadmap requires chunk-quality evidence: no empty chunks, traceability, and configurable chunking. Automated checks are available in `tests/test_day05_quality.py`; `scripts/inspect_chunks.py` remains the review command.

```powershell
python -m pytest -v
python .\scripts\inspect_chunks.py
```
