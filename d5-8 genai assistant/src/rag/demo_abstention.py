from src.rag.abstention import (
    should_abstain,
    get_abstention_message,
)


print("=" * 60)
print("ABSTENTION OUTPUT")
print("=" * 60)

chunks = []

if should_abstain(chunks):
    print("Abstain:", get_abstention_message())
else:
    print("Evidence available. Continue with generation.")