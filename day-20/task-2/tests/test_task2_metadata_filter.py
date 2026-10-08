from task2_metadata_filter import filter_by_metadata


SAMPLE_RECORDS = [
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


def test_filter_by_source():
    results = filter_by_metadata(
        SAMPLE_RECORDS,
        {"source": "HR_POLICY"}
    )

    assert len(results) == 2
    assert results[0]["id"] == "DOC001"
    assert results[1]["id"] == "DOC003"


def test_non_matching_filter_returns_empty():
    results = filter_by_metadata(
        SAMPLE_RECORDS,
        {"source": "FINANCE_POLICY"}
    )

    assert results == []


def test_multiple_metadata_filters():
    results = filter_by_metadata(
        SAMPLE_RECORDS,
        {
            "source": "HR_POLICY",
            "department": "HR"
        }
    )

    assert len(results) == 2


def test_missing_metadata_does_not_match():
    records = [
        {
            "id": "DOC004",
            "content": "Unknown document"
        }
    ]

    results = filter_by_metadata(
        records,
        {"source": "HR_POLICY"}
    )

    assert results == []


def test_empty_filter_returns_all_records():
    results = filter_by_metadata(
        SAMPLE_RECORDS,
        {}
    )

    assert len(results) == 3