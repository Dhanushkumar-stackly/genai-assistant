from app.core.extractor import Extractor
from app.core.model_client import ModelClient


def main():
    model_client = ModelClient()

    extractor = Extractor(model_client)

    document = """
    Invoice Number: INV-1001
    Customer Name: Ravi Kumar
    Customer Email: ravi@example.com
    Invoice Date: 10-Aug-2026
    Total Amount: ₹5,500
    """

    result = extractor.extract(document)

    print("EXTRACTED DATA:")
    print(result)


if __name__ == "__main__":
    main()