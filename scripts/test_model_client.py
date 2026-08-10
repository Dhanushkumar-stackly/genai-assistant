from app.core.model_client import ModelClient


client = ModelClient()

result = client.generate(
    "Explain artificial intelligence in one simple sentence."
)

print("Response:")
print(result["text"])

print("\nModel:")
print(result["model"])

print("\nLatency:")
print(f'{result["latency_seconds"]} seconds')