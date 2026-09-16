import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from classifier import build_classification_prompt

def test_classification_prompt_defines_labels():
    p = build_classification_prompt("A server returned an error.")
    assert "business" in p and "technical" in p and "general" in p
