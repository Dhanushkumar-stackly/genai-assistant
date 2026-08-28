from app.core.model_client import ModelClient


def main():

    client = ModelClient()

    prompt = "Explain AI."

    result = client.generate(prompt)

    print("TEXT:")
    print(result["text"])

    print("\nMODEL:")
    print(result["model"])

    print("\nLATENCY:")
    print(f'{result["latency_ms"]} ms')


if __name__ == "__main__":
    main()