# Requirements / Dependencies

The supplied Day 9–10 project `requirements.txt` is currently empty, so the dependencies should be declared before distributing the project.

Python standard-library modules used by the project do not need installation. The external packages imported by the project are:

```text
chromadb
sentence-transformers
```

Recommended setup:

```powershell
cd "d9-d10 genai"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install chromadb sentence-transformers pytest
```

For a permanent project setup, put these in `requirements.txt`:

```text
chromadb
sentence-transformers
pytest
```

Then install with:

```powershell
python -m pip install -r requirements.txt
```

Verify:

```powershell
python -c "import chromadb; import sentence_transformers; import pytest; print('DAY 9-10 REQUIREMENTS INSTALLED SUCCESSFULLY')"
```
