from app.core.model_client import ModelClient
from app.core.summarizer import Summarizer


def main():
    model_client = ModelClient()

    summarizer = Summarizer(model_client)

    text = """
    Artificial Intelligence is a field of computer science
    that focuses on building systems capable of performing
    tasks that normally require human intelligence.
    These tasks include learning, reasoning, problem solving,
    understanding language, and recognizing patterns.
    """

    summary = summarizer.summarize(text)

    print("SUMMARY:")
    print(summary)


if __name__ == "__main__":
    main()