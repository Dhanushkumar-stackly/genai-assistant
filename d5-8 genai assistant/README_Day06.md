# Day 06 — Build Vector Indexing and Semantic Search

## Practical Goal
Store document embeddings and return the most relevant chunks with scores and metadata.

## Tasks

### Task 1 — Generate embeddings
Generate embeddings for the Day 5 chunk dataset in batches and record the embedding model/version. The configured model is `all-MiniLM-L6-v2`, with batch size `32`.

### Task 2 — Create the vector index
Store vectors and metadata in the vector database and provide a repeatable index-building command. The project uses ChromaDB and collection `genai_documents`.

### Task 3 — Implement top-k semantic search
Accept a question, create its embedding, search the index, and return top-k text, score/distance, chunk ID, and metadata.

### Task 4 — Add filters and thresholds
Support metadata filtering, configurable `top_k`, and an optional evidence/score threshold.

### Task 5 — Create a retrieval test set
Create 10 questions with expected source documents and check whether the expected document appears in the top results.

## Required Deliverables
- Populated vector index.
- Semantic search.
- 10-question retrieval dataset.
- Retrieval report with scores and metadata.

## Completion Gate
- Relevant questions return useful top-three results.
- Results contain citation-ready metadata.
- Index and search commands are documented.
- A metadata-filtered search is demonstrated.

## End-of-Day Evidence
Show two successful retrieval examples and one weak result for improvement.

## Terminal Commands
```powershell
cd "d5-8 genai assistant"
python .\scripts\generate_embeddings.py
python .\scripts\build_vector_index.py
python .\scripts\semantic_search.py
python .\scripts\search_with_filters.py
python .\scripts\evaluate_retrieval.py
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
