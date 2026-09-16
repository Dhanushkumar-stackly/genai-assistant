# Day 07 — Implement Baseline RAG Ingestion and Retrieval

## Practical Goal
Connect document loading, chunking, embedding, indexing, and retrieval into one understandable pipeline.

## Tasks

### Task 1 — Separate the RAG modules
Create clear modules such as `ingest.py`, `retrieve.py`, and `generate.py`, keeping each stage independently callable.

### Task 2 — Build the ingestion flow
Accept approved documents, clean and chunk them, generate embeddings, store vectors, record processing events, and make re-ingestion behavior explicit.

### Task 3 — Build the retrieval flow
Accept a question, generate the query embedding, retrieve relevant chunks, and return scores/distances and metadata while applying `top_k`, filters, and evidence thresholds.

### Task 4 — Prepare context for generation
Format retrieved chunks with stable source labels, remove duplicates, and limit context to selected evidence.

### Task 5 — Add pipeline-level checks
Verify ingestion and retrieval and ensure a failed document is logged without stopping other documents.

## Required Deliverables
- Separate ingestion/retrieval modules.
- Ingestion command.
- Retrieval-context command.
- Integration events/logging.
- Pipeline tests.

## Completion Gate
- Full RAG flow is visible in code.
- Re-ingestion does not create uncontrolled duplicates.
- Retrieved context contains stable source labels.
- Integration tests pass.

## End-of-Day Evidence
Walk through one document from raw input to retrieved context.

## Terminal Commands
```powershell
cd "d5-8 genai assistant"
python .\src\rag\ingest.py
python .\src\rag\retrieve.py
python .\scripts\run_rag.py
python .\scripts\test_rag_pipeline.py
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
