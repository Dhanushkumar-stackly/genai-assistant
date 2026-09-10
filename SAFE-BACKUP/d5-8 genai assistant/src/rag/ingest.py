from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

EVENT_LOG = OUTPUTS_DIR / "ingestion_events.jsonl"

PREPROCESS_SCRIPT = PROJECT_ROOT / "scripts" / "preprocess_documents.py"
EMBEDDING_SCRIPT = PROJECT_ROOT / "scripts" / "generate_embeddings.py"
INDEX_SCRIPT = PROJECT_ROOT / "scripts" / "build_vector_index.py"


def log_event(
    stage,
    status,
    message,
    document=None
):
    """Record one ingestion event."""

    OUTPUTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    event = {
        "timestamp": datetime.now().isoformat(),
        "stage": stage,
        "status": status,
        "message": message
    }

    if document is not None:
        event["document"] = document

    with open(
        EVENT_LOG,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(event) + "\n"
        )


def get_documents():
    """Return approved markdown documents."""

    documents = sorted(
        DOCUMENTS_DIR.glob("*.md")
    )

    return documents


def validate_documents():
    """Validate that approved documents exist."""

    documents = get_documents()

    if not documents:

        log_event(
            stage="validation",
            status="failed",
            message="No markdown documents found."
        )

        raise FileNotFoundError(
            f"No documents found in {DOCUMENTS_DIR}"
        )

    print(
        f"Approved documents found: "
        f"{len(documents)}"
    )

    log_event(
        stage="validation",
        status="success",
        message=f"Found {len(documents)} approved documents."
    )

    return documents


def run_stage(
    stage_name,
    script_path
):
    """Run one ingestion stage."""

    print()
    print("=" * 60)
    print(f"STAGE: {stage_name}")
    print("=" * 60)

    if not script_path.exists():

        log_event(
            stage=stage_name,
            status="failed",
            message=f"Script not found: {script_path}"
        )

        raise FileNotFoundError(
            f"Missing script: {script_path}"
        )

    result = subprocess.run(
        [
            sys.executable,
            str(script_path)
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:

        log_event(
            stage=stage_name,
            status="failed",
            message=(
                f"{stage_name} failed "
                f"with exit code "
                f"{result.returncode}"
            )
        )

        raise RuntimeError(
            f"{stage_name} failed."
        )

    log_event(
        stage=stage_name,
        status="success",
        message=f"{stage_name} completed successfully."
    )

    return True


def ingest_documents():
    """
    Run the complete Day-07 ingestion pipeline.

    Documents
        ↓
    preprocessing
        ↓
    embeddings
        ↓
    vector index
    """

    print()
    print("=" * 70)
    print("DAY 07 - RAG INGESTION PIPELINE")
    print("=" * 70)

    log_event(
        stage="pipeline",
        status="started",
        message="Ingestion pipeline started."
    )

    try:

        documents = validate_documents()

        for document in documents:

            log_event(
                stage="document",
                status="accepted",
                message="Document accepted for ingestion.",
                document=document.name
            )

        # Stage 1:
        # Load + clean + chunk + metadata
        run_stage(
            "preprocessing",
            PREPROCESS_SCRIPT
        )

        # Stage 2:
        # Generate embeddings
        run_stage(
            "embedding",
            EMBEDDING_SCRIPT
        )

        # Stage 3:
        # Store vectors in ChromaDB
        run_stage(
            "vector_index",
            INDEX_SCRIPT
        )

        log_event(
            stage="pipeline",
            status="success",
            message=(
                "Complete ingestion pipeline "
                "finished successfully."
            )
        )

        print()
        print("=" * 70)
        print("INGESTION COMPLETED SUCCESSFULLY")
        print("=" * 70)

        return True

    except Exception as error:

        log_event(
            stage="pipeline",
            status="failed",
            message=str(error)
        )

        print()
        print("=" * 70)
        print("INGESTION FAILED")
        print("=" * 70)

        print(f"Error: {error}")

        return False


if __name__ == "__main__":

    success = ingest_documents()

    if not success:
        sys.exit(1)