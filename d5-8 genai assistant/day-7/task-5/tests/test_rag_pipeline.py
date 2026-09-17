import sys
from pathlib import Path

# Always resolve imports against this Day-7 Task-5 project root.
# This prevents another task's top-level `src` package from being reused
# when pytest is executed recursively from the d5-8 parent directory.
TASK_ROOT = Path(__file__).resolve().parents[1]
if str(TASK_ROOT) not in sys.path:
    sys.path.insert(0, str(TASK_ROOT))

# Multiple Day-5/6/7/8 tasks contain a package named `src`.
# Remove a previously imported one so this test loads Day-7 Task-5's `src`.
for module_name in list(sys.modules):
    if module_name == "src" or module_name.startswith("src."):
        del sys.modules[module_name]

from src.rag.retrieve import retrieve
from src.rag.generate import generate_context


def test_ingest_then_retrieve_known_question():
    """Roadmap check: a known question returns retrievable evidence."""
    results = retrieve("What is reinforcement learning?", top_k=5)

    assert isinstance(results, list)
    assert len(results) > 0
    assert all("chunk_id" in item for item in results)
    assert all("text" in item for item in results)
    assert all("metadata" in item for item in results)


def test_retrieved_context_contains_source_labels():
    """Roadmap check: retrieved context uses stable source labels."""
    results = retrieve("What is reinforcement learning?", top_k=5)
    context = generate_context("What is reinforcement learning?", results)

    assert isinstance(context, str)
    assert context
    assert "EVIDENCE:" in context
    assert any(f"[{item['chunk_id']}]" in context for item in results)


def test_retrieval_respects_top_k():
    """Roadmap check: configured top-k limits the selected evidence."""
    results = retrieve("What is reinforcement learning?", top_k=3)

    assert len(results) <= 3
