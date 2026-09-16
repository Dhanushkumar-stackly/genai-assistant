from src.rag.retrieve import retrieve
from src.rag.generate import generate_answer


def run_rag(question, top_k=5):

    print("=" * 60)
    print("RAG ASSISTANT")
    print("=" * 60)

    print(f"\nQuestion: {question}")

    # --------------------------------------------------------
    # STEP 1: RETRIEVAL
    # --------------------------------------------------------

    retrieved_chunks = retrieve(
        question,
        top_k=top_k
    )

    # --------------------------------------------------------
    # STEP 2: CHECK RETRIEVAL
    # --------------------------------------------------------

    if not retrieved_chunks:

        print(
            "\nNo relevant documents were retrieved."
        )

        return

    print(
        f"\nRetrieved {len(retrieved_chunks)} chunks."
    )

    # --------------------------------------------------------
    # STEP 3: GENERATION
    # --------------------------------------------------------

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    # --------------------------------------------------------
    # STEP 4: FINAL ANSWER
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(answer)


if __name__ == "__main__":

    question = (
        "What is reinforcement learning?"
    )

    run_rag(
        question,
        top_k=5
    )