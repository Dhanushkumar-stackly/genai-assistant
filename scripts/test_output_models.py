from app.core.model_client import ModelClient
from app.core.summarizer import Summarizer
from app.core.extractor import Extractor
from app.core.classifier import Classifier


client = ModelClient()

summarizer = Summarizer(client)
extractor = Extractor(client)
classifier = Classifier(client)


print("\n--- SUMMARIZER ---")

summary = summarizer.summarize(
    "Artificial intelligence helps computers perform tasks "
    "that normally require human intelligence."
)

print(summary)


print("\n--- EXTRACTOR ---")

document = """
Invoice Number: INV-1001
Customer Name: Ravi Kumar
Customer Email: ravi@example.com
Invoice Date: 12-Aug-2026
Total Amount: 5000
"""

extracted = extractor.extract(document)

print(extracted)


print("\n--- CLASSIFIER ---")

classification = classifier.classify(document)

print(classification)