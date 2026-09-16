import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from models import SummaryOutput, ExtractionOutput, ClassificationOutput

def test_models_accept_valid_payloads():
    assert SummaryOutput(summary=['one']).summary == ['one']
    assert ExtractionOutput(name=None,email=None).name is None
    assert ClassificationOutput(label='technical',reason='about software').label == 'technical'
