# Day 08 — Add Grounded Generation, Citations, and Abstention

## Practical Goal
Generate answers only from retrieved evidence and return valid citations or a useful abstention response.

## Tasks

### Task 1 — Create the grounded answer prompt
Instruct the model to use only supplied context, avoid unsupported assumptions, cite source labels, and state when evidence is insufficient.

### Task 2 — Define the answer response model
Return structured answer text, source/citation references, chunk previews or retrieval information, grounded status, and response status.

### Task 3 — Map citations to source chunks
Validate that citations refer to retrieved chunks, reject invalid references, remove duplicates, and map chunk IDs to source information.

### Task 4 — Implement abstention
When evidence is insufficient, do not invent an answer. Return the safe fallback response.

### Task 5 — Test three question types
Test answerable, partially answerable, and unanswerable questions and verify answer, citation mapping, grounding, and abstention behavior.

## Required Deliverables
- Grounded Q&A pipeline.
- Validated response schema.
- Tests for the three question types.
- Example citation and abstention outputs.

## Completion Gate
- Answered responses contain valid sources.
- No citation points outside supplied context.
- Unsupported questions produce the agreed abstention response.
- The pipeline is reproducible from a command.

## End-of-Day Evidence
Demonstrate one cited answer and one unsupported question that is safely declined.

## Terminal Commands
```powershell
cd "d5-8 genai assistant"
python .\src\rag\demo_grounded_prompt.py
python .\src\rag\demo_citation_mapper.py
python .\src\rag\demo_abstention.py
python .\src\rag\demo_response_schema.py
python .\src\rag\demo_grounded_generation.py
```

Run Day 8 tests:
```powershell
pytest -v .\tests\test_abstention.py
pytest -v .\tests\test_citation_mapper.py
pytest -v .\tests\test_grounded_generation.py
pytest -v .\tests\test_grounded_prompt.py
pytest -v .\tests\test_response_schema.py
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
