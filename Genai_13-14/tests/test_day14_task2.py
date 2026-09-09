from eval.graders.answer_grader import (
    check_answerability,
    check_correct_abstention,
    check_required_facts,
    grade_answer_case,
    has_citation,
    is_abstention,
    validate_citations,
)


def test_answerable_case_has_answer():
    assert check_answerability(
        True,
        "Employees get 20 days of leave.",
    )


def test_answerable_case_without_answer_fails():
    assert not check_answerability(
        True,
        "",
    )


def test_citation_presence():
    assert has_citation(
        "Employees get 20 days.",
        ["doc-A"],
    )


def test_missing_citation_is_detected():
    assert not has_citation(
        "Employees get 20 days.",
        [],
    )


def test_valid_citation():
    assert validate_citations(
        ["doc-A"],
        ["doc-A", "doc-B"],
    )


def test_invalid_citation():
    assert not validate_citations(
        ["doc-C"],
        ["doc-A", "doc-B"],
    )


def test_required_facts_are_present():
    assert check_required_facts(
        "Employees get 20 days of annual leave.",
        ["20 days"],
    )


def test_missing_required_fact_fails():
    assert not check_required_facts(
        "Employees get 30 days of annual leave.",
        ["20 days"],
    )


def test_abstention_is_detected():
    assert is_abstention(
        "I do not have enough information to answer this."
    )


def test_correct_abstention_for_unanswerable_case():
    assert check_correct_abstention(
        False,
        "I cannot answer from the provided documents.",
    )


def test_incorrect_answer_for_unanswerable_case():
    assert not check_correct_abstention(
        False,
        "The company provides 20 days of leave.",
    )


def test_complete_answer_grading():
    result = grade_answer_case(
        expected_answerable=True,
        answer="Employees get 20 days of leave.",
        citation_ids=["doc-leave"],
        retrieved_source_ids=[
            "doc-leave",
            "doc-benefits",
        ],
        required_facts=["20 days"],
    )

    assert result == {
        "answerability_correct": True,
        "citation_present": True,
        "citation_valid": True,
        "required_facts_correct": True,
        "abstention_correct": True,
    }


def test_complete_unanswerable_grading():
    result = grade_answer_case(
        expected_answerable=False,
        answer="I do not have enough information to answer this.",
        citation_ids=[],
        retrieved_source_ids=[],
        required_facts=[],
    )

    assert result == {
        "answerability_correct": True,
        "citation_present": False,
        "citation_valid": False,
        "required_facts_correct": True,
        "abstention_correct": True,
    }