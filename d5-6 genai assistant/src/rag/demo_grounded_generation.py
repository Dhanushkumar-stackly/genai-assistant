from src.rag.grounded_generation import (
    generate_grounded_response,
)


chunks = [
    {
        "source": "python_guide.pdf",
        "chunk_id": "chunk_001",
        "text": "Python is a high-level programming language.",
    },
    {
        "source": "python_guide.pdf",
        "chunk_id": "chunk_002",
        "text": "Python supports object-oriented programming.",
    },
]


response = generate_grounded_response(
    "What is Python?",
    chunks,
)


print("=" * 60)
print("GROUNDED GENERATION OUTPUT")
print("=" * 60)

print("Answer:")
print(response.answer)

print()
print("Grounded:")
print(response.grounded)

print()
print("Citations:")

for citation in response.citations:
    print(
        f"- Source: {citation.source} | "
        f"Chunk: {citation.chunk_id}"
    )