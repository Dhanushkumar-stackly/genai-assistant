import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "task-1"))
from model_client import ModelClient
from summarizer import Summarizer

def main():
    text = """Artificial intelligence is a branch of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence. Machine learning is a subset of artificial intelligence that allows computers to learn from data."""
    result = Summarizer(ModelClient()).summarize(text)
    print("SUMMARY PROMPT")
    print(result.text)
    print(f"MODEL: {result.model}")
    print(f"LATENCY_MS: {result.latency_ms}")

if __name__ == "__main__": main()
