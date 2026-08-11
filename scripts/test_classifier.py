from app.core.model_client import ModelClient
from app.core.classifier import Classifier


client = ModelClient()
classifier = Classifier(client)

text = """
Invoice Number: INV-1001
Customer Name: Ravi Kumar
Invoice Date: 11-Aug-2026
Total Amount: 5000
"""

result = classifier.classify(text)

print("Classification Result:")
print(result)