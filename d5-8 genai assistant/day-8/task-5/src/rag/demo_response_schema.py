from src.rag.response_schema import AnswerResponse, Citation


response = AnswerResponse(
    answer="Python is a high-level programming language.",
    citations=[
        Citation(
            source="python_guide.pdf",
            chunk_id="chunk_001",
        )
    ],
    grounded=True,
)

print("=" * 60)
print("ANSWER RESPONSE")
print("=" * 60)

print("Answer:", response.answer)
print("Grounded:", response.grounded)

print("Citations:")

for citation in response.citations:
    print(
        f"- Source: {citation.source} | "
        f"Chunk: {citation.chunk_id}"
    )