# Day 20 — Final Release Candidate

## Task 1 — Freeze the Release Candidate

The purpose of this task is to establish a reproducible baseline
before the final independent change.

## Frozen Information

- Project configuration
- Python version
- Dependency versions
- Prompt version
- Model version
- Database migration state
- Evaluation dataset version

## Release Artifact

The release metadata is stored in:

`release/release_candidate.json`

## Validation

Before freezing the release candidate:

```powershell
git status
python --version
pip freeze
pytest -v