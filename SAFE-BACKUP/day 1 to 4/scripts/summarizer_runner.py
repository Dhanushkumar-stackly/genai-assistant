from app.core.model_client import ModelClient
from app.core.summarizer import Summarizer


def main():

    text = """
    Artificial intelligence is a branch of computer science that focuses
    on creating systems capable of performing tasks that normally require
    human intelligence. These tasks include learning, reasoning,
    understanding language, recognizing patterns, and making decisions.

    Machine learning is a subset of artificial intelligence. It allows
    computers to learn from data and improve their performance without
    being explicitly programmed for every task.
    """.strip()

    if not text:
        raise ValueError("Input text is empty.")

    print("=" * 60)
    print("SUMMARIZER")
    print("=" * 60)

    print("\nInput text:")
    print(text)

    client = ModelClient()

    summarizer = Summarizer(client)

    summary = summarizer.summarize(text)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(summary)

    print("\n" + "=" * 60)
    print("Execution completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()