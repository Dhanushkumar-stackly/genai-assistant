from src.rag.retrieve import retrieve
from src.rag.generate import generate_context


def main():

    question = (
        "What is reinforcement learning?"
    )

    print("=" * 70)
    print("DAY 07 - RAG PIPELINE TEST")
    print("=" * 70)

    print("\nStep 1: Retrieving relevant chunks...")

    results = retrieve(
        question,
        top_k=5
    )

    print(
        f"\nRetrieved: {len(results)} chunks"
    )

    print("\nStep 2: Building generation context...")

    prompt = generate_context(
        question,
        results,
        max_chunks=5
    )

    print("\nStep 3: Final LLM-ready input")
    print("=" * 70)

    print(prompt)

    print("=" * 70)
    print("RAG PIPELINE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()