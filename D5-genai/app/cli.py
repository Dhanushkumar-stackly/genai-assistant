from __future__ import annotations

import argparse

from app.embeddings import EmbeddingModel
from app.search import SemanticSearcher
from app.vector_store.vector_store import VectorStore


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="Day 06 Semantic Search CLI"
    )

    parser.add_argument(
        "query",
        help="Search question",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of results to return",
    )

    parser.add_argument(
        "--min-score",
        type=float,
        default=None,
        help="Optional minimum similarity score",
    )

    parser.add_argument(
        "--source",
        default=None,
        help="Optional source metadata filter",
    )

    return parser


def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    # -----------------------------------------------------
    # VECTOR STORE
    # -----------------------------------------------------

    vector_store = VectorStore(
        persist_directory="vector_db",
        collection_name="d5_chunks",
    )

    # -----------------------------------------------------
    # EMBEDDING MODEL
    # -----------------------------------------------------

    embedding_model = EmbeddingModel()

    # -----------------------------------------------------
    # SEARCHER
    # -----------------------------------------------------

    searcher = SemanticSearcher(
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    metadata_filter = None

    if args.source:

        metadata_filter = {
            "source": args.source
        }

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    results = searcher.search(
        query=args.query,
        top_k=args.top_k,
        metadata_filter=metadata_filter,
        min_score=args.min_score,
    )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    print()

    print("=" * 70)

    print(
        "SEMANTIC SEARCH RESULTS"
    )

    print("=" * 70)

    print(
        f"Query: {args.query}"
    )

    print()

    if not results:

        print(
            "No matching results found."
        )

        return

    for position, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"RESULT {position}"
        )

        print(
            "-" * 70
        )

        print(
            f"Score: "
            f"{result.get('score', 0):.4f}"
        )

        print(
            f"Chunk ID: "
            f"{result.get('chunk_id', 'N/A')}"
        )

        print(
            f"Document ID: "
            f"{result.get('document_id', 'N/A')}"
        )

        print(
            f"Source: "
            f"{result.get('source', 'N/A')}"
        )

        text = (
            result.get("text")
            or result.get("chunk_text")
            or result.get("content")
            or ""
        )

        print(
            f"Text: {text[:500]}"
        )

        print()


if __name__ == "__main__":
    main()