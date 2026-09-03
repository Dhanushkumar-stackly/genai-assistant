import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "outputs"

DAY6_RESULTS_FILE = OUTPUT_DIR / "day6_results.json"
DAY8_RESULTS_FILE = OUTPUT_DIR / "day8_results.json"

WEAK_QUESTIONS_FILE = OUTPUT_DIR / "weak_questions.json"


# ============================================================
# FAILURE SCORE
# ============================================================

def calculate_failure_score(day6, day8):
    """
    Calculate retrieval failure score.

    Returns:
        (score, reasons)
    """

    score = 0
    reasons = []

    expected_doc_id = day6.get("expected_doc_id")
    retrieved_doc_ids = day6.get("retrieved_doc_ids", [])
    distances = day6.get("distances", [])

    citations = day8.get("citations", [])
    status = day8.get("status")

    # --------------------------------------------------------
    # Missing expected source
    # --------------------------------------------------------

    if expected_doc_id not in retrieved_doc_ids:
        score += 5
        reasons.append("missing_expected_source")

    else:
        rank = retrieved_doc_ids.index(expected_doc_id) + 1

        # ----------------------------------------------------
        # Ranking weakness
        # ----------------------------------------------------

        if rank == 2:
            score += 2
            reasons.append("low_ranking")

        elif rank == 3:
            score += 3
            reasons.append("low_ranking")

        elif rank >= 4:
            score += 4
            reasons.append("low_ranking")

    # --------------------------------------------------------
    # No retrieval results
    # --------------------------------------------------------

    if not retrieved_doc_ids:
        if "no_retrieval_results" not in reasons:
            score += 5
            reasons.append("no_retrieval_results")

    # --------------------------------------------------------
    # No citations
    # --------------------------------------------------------

    if not citations:
        score += 2
        reasons.append("no_citations")

    # --------------------------------------------------------
    # Insufficient evidence
    # --------------------------------------------------------

    if status == "insufficient_evidence":
        score += 2
        reasons.append("insufficient_evidence")

    return score, reasons


# ============================================================
# ANALYSE FAILURE
# ============================================================

def analyse_failure(day6, day8):
    """
    Analyse one question and return structured failure data.
    """

    score, reasons = calculate_failure_score(
        day6,
        day8
    )

    return {
        "question": day6.get("question", ""),
        "expected_doc_id": day6.get(
            "expected_doc_id"
        ),
        "failure_score": score,
        "reasons": reasons,
        "retrieved_doc_ids": day6.get(
            "retrieved_doc_ids",
            []
        ),
        "distances": day6.get(
            "distances",
            []
        ),
        "status": day8.get("status"),
        "citations": day8.get(
            "citations",
            []
        )
    }


# ============================================================
# SELECT FIVE WEAKEST
# ============================================================

def select_five_weakest(results):
    """
    Return five questions with the highest failure scores.
    """

    if not isinstance(results, list):
        raise TypeError("results must be a list")

    ranked = sorted(
        results,
        key=lambda item: item.get(
            "failure_score",
            0
        ),
        reverse=True
    )

    return ranked[:5]


# ============================================================
# PUBLIC TEST COMPATIBILITY FUNCTION
# ============================================================

def select_weak_questions(day6_results, day8_results):
    """
    Combine Day 6 and Day 8 results and return
    exactly five weakest questions.

    This is the public function expected by
    tests/test_select_weak_questions.py.
    """

    if not isinstance(day6_results, list):
        raise TypeError(
            "day6_results must be a list"
        )

    if not isinstance(day8_results, list):
        raise TypeError(
            "day8_results must be a list"
        )

    day8_by_question = {
        item.get("question"): item
        for item in day8_results
    }

    analysed = []

    for day6 in day6_results:

        question = day6.get("question", "")

        day8 = day8_by_question.get(
            question,
            {
                "question": question,
                "status": None,
                "citations": []
            }
        )

        analysed.append(
            analyse_failure(
                day6,
                day8
            )
        )

    return select_five_weakest(analysed)


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):
    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("DAY 09 - SELECT FIVE WEAKEST QUESTIONS")
    print("=" * 70)

    day6_results = load_json(
        DAY6_RESULTS_FILE
    )

    day8_results = load_json(
        DAY8_RESULTS_FILE
    )

    weak_questions = select_weak_questions(
        day6_results,
        day8_results
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        WEAK_QUESTIONS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            weak_questions,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\nWeak questions selected: "
        f"{len(weak_questions)}"
    )

    for index, item in enumerate(
        weak_questions,
        1
    ):
        print(
            f"{index}. "
            f"{item['question']} "
            f"(score={item['failure_score']})"
        )

    print(
        f"\nSaved to: "
        f"{WEAK_QUESTIONS_FILE}"
    )


if __name__ == "__main__":
    main()