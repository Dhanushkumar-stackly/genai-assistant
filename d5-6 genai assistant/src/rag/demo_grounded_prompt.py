from src.rag.grounded_prompt import build_grounded_prompt


chunks = [
    {
        "chunk_id": "chunk_001",
        "source": "python_guide.pdf",
        "text": "Python is a high-level programming language.",
    }
]

question = "What is Python?"

prompt = build_grounded_prompt(question, chunks)

print("=" * 60)
print("GROUNDED PROMPT OUTPUT")
print("=" * 60)
print(prompt)