import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from extractor import build_extraction_prompt

def test_extraction_prompt_contains_source():
    p = build_extraction_prompt("Name: Arun")
    assert "SOURCE TEXT:" in p and "Name: Arun" in p and "null" in p
