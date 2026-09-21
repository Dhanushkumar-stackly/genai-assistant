# Operational Runbook

## Start

Activate the virtual environment.

.\venv\Scripts\Activate.ps1

## Run API

Use the documented application startup command.

## Health Verification

Verify that the API starts successfully.

## Ingestion

Run the documented ingestion command before querying
when the knowledge base has changed.

## Ask

Send a question through the `/ask` API.

## Voice

Run the Day 18 voice pipeline.

## Evaluation

Run the 25-case golden evaluation.

## Adversarial Verification

Run the 10-case adversarial suite.

## Release Verification

Run the complete pytest suite.