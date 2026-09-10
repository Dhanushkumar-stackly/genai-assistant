# Day 05 — Prepare Documents, Chunks, and Retrieval Metadata

## Practical Goal
Create a reliable preprocessing pipeline that converts 30–50 approved documents into traceable chunks.

## Tasks

### Task 1 — Collect and sanitize the document set
Prepare 30–50 approved/sample documents, remove prohibited confidential content, and give every document a stable ID.

### Task 2 — Implement text loading and cleaning
Load plain text/Markdown/approved exported text, normalize whitespace, remove empty sections, and preserve meaningful headings.

### Task 3 — Implement configurable chunking
Split documents using configurable chunk size and overlap while preserving meaningful context. The project chunker defaults to `chunk_size=500` and `chunk_overlap=100`.

### Task 4 — Attach complete metadata
Attach traceability fields such as `chunk_id`, document ID, title, `source_path`, update information, `chunk_index`, and useful category/team metadata.

### Task 5 — Inspect chunk quality
Inspect short, long, and structured documents; fix heading splits, empty chunks, duplicate text, and excessive text.

## Required Deliverables
- Preprocessing script.
- Normalized chunk dataset.
- Metadata attached to every chunk.
- Chunk-quality review.

## Completion Gate
- 30–50 documents process without silent failures.
- Every chunk is traceable to its source.
- No empty chunks.
- Chunk size and overlap are configurable.

## End-of-Day Evidence
Show source documents and resulting chunks with metadata and one corrected chunking issue.

## Terminal Commands
```powershell
cd "d5-8 genai assistant"
python .\scripts\generate_documents.py
python .\scripts\preprocess_documents.py
python .\scripts\inspect_chunks.py
pytest -v .\tests\test_day08_pipeline.py
pytest -v
```
## Requirements

```powershell
python --version
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Required packages:
- numpy
- chromadb
- sentence-transformers
- pydantic
- scikit-learn
- python-dotenv
- pytest

Verify:
```powershell
python -c "import numpy, chromadb, sentence_transformers, pydantic, sklearn, dotenv, pytest; print('ALL REQUIRED PACKAGES INSTALLED SUCCESSFULLY')"
```
