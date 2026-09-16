import importlib.util
from pathlib import Path
p=Path(__file__).with_name('run_prompt_tests.py')
spec=importlib.util.spec_from_file_location('run_prompt_tests',p)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
TEST_CASES=mod.TEST_CASES; PROMPT_VERSION=mod.PROMPT_VERSION; MODEL_VERSION=mod.MODEL_VERSION
validate_input=mod.validate_input; run_case=mod.run_case
