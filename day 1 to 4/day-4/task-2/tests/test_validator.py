import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from validator import validate_response

def test_valid_response(): assert validate_response('classification',{'label':'technical','reason':'software'})[0] is True
def test_invalid_response_is_validation_error():
    ok,cat,_=validate_response('classification',{'label':'other','reason':'x'}); assert not ok and cat=='validation_error'
def test_unknown_task(): assert validate_response('unknown',{})[1]=='validation_error'
