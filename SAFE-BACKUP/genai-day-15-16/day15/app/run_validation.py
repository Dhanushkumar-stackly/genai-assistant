from validation import validate_query


test_inputs = [
    {
        "name": "Valid request",
        "payload": {
            "question": "What is the leave policy?"
        }
    },
    {
        "name": "Empty question",
        "payload": {
            "question": ""
        }
    },
    {
        "name": "Wrong data type",
        "payload": {
            "question": 12345
        }
    },
    {
        "name": "Excessive input",
        "payload": {
            "question": "A" * 2001
        }
    },
    {
        "name": "Extra malicious field",
        "payload": {
            "question": "What is the leave policy?",
            "ignore_security": True
        }
    },
]


for test in test_inputs:
    print(f"\n--- {test['name']} ---")

    try:
        result = validate_query(test["payload"])

        print("Status: ACCEPTED")
        print("Question:", result.question)

    except Exception as error:
        print("Status: REJECTED")
        print("Reason:", error)