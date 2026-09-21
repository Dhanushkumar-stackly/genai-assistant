import asyncio
import argparse

from day17_app.rag_client import ExistingRAGClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a cleaned transcript to the existing RAG /ask service."
    )
    parser.add_argument(
        "--base-url",
        help=(
            "RAG service base URL. Defaults to RAG_API_URL or "
            "http://127.0.0.1:8000."
        ),
    )
    return parser.parse_args()


async def main():

    args = parse_args()
    client = ExistingRAGClient(base_url=args.base_url)

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
