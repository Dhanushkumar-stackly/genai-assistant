"""
Day 20 - Task 2
Independent Change Request: Metadata Filtering

This module provides an isolated metadata filtering feature.
It does not modify the existing GenAI Assistant application.
"""


def filter_by_metadata(records, filters):
    """
    Filter records using metadata values.

    Parameters
    ----------
    records : list
        List of records containing metadata.

    filters : dict
        Metadata key/value pairs that must match.

    Returns
    -------
    list
        Records matching all supplied metadata filters.
    """

    filtered_records = []

    for record in records:
        metadata = record.get("metadata", {})

        matches = True

        for key, expected_value in filters.items():
            actual_value = metadata.get(key)

            if actual_value != expected_value:
                matches = False
                break

        if matches:
            filtered_records.append(record)

    return filtered_records


if __name__ == "__main__":

    sample_records = [
        {
            "id": "DOC001",
            "content": "Annual leave policy",
            "metadata": {
                "source": "HR_POLICY",
                "department": "HR"
            }
        },
        {
            "id": "DOC002",
            "content": "Employee onboarding process",
            "metadata": {
                "source": "ONBOARDING",
                "department": "HR"
            }
        },
        {
            "id": "DOC003",
            "content": "Work from home policy",
            "metadata": {
                "source": "HR_POLICY",
                "department": "HR"
            }
        }
    ]

    filters = {
        "source": "HR_POLICY"
    }

    results = filter_by_metadata(
        sample_records,
        filters
    )

    print("DAY 20 - TASK 2")
    print("Independent Change Request")
    print("Feature: Metadata Filtering")
    print("-----------------------------------")

    print(f"Total records : {len(sample_records)}")
    print(f"Filter        : {filters}")
    print(f"Matched       : {len(results)}")

    print("\nMatching Records:")

    for record in results:
        print(
            f"{record['id']} -> "
            f"{record['metadata']['source']}"
        )