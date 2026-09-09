from eval.scorecard import (
    build_scorecard,
    calculate_answer_score,
    calculate_overall_score,
    calculate_retrieval_score,
)


def test_retrieval_score_calculation():
    results = [
        {
            "hit_at_k": 1.0,
            "recall_at_k": 1.0,
            "reciprocal_rank": 0.5,
        }
    ]

    score = calculate_retrieval_score(results)

    assert score == 0.8333333333333334


def test_answer_score_all_correct():
    results = [
        {
            "answerability_correct": True,
            "citation_present": True,
            "citation_valid": True,
            "required_facts_correct": True,
            "abstention_correct": True,
        }
    ]

    score = calculate_answer_score(results)

    assert score == 1.0


def test_answer_score_partial():
    results = [
        {
            "answerability_correct": True,
            "citation_present": True,
            "citation_valid": False,
            "required_facts_correct": True,
            "abstention_correct": False,
        }
    ]

    score = calculate_answer_score(results)

    assert score == 0.6


def test_overall_score():
    score = calculate_overall_score(
        0.8,
        1.0,
    )

    assert score == 0.9


def test_empty_retrieval_results():
    assert calculate_retrieval_score([]) == 0.0


def test_empty_answer_results():
    assert calculate_answer_score([]) == 0.0


def test_build_scorecard():
    retrieval_results = [
        {
            "hit_at_k": 1.0,
            "recall_at_k": 1.0,
            "reciprocal_rank": 0.5,
        }
    ]

    answer_results = [
        {
            "answerability_correct": True,
            "citation_present": True,
            "citation_valid": True,
            "required_facts_correct": True,
            "abstention_correct": True,
        }
    ]

    scorecard = build_scorecard(
        retrieval_results,
        answer_results,
    )

    assert scorecard["retrieval_score"] == 0.8333333333333334
    assert scorecard["answer_score"] == 1.0
    assert scorecard["overall_score"] == 0.9166666666666667