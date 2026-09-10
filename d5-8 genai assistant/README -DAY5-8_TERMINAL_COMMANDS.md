# Day 5–8 Complete Terminal Commands

## Setup
```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\d5-8 genai assistant"
python --version
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Required packages
```text
numpy
chromadb
sentence-transformers
pydantic
scikit-learn
python-dotenv
pytest
```

## Day 5 output
```powershell
python .\scripts\generate_documents.py
python .\scripts\preprocess_documents.py
python .\scripts\inspect_chunks.py
```

## Day 6 output
```powershell
python .\scripts\generate_embeddings.py
python .\scripts\build_vector_index.py
python .\scripts\semantic_search.py
python .\scripts\search_with_filters.py
python .\scripts\evaluate_retrieval.py
```

## Day 7 output
```powershell
python .\src\rag\ingest.py
python .\src\rag\retrieve.py
python .\scripts\run_rag.py
python .\scripts\test_rag_pipeline.py
```

## Day 8 output
```powershell
python .\src\rag\demo_grounded_prompt.py
python .\src\rag\demo_citation_mapper.py
python .\src\rag\demo_abstention.py
python .\src\rag\demo_response_schema.py
python .\src\rag\demo_grounded_generation.py
```

## Complete tests
```powershell
pytest -v .\tests\test_abstention.py
pytest -v .\tests\test_citation_mapper.py
pytest -v .\tests\test_grounded_generation.py
pytest -v .\tests\test_grounded_prompt.py
pytest -v .\tests\test_response_schema.py
pytest -v .\tests\test_day08_pipeline.py
pytest -v
```
