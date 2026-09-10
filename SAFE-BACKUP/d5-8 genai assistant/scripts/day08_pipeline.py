from src.rag.retrieve import retrieve
from src.rag.grounded_prompt import build_grounded_prompt
from src.rag.generate import generate_answer


def check_evidence(retrieved_chunks):
    """
    Check whether retrieval returned supporting evidence.
    """

    if not retrieved_chunks:
        return False

    valid_chunks = []

    for chunk in retrieved_chunks:
        text = chunk.get("text", "").strip()

        if text:
            valid_chunks.append(chunk)

    return len(valid_chunks) > 0


def validate_citations(answer, retrieved_chunks):
    """
    Validate that cited chunk IDs actually exist
    in retrieved evidence.
    """

    retrieved_ids = {
        chunk.get("chunk_id")
        for chunk in retrieved_chunks
    }

    valid_citations = []

    for chunk_id in retrieved_ids:
        if not chunk_id:
            continue

        if f"[{chunk_id}]" in answer:
            valid_citations.append(chunk_id)

    return valid_citations


def build_final_response(
    question,
    answer,
    retrieved_chunks,
    valid_citations
):
    """
    Build the final Day-08 response.
    """

    if not answer:
        answer = (
            "The answer cannot be determined "
            "from the provided evidence."
        )

    response = []

    response.append("Status:")
    response.append("answered")
    response.append("")

    response.append("Answer:")
    response.append(answer)
    response.append("")

    response.append("Sources:")

    for chunk in retrieved_chunks:
        chunk_id = chunk.get("chunk_id")

        if chunk_id in valid_citations:
            response.append(
                f"- {chunk_id}"
            )

    return "\n".join(response)


def main():

    question = input("Enter your question: ").strip()

    print("=" * 70)
    print("DAY 08 - GROUNDED RAG PIPELINE")
    print("=" * 70)

    print()
    print("Question:")
    print(question)

    # ---------------------------------------------------------
    # STEP 1
    # ---------------------------------------------------------

    print()
    print("Step 1: Retrieving from ChromaDB...")
    print()

    retrieved_chunks = retrieve(question)

    print()
    print("Retrieved chunks:")
    print("-" * 60)

    for index, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        print()
        print(f"Rank: {index}")

        print(
            f"Chunk ID: {chunk.get('chunk_id')}"
        )

        if "distance" in chunk:
            print(
                f"Distance: {chunk.get('distance')}"
            )

        if "metadata" in chunk:
            print(
                f"Metadata: {chunk.get('metadata')}"
            )

        print(
            f"Text: {chunk.get('text', '')}"
        )

    print("-" * 60)

    print(
        f"Retrieved chunks: {len(retrieved_chunks)}"
    )

    # ---------------------------------------------------------
    # STEP 2
    # ---------------------------------------------------------

    print()
    print("Step 2: Checking evidence...")

    evidence_sufficient = check_evidence(
        retrieved_chunks
    )

    if evidence_sufficient:
        print("Evidence status: SUFFICIENT")
    else:
        print("Evidence status: INSUFFICIENT")

        print()
        print("=" * 70)
        print("FINAL RESPONSE")
        print("=" * 70)

        print()
        print("Status:")
        print("abstained")

        print()
        print("Answer:")
        print(
            "The answer cannot be determined "
            "from the provided evidence."
        )

        return

    # ---------------------------------------------------------
    # STEP 3
    # ---------------------------------------------------------

    print()
    print("Step 3: Building grounded prompt...")

    grounded_prompt = build_grounded_prompt(
        question,
        retrieved_chunks
    )

    print("Grounded prompt created.")

    # ---------------------------------------------------------
    # STEP 4
    # ---------------------------------------------------------

    print()
    print("Step 4: Generating grounded answer...")

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    print("Grounded answer generated.")

    # ---------------------------------------------------------
    # STEP 5
    # ---------------------------------------------------------

    print()
    print("Step 5: Validating citations...")

    valid_citations = validate_citations(
        answer,
        retrieved_chunks
    )

    print(
        f"Valid citations: {len(valid_citations)}"
    )

    # ---------------------------------------------------------
    # STEP 6
    # ---------------------------------------------------------

    print()
    print("Step 6: Building final response...")

    final_response = build_final_response(
        question,
        answer,
        retrieved_chunks,
        valid_citations
    )

    print()
    print("=" * 70)
    print("FINAL RESPONSE")
    print("=" * 70)

    print()
    print(final_response)

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()