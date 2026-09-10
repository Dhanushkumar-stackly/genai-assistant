import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "eval" / "evaluation_case.schema.json"


def load_schema():
    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_evaluation_case_schema_exists():
    assert SCHEMA_PATH.exists()


def test_required_evaluation_fields_are_defined():
    schema = load_schema()

    required_fields = {
        "case_id",
        "question",
        "category",
        "expected_source_ids",
        "answerability",
    }

    assert required_fields.issubset(set(schema["required"]))


def test_evaluation_case_schema_defines_optional_fields():
    schema = load_schema()

    properties = schema["properties"]

    assert "expected_facts" in properties
    assert "answer_notes" in properties


def test_evaluation_categories_are_defined():
    schema = load_schema()

    categories = schema["properties"]["category"]["enum"]

    assert "answerable" in categories
    assert "unanswerable" in categories
    assert "ambiguous" in categories
    assert "multi_document" in categories
    assert "adversarial" in categories


def test_answerability_values_are_defined():
    schema = load_schema()

    answerability_values = (
        schema["properties"]["answerability"]["enum"]
    )

    assert "answerable" in answerability_values
    assert "unanswerable" in answerability_values
    assert "ambiguous" in answerability_values


def test_case_id_format_is_defined():
    schema = load_schema()

    case_id_schema = schema["properties"]["case_id"]

    assert case_id_schema["type"] == "string"
    assert case_id_schema["pattern"] == "^D13-[0-9]{3}$"


def test_additional_properties_are_disabled():
    schema = load_schema()

    assert schema["additionalProperties"] is False