from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_all_prompt_sample_types_exist():
    for category in ("classification", "extraction", "summarization"):
        for kind in ("normal", "long", "ambiguous", "incomplete"):
            p = ROOT / category / f"{kind}.txt"
            assert p.exists() and p.read_text(encoding="utf-8").strip()
