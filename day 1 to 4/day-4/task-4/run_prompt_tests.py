import json, time
from pathlib import Path

PROMPT_VERSION = "v1"
MODEL_VERSION = "test-model-v1"
ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "task-3" / "prompt_cases.json"

TEST_CASES = json.loads(DATASET.read_text(encoding="utf-8"))

def validate_input(value):
    if value is None or not isinstance(value, str): return False, "malformed_input"
    if not value.strip(): return False, "empty_input"
    return True, None

def run_case(case):
    start = time.perf_counter()
    valid, failure_reason = validate_input(case.get("input"))
    return {"case_id":case["case_id"],"prompt_version":PROMPT_VERSION,"model_version":MODEL_VERSION,
            "latency_ms":round((time.perf_counter()-start)*1000,3),
            "validation_result":"PASS" if valid else "FAIL",
            "failure_reason":failure_reason,"expected_label":case["expected_label"]}

def main():
    results = [run_case(c) for c in TEST_CASES]
    output_file = Path(__file__).with_name("prompt_test_results.json")
    output_file.write_text(json.dumps({"prompt_version":PROMPT_VERSION,"model_version":MODEL_VERSION,
        "total_cases":len(results),"passed":sum(r["validation_result"]=="PASS" for r in results),
        "failed":sum(r["validation_result"]=="FAIL" for r in results),"results":results},indent=2),encoding="utf-8")
    print(f"Total Cases: {len(results)}")
    print(f"Passed: {sum(r['validation_result']=='PASS' for r in results)}")
    print(f"Failed: {sum(r['validation_result']=='FAIL' for r in results)}")

if __name__ == "__main__": main()
