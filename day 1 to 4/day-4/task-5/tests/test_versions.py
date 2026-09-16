from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_extractor_has_two_versions():
    v1=(ROOT/'extractor/v1.txt').read_text(); v2=(ROOT/'extractor/v2.txt').read_text()
    assert v1.strip() and v2.strip() and v1 != v2
    assert 'Do not infer' in v2

def test_all_prompt_files_nonempty():
    for p in (ROOT/'classifier/v1.txt',ROOT/'summarizer/v1.txt'):
        assert p.read_text(encoding='utf-8').strip()
