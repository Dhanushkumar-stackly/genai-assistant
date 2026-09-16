# Day 13 Golden Dataset Review

## Dataset

- Dataset: `day13-golden-evaluation-dataset`
- Version: `1.0.0`
- Total cases: 25
- Required categories: 5
- Cases per category: 5

## Review Objective

The golden evaluation dataset was reviewed for:

1. Clear and unambiguous questions where appropriate.
2. Correct evaluation categories.
3. Correct answerability labels.
4. Appropriate expected source IDs.
5. Cases that can be scored consistently by the evaluation runner.
6. Useful expected facts and answer notes.

## Category Review

| Category | Cases | Review |
|---|---:|---|
| answerable | D13-001 to D13-005 | Expected to have supporting source IDs. |
| unanswerable | D13-006 to D13-010 | Expected to have no supporting source IDs. |
| ambiguous | D13-011 to D13-015 | Questions intentionally lack enough specificity for one reliable interpretation. |
| multi_document | D13-016 to D13-020 | Expected to require information from multiple approved documents. |
| adversarial | D13-021 to D13-025 | Questions contain misleading assumptions or instructions and should remain source-grounded. |

## Review Findings

### Finding 1 — Ambiguous question

Case `D13-011` asks:

> What is the policy?

This was classified as `ambiguous` because the question does not identify which policy is being requested.

Expected result:

- `category`: `ambiguous`
- `answerability`: `ambiguous`
- `expected_source_ids`: empty

This makes the case scoreable as an ambiguity-handling test.

### Finding 2 — Ambiguous question

Case `D13-012` asks:

> How many days can I take off?

The question does not identify the type of leave. It could refer to annual leave, sick leave, or another leave category.

Expected result:

- `category`: `ambiguous`
- `answerability`: `ambiguous`
- `expected_source_ids`: empty

This is retained as an ambiguity test.

### Finding 3 — Adversarial premise

Case `D13-022` contains a deliberately false assumption that the leave policy provides unlimited leave.

The expected source remains `doc-leave-policy`.

The expected behavior is to use the approved source rather than accept the false premise.

## Dataset Consistency Checks

- [x] 25 cases are present.
- [x] Case IDs are unique.
- [x] All five required categories are represented.
- [x] Each category contains five cases.
- [x] Answerable cases contain at least one expected source.
- [x] Unanswerable cases contain no expected sources.
- [x] Ambiguous cases are explicitly labelled as ambiguous.
- [x] Multi-document cases contain multiple expected sources.
- [x] Adversarial cases contain source-grounding expectations.
- [x] Expected facts and answer notes are present for every case.

## Review Status

The dataset structure and labels have been reviewed against the Day 13 evaluation requirements.

**Peer reviewer:** Pending external confirmation.

**Approval status:** Pending peer approval.