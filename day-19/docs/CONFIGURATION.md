# Configuration Guide

## Application Configuration

The application configuration must be documented before
starting the services.

## Service URL

RAG API:

http://127.0.0.1:8000

## API Endpoint

Ask:

POST /ask

## Health

GET /health

## Ingestion

POST /ingest

## Environment Variables

Document every required variable here.

Example:

VARIABLE_NAME=<value>

Never commit:

- API keys
- passwords
- tokens
- credentials
- private secrets

## Configuration Precedence

Document which source has priority:

1. Environment variables
2. .env configuration
3. Application defaults

## Model Configuration

Record:

- Model/provider
- Model version
- Embedding model
- Embedding version

## Prompt Configuration

Record:

- Prompt name
- Prompt version
- Prompt change date

## Database

Record:

- Database type
- Database location
- Migration state
- Schema version

## Evaluation Dataset

Record:

- Dataset name
- Dataset version
- Number of cases
- Last updated date