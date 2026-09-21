# Day 19 Failure Analysis

## Baseline

The 25-case evaluation contained:

- Total cases: 25
- Passed: 10
- Failed: 15

## Failure Pattern

The failed answerable cases expected document source IDs,
but the evaluation responder returned empty source lists.

## Failure Category 1

Retrieval/source propagation.

### Evidence

Expected source IDs were populated while actual source IDs were empty.

## Failure Category 2

Grounded answer/citation verification.

The answer grader could not verify expected source evidence when
the response contained no source IDs.

## Controlled Changes

1. Connect the evaluation path to the actual RAG responder.
2. Preserve retrieved document IDs in the final response.
3. Keep existing answer/citation grading rules unchanged.

## Regression Tests

Run:

pytest -v

## Before

Record actual result.

## After

Record actual result.

## Conclusion

The fix is accepted only if the target failure category improves
without introducing regression into existing tests.