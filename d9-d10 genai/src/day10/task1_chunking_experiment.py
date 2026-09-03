"""
DAY 10 - TASK 1
CHUNKING AND TOP-K EXPERIMENT

Controlled retrieval experiment.

Baseline:
    Embedding model : sentence-transformers/all-MiniLM-L6-v2
    Chunk size      : 1000
    Chunk overlap   : 200
    Top-k           : 5

Experiment:
    Chunk size      : 500
    Chunk overlap   : 100
    Top-k           : 5

Only the chunking configuration is changed.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

BASELINE_FILE = DATA_DIR / "baseline.json"

QUESTIONS_FILE = (
    PROJECT_ROOT.parent
    / "d5-6 genai assistant"
    / "data"
    / "retrieval_questions.json"
)

CHUNKS_FILE = (
    PROJECT_ROOT.parent
    / "d5-6 genai assistant"
    / "outputs"
    / "chunks.json"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

BASELINE_CHUNK_SIZE = 1000
BASELINE_OVERLAP = 200

EXPERIMENT_CHUNK_SIZE = 500
EXPERIMENT_OVERLAP = 100

TOP_K = 5


# ============================================================
# OUTPUT FILES
# ============================================================

EXPERIMENT_OUTPUT = (
    OUTPUT_DIR
    / "day10_task1_chunking_experiment.json"
)

BASELINE_RESULTS_OUTPUT = (
    OUTPUT_DIR
    / "day10_task1_baseline_results.json"
)

EXPERIMENT_RESULTS_OUTPUT = (
    OUTPUT_DIR
    / "day10_task1_experiment_results.json"
)


# ============================================================
# JSON HELPERS
# ============================================================

def load_json(
    path: Path,
    default: Any = None,
) -> Any:
    """Load JSON from disk."""

    if not path.exists():

        if default is not None:
            return default

        raise FileNotFoundError(
            f"JSON file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def save_json(
    path: Path,
    data: Any,
) -> None:
    """Save JSON to disk."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


# ============================================================
# DOCUMENT ID NORMALIZATION
# ============================================================

def get_document_id(
    document: dict,
) -> str:
    """
    Get document ID from either:

        document_id
        doc_id
    """

    if not isinstance(
        document,
        dict,
    ):
        raise TypeError(
            "Document must be a dictionary."
        )

    document_id = (
        document.get("document_id")
        or document.get("doc_id")
    )

    if document_id is None:
        raise ValueError(
            "Source document is missing "
            "doc_id/document_id."
        )

    document_id = str(
        document_id
    ).strip()

    if not document_id:
        raise ValueError(
            "Source document has an empty "
            "doc_id/document_id."
        )

    return document_id


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def get_document_text(
    document: dict,
) -> str:
    """
    Extract document text.

    Supports:
        text
        content
        document
    """

    text = (
        document.get("text")
        or document.get("content")
        or document.get("document")
        or ""
    )

    return str(text)


# ============================================================
# LOAD BASELINE
# ============================================================

def load_baseline() -> dict:
    """Load frozen baseline configuration."""

    baseline = load_json(
        BASELINE_FILE,
        default={},
    )

    if not isinstance(
        baseline,
        dict,
    ):
        raise ValueError(
            "baseline.json must contain an object."
        )

    return baseline


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_questions() -> list[dict]:
    """
    Load the 30 retrieval evaluation questions.
    """

    questions = load_json(
        QUESTIONS_FILE,
        default=[],
    )

    if not isinstance(
        questions,
        list,
    ):
        raise ValueError(
            "retrieval_questions.json must contain a list."
        )

    normalized = []

    for item in questions:

        if not isinstance(
            item,
            dict,
        ):
            continue

        question = str(
            item.get(
                "question",
                "",
            )
        ).strip()

        expected_doc_id = (
            item.get("expected_doc_id")
            or item.get("document_id")
            or item.get("doc_id")
        )

        if not question:
            continue

        if expected_doc_id is None:
            continue

        normalized.append(
            {
                "question": question,
                "expected_doc_id": str(
                    expected_doc_id
                ),
            }
        )

    return normalized


# ============================================================
# LOAD SOURCE DOCUMENTS
# ============================================================

def load_source_documents() -> list[dict]:
    """
    Load source documents from chunks.json.

    Existing chunks.json may look like:

        {
            "chunk_id": "...",
            "doc_id": "document_001",
            "title": "...",
            "text": "..."
        }

    This function converts the data into one record
    per document.
    """

    print()
    print(
        "Loading source documents from baseline index..."
    )

    raw_chunks = load_json(
        CHUNKS_FILE,
        default=[],
    )

    if not isinstance(
        raw_chunks,
        list,
    ):
        raise ValueError(
            "chunks.json must contain a list."
        )

    documents: dict[str, dict] = {}

    for chunk in raw_chunks:

        if not isinstance(
            chunk,
            dict,
        ):
            continue

        # ----------------------------------------------------
        # IMPORTANT FIX
        # ----------------------------------------------------

        document_id = get_document_id(
            chunk
        )

        text = get_document_text(
            chunk
        )

        title = str(
            chunk.get(
                "title",
                document_id,
            )
        )

        source_path = str(
            chunk.get(
                "source_path",
                "",
            )
        )

        if document_id not in documents:

            documents[document_id] = {
                "document_id": document_id,
                "doc_id": document_id,
                "title": title,
                "source_path": source_path,
                "text_parts": [],
            }

        if text.strip():

            documents[
                document_id
            ][
                "text_parts"
            ].append(
                text.strip()
            )

    source_documents = []

    for document in documents.values():

        source_documents.append(
            {
                "document_id": document[
                    "document_id"
                ],

                "doc_id": document[
                    "document_id"
                ],

                "title": document[
                    "title"
                ],

                "source_path": document[
                    "source_path"
                ],

                "text": "\n\n".join(
                    document[
                        "text_parts"
                    ]
                ),
            }
        )

    if not source_documents:

        raise ValueError(
            "No source documents were loaded."
        )

    print(
        f"Loaded {len(source_documents)} "
        f"source documents."
    )

    return source_documents


# ============================================================
# TEXT CHUNKING
# ============================================================

def split_text(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    """
    Character-based overlapping chunking.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative."
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size."
        )

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0
    length = len(text)

    while start < length:

        end = min(
            start + chunk_size,
            length,
        )

        chunk = text[
            start:end
        ].strip()

        if chunk:
            chunks.append(
                chunk
            )

        if end >= length:
            break

        start = end - overlap

    return chunks


# ============================================================
# BUILD EXPERIMENT CHUNKS
# ============================================================

def build_experiment_chunks(
    source_documents: list[dict],
    chunk_size: int,
    overlap: int,
) -> list[dict]:
    """
    Build chunks for an experiment.

    FIX:
        Supports both doc_id and document_id.
    """

    experiment_chunks = []

    for document in source_documents:

        # ----------------------------------------------------
        # IMPORTANT FIX
        # ----------------------------------------------------

        document_id = get_document_id(
            document
        )

        text = get_document_text(
            document
        )

        title = document.get(
            "title",
            document_id,
        )

        source_path = document.get(
            "source_path",
            "",
        )

        chunks = split_text(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for index, chunk_text in enumerate(
            chunks
        ):

            experiment_chunks.append(
                {
                    "chunk_id": (
                        f"{document_id}_"
                        f"chunk_{index:03d}"
                    ),

                    "document_id": document_id,

                    # Keep compatibility with
                    # existing project data.
                    "doc_id": document_id,

                    "title": title,

                    "source_path": source_path,

                    "chunk_index": index,

                    "chunk_size": chunk_size,

                    "overlap": overlap,

                    "text": chunk_text,
                }
            )

    return experiment_chunks


# ============================================================
# TOKENIZATION
# ============================================================

def tokenize(
    text: str,
) -> set[str]:
    """
    Basic tokenization.
    """

    tokens = re.findall(
        r"[a-zA-Z0-9]+",
        str(text).lower(),
    )

    return {
        token
        for token in tokens
        if len(token) > 1
    }


# ============================================================
# SIMILARITY
# ============================================================

def similarity(
    query: str,
    text: str,
) -> float:
    """
    Calculate simple lexical similarity.
    """

    query_tokens = tokenize(
        query
    )

    text_tokens = tokenize(
        text
    )

    if not query_tokens:
        return 0.0

    if not text_tokens:
        return 0.0

    common = (
        query_tokens
        & text_tokens
    )

    return (
        len(common)
        / len(query_tokens)
    )


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(
    question: str,
    chunks: list[dict],
    top_k: int = TOP_K,
) -> list[dict]:
    """
    Retrieve top-k chunks.
    """

    scored = []

    for chunk in chunks:

        score = similarity(
            question,
            chunk.get(
                "text",
                "",
            ),
        )

        scored.append(
            {
                "chunk": chunk,
                "score": score,
            }
        )

    scored.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored[
        :max(1, top_k)
    ]


# ============================================================
# EVALUATE RETRIEVAL
# ============================================================

def evaluate_retrieval(
    questions: list[dict],
    chunks: list[dict],
    top_k: int = TOP_K,
) -> dict:
    """
    Evaluate retrieval.

    Metrics:
        retrieval_recall
        top1_accuracy
        mrr
        average_latency_ms

    Always returns 'details'.
    """

    total_questions = len(
        questions
    )

    if total_questions == 0:

        return {
            "total_questions": 0,
            "retrieval_recall": 0.0,
            "top1_accuracy": 0.0,
            "mrr": 0.0,
            "average_latency_ms": 0.0,
            "details": [],
        }

    recovered = 0
    top1_correct = 0
    reciprocal_rank_sum = 0.0
    total_latency = 0.0

    details = []

    for question_data in questions:

        question = str(
            question_data.get(
                "question",
                "",
            )
        )

        expected_doc_id = str(
            question_data.get(
                "expected_doc_id",
                "",
            )
        )

        start = time.perf_counter()

        retrieved = retrieve(
            question=question,
            chunks=chunks,
            top_k=top_k,
        )

        elapsed_ms = (
            time.perf_counter()
            - start
        ) * 1000

        total_latency += elapsed_ms

        retrieved_doc_ids = []

        retrieved_scores = []

        for result in retrieved:

            chunk = result[
                "chunk"
            ]

            document_id = get_document_id(
                chunk
            )

            score = float(
                result.get(
                    "score",
                    0.0,
                )
            )

            if document_id not in retrieved_doc_ids:

                retrieved_doc_ids.append(
                    document_id
                )

                retrieved_scores.append(
                    round(
                        score,
                        4,
                    )
                )

        expected_rank = None

        if expected_doc_id in retrieved_doc_ids:

            expected_rank = (
                retrieved_doc_ids.index(
                    expected_doc_id
                )
                + 1
            )

            recovered += 1

            reciprocal_rank_sum += (
                1.0
                / expected_rank
            )

            if expected_rank == 1:
                top1_correct += 1

        details.append(
            {
                "question": question,
                "expected_doc_id": expected_doc_id,
                "expected_rank": expected_rank,
                "retrieved_doc_ids": retrieved_doc_ids,
                "retrieved_scores": retrieved_scores,
                "recovered": (
                    expected_rank
                    is not None
                ),
                "latency_ms": round(
                    elapsed_ms,
                    2,
                ),
            }
        )

    return {
        "total_questions": total_questions,

        "retrieval_recall": round(
            recovered
            / total_questions,
            4,
        ),

        "top1_accuracy": round(
            top1_correct
            / total_questions,
            4,
        ),

        "mrr": round(
            reciprocal_rank_sum
            / total_questions,
            4,
        ),

        "average_latency_ms": round(
            total_latency
            / total_questions,
            2,
        ),

        "details": details,
    }


# ============================================================
# METRIC SUMMARY
# ============================================================

def metric_summary(
    metrics: dict,
) -> dict:
    """
    Return only summary metrics.
    """

    return {
        "total_questions": metrics.get(
            "total_questions",
            0,
        ),

        "retrieval_recall": metrics.get(
            "retrieval_recall",
            0.0,
        ),

        "top1_accuracy": metrics.get(
            "top1_accuracy",
            0.0,
        ),

        "mrr": metrics.get(
            "mrr",
            0.0,
        ),

        "average_latency_ms": metrics.get(
            "average_latency_ms",
            0.0,
        ),
    }


# ============================================================
# CREATE FINAL REPORT
# ============================================================

def create_report(
    baseline_metrics: dict,
    experiment_metrics: dict,
) -> dict:
    """
    Create complete experiment report.

    FIX:
        Uses .get("details", []) so a missing details
        field cannot produce KeyError.
    """

    baseline_recall = float(
        baseline_metrics.get(
            "retrieval_recall",
            0.0,
        )
    )

    experiment_recall = float(
        experiment_metrics.get(
            "retrieval_recall",
            0.0,
        )
    )

    baseline_top1 = float(
        baseline_metrics.get(
            "top1_accuracy",
            0.0,
        )
    )

    experiment_top1 = float(
        experiment_metrics.get(
            "top1_accuracy",
            0.0,
        )
    )

    baseline_mrr = float(
        baseline_metrics.get(
            "mrr",
            0.0,
        )
    )

    experiment_mrr = float(
        experiment_metrics.get(
            "mrr",
            0.0,
        )
    )

    baseline_latency = float(
        baseline_metrics.get(
            "average_latency_ms",
            0.0,
        )
    )

    experiment_latency = float(
        experiment_metrics.get(
            "average_latency_ms",
            0.0,
        )
    )

    # --------------------------------------------------------
    # ALWAYS GET DETAILS SAFELY
    # --------------------------------------------------------

    baseline_details = baseline_metrics.get(
        "details",
        [],
    )

    experiment_details = experiment_metrics.get(
        "details",
        [],
    )

    if not isinstance(
        baseline_details,
        list,
    ):
        baseline_details = []

    if not isinstance(
        experiment_details,
        list,
    ):
        experiment_details = []

    # --------------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------------

    recall_change = (
        experiment_recall
        - baseline_recall
    )

    if recall_change > 0:
        interpretation = (
            "The smaller chunk configuration "
            "improved retrieval recall."
        )

    elif recall_change < 0:
        interpretation = (
            "The smaller chunk configuration "
            "reduced retrieval recall."
        )

    else:
        interpretation = (
            "Changing the chunk configuration "
            "produced no recall improvement."
        )

    # --------------------------------------------------------
    # CONCLUSION
    # --------------------------------------------------------

    if recall_change > 0:

        conclusion = (
            "The controlled experiment changed "
            "the chunking configuration while "
            "keeping top_k fixed. Retrieval recall "
            "improved, indicating that the candidate "
            "chunking configuration may be beneficial."
        )

    elif recall_change < 0:

        conclusion = (
            "The controlled experiment changed "
            "the chunking configuration while "
            "keeping top_k fixed. Retrieval recall "
            "decreased, so the candidate chunking "
            "configuration is not preferred."
        )

    else:

        conclusion = (
            "The controlled experiment changed "
            "the chunking configuration while "
            "keeping top_k fixed. There was no "
            "improvement in retrieval recall, "
            "Top-1 accuracy, or MRR."
        )

    return {
        "experiment": {
            "id": "DAY10-TASK1",
            "name": (
                "Controlled Chunking Experiment"
            ),

            "variable": "chunk_size",

            "baseline_value":
                BASELINE_CHUNK_SIZE,

            "experiment_value":
                EXPERIMENT_CHUNK_SIZE,

            "baseline_overlap":
                BASELINE_OVERLAP,

            "experiment_overlap":
                EXPERIMENT_OVERLAP,

            "top_k": TOP_K,

            "hypothesis": (
                "Changing chunk size may improve "
                "retrieval quality for weak questions."
            ),
        },

        "baseline_metrics": metric_summary(
            baseline_metrics
        ),

        "experiment_metrics": metric_summary(
            experiment_metrics
        ),

        "metric_changes": {
            "retrieval_recall": round(
                experiment_recall
                - baseline_recall,
                4,
            ),

            "top1_accuracy": round(
                experiment_top1
                - baseline_top1,
                4,
            ),

            "mrr": round(
                experiment_mrr
                - baseline_mrr,
                4,
            ),

            "average_latency_ms": round(
                experiment_latency
                - baseline_latency,
                2,
            ),
        },

        "interpretation": interpretation,

        "conclusion": conclusion,

        "baseline_results": baseline_details,

        "experiment_results": experiment_details,
    }


# ============================================================
# PRINT METRICS
# ============================================================

def print_metrics(
    title: str,
    metrics: dict,
) -> None:

    print()
    print(title)
    print("-" * 70)

    print(
        json.dumps(
            metric_summary(metrics),
            indent=2,
        )
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("=" * 70)
    print(
        "DAY 10 - TASK 1"
    )
    print(
        "CHUNKING AND TOP-K EXPERIMENT"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # LOAD BASELINE
    # --------------------------------------------------------

    baseline = load_baseline()

    print()
    print("FROZEN BASELINE")
    print("-" * 70)

    print(
        "Embedding Model :",
        baseline.get(
            "embedding_model",
            "sentence-transformers/all-MiniLM-L6-v2",
        ),
    )

    chunking = baseline.get(
        "chunking",
        {},
    )

    retrieval = baseline.get(
        "retrieval",
        {},
    )

    actual_baseline_chunk_size = chunking.get(
        "chunk_size",
        BASELINE_CHUNK_SIZE,
    )

    actual_baseline_overlap = chunking.get(
        "chunk_overlap",
        chunking.get(
            "overlap",
            BASELINE_OVERLAP,
        ),
    )

    actual_top_k = retrieval.get(
        "top_k",
        TOP_K,
    )

    print(
        "Chunk Size      :",
        actual_baseline_chunk_size,
    )

    print(
        "Overlap         :",
        actual_baseline_overlap,
    )

    print(
        "Top K           :",
        actual_top_k,
    )

    # --------------------------------------------------------
    # LOAD QUESTIONS
    # --------------------------------------------------------

    questions = load_questions()

    print()
    print(
        f"Questions loaded: {len(questions)}"
    )

    # --------------------------------------------------------
    # LOAD SOURCE DOCUMENTS
    # --------------------------------------------------------

    source_documents = (
        load_source_documents()
    )

    # --------------------------------------------------------
    # BUILD BASELINE CHUNKS
    # --------------------------------------------------------

    print()
    print(
        "Building baseline chunks..."
    )

    baseline_chunks = (
        build_experiment_chunks(
            source_documents=source_documents,
            chunk_size=actual_baseline_chunk_size,
            overlap=actual_baseline_overlap,
        )
    )

    print(
        f"Baseline chunks: "
        f"{len(baseline_chunks)}"
    )

    # --------------------------------------------------------
    # BUILD EXPERIMENT CHUNKS
    # --------------------------------------------------------

    print()
    print(
        "Building experiment chunks..."
    )

    experiment_chunks = (
        build_experiment_chunks(
            source_documents=source_documents,
            chunk_size=EXPERIMENT_CHUNK_SIZE,
            overlap=EXPERIMENT_OVERLAP,
        )
    )

    print(
        f"Experiment chunks: "
        f"{len(experiment_chunks)}"
    )

    # --------------------------------------------------------
    # BASELINE EVALUATION
    # --------------------------------------------------------

    print()
    print(
        "Running baseline retrieval..."
    )

    baseline_metrics = (
        evaluate_retrieval(
            questions=questions,
            chunks=baseline_chunks,
            top_k=actual_top_k,
        )
    )

    print_metrics(
        "BASELINE METRICS",
        baseline_metrics,
    )

    # --------------------------------------------------------
    # SAVE BASELINE RESULTS
    # --------------------------------------------------------

    save_json(
        BASELINE_RESULTS_OUTPUT,
        baseline_metrics,
    )

    # --------------------------------------------------------
    # EXPERIMENT EVALUATION
    # --------------------------------------------------------

    print()
    print(
        "Running chunking experiment..."
    )

    experiment_metrics = (
        evaluate_retrieval(
            questions=questions,
            chunks=experiment_chunks,
            top_k=actual_top_k,
        )
    )

    print_metrics(
        "EXPERIMENT METRICS",
        experiment_metrics,
    )

    # --------------------------------------------------------
    # SAVE EXPERIMENT RESULTS
    # --------------------------------------------------------

    save_json(
        EXPERIMENT_RESULTS_OUTPUT,
        experiment_metrics,
    )

    # --------------------------------------------------------
    # CREATE REPORT
    # --------------------------------------------------------

    report = create_report(
        baseline_metrics=baseline_metrics,
        experiment_metrics=experiment_metrics,
    )

    # --------------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------------

    save_json(
        EXPERIMENT_OUTPUT,
        report,
    )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "DAY 10 - TASK 1 COMPLETE"
    )
    print("=" * 70)

    print()
    print(
        "EXPERIMENT"
    )
    print("-" * 70)

    print(
        "Variable Changed   : chunk_size"
    )

    print(
        f"Baseline           : "
        f"{actual_baseline_chunk_size}"
    )

    print(
        f"Experiment         : "
        f"{EXPERIMENT_CHUNK_SIZE}"
    )

    print(
        f"Baseline Overlap   : "
        f"{actual_baseline_overlap}"
    )

    print(
        f"Experiment Overlap : "
        f"{EXPERIMENT_OVERLAP}"
    )

    print(
        f"Top K              : "
        f"{actual_top_k}"
    )

    print()
    print(
        "METRIC CHANGES"
    )
    print("-" * 70)

    print(
        f"Recall Change      : "
        f"{report['metric_changes']['retrieval_recall']:+.4f}"
    )

    print(
        f"Top-1 Change       : "
        f"{report['metric_changes']['top1_accuracy']:+.4f}"
    )

    print(
        f"MRR Change         : "
        f"{report['metric_changes']['mrr']:+.4f}"
    )

    print(
        f"Latency Change     : "
        f"{report['metric_changes']['average_latency_ms']:+.2f} ms"
    )

    print()
    print(
        "INTERPRETATION"
    )
    print("-" * 70)

    print(
        report["interpretation"]
    )

    print()
    print(
        "CONCLUSION"
    )
    print("-" * 70)

    print(
        report["conclusion"]
    )

    print()
    print(
        "Output files:"
    )

    print(
        f"1. {BASELINE_RESULTS_OUTPUT}"
    )

    print(
        f"2. {EXPERIMENT_RESULTS_OUTPUT}"
    )

    print(
        f"3. {EXPERIMENT_OUTPUT}"
    )

    print()
    print("=" * 70)
    print(
        "TASK 1 EXPERIMENT COMPLETED SUCCESSFULLY"
    )
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()