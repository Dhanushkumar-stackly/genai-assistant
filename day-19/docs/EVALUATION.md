# Evaluation Guide

## Golden Evaluation

Dataset:

25 cases.

Categories:

- answerable
- unanswerable
- ambiguous
- multi-document
- adversarial

Run:

python -m eval.evaluation_runner

## Adversarial Evaluation

Run the 10-case adversarial suite.

## Voice Evaluation

Run:

python run_task5.py

## Regression

Compare the current result with the baseline.

A release candidate must not hide regressions.