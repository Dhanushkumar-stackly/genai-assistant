# Troubleshooting

## ModuleNotFoundError

Check:

1. Current working directory.
2. Virtual environment.
3. PYTHONPATH.
4. pytest.ini.
5. Package names.

## Missing Environment Variable

Check `.env.example`.

Never commit actual secrets.

## API Failure

Check:

- API process
- configuration
- database
- logs
- request payload

## Retrieval Failure

Check:

- ingestion completed
- vector database available
- collection exists
- query reaches retriever
- source IDs are returned

## TTS Failure

The system should preserve the validated text answer
and sources.

## STT Failure

The system must stop before RAG.

## Test Failure

Run the failing test individually:

pytest path/to/test.py -v 