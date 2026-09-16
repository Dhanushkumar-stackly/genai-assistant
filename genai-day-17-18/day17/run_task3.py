import asyncio

from app.rag_client import ExistingRAGClient


async def main():

    client = ExistingRAGClient(
        base_url="http://127.0.0.1:8000"
    )

    result = await client.ask(
        "  What   is   the   leave   policy?  "
    )

    print("CLEANED QUESTION:")
    print(
        "What is the leave policy?"
    )

    print("\nANSWER:")
    print(result.answer)

    print("\nSOURCES:")
    print(result.sources)

    print("\nRAG LATENCY:")
    print(
        f"{result.rag_latency_ms} ms"
    )


if __name__ == "__main__":
    asyncio.run(main())