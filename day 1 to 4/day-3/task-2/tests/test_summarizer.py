import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from summarizer import build_summarization_prompt

def test_prompt_separates_instruction_and_source():
    p = build_summarization_prompt("AI learns from data.")
    assert "SOURCE TEXT:" in p and "AI learns from data." in p

def test_prompt_rejects_empty():
    import pytest
    with pytest.raises(ValueError): build_summarization_prompt("")
