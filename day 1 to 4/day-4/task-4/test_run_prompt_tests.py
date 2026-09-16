from task_4_runner import TEST_CASES, PROMPT_VERSION, MODEL_VERSION, validate_input, run_case

def test_ten_cases(): assert len(TEST_CASES) == 10
def test_valid_input(): assert validate_input('hello') == (True, None)
def test_malformed_input(): assert validate_input(None)[1] == 'malformed_input'
def test_empty_input(): assert validate_input(' ')[1] == 'empty_input'
def test_case_metadata():
    r=run_case(TEST_CASES[0]); assert r['prompt_version']==PROMPT_VERSION and r['model_version']==MODEL_VERSION and r['validation_result']=='PASS'
def test_all_cases_have_result_fields():
    for c in TEST_CASES:
        r=run_case(c); assert r['case_id']==c['case_id']; assert 'latency_ms' in r; assert r['validation_result'] in {'PASS','FAIL'}
