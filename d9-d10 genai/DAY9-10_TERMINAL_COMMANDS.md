# Day 9–10 Complete Terminal Command Reference

## Setup

```powershell
cd "C:\Users\Stackly_Official\Desktop\STACKLY\genai assistant 20 days challenge\d9-d10 genai"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Day 9 — Runtime outputs

```powershell
python .\src\day09\freeze_baseline.py
python .\src\day09\task2_weak_questions.py
python .\src\diagnose_retrieval_failures.py
python .\src\run_controlled_experiment.py
python .\src\generate_experiment_report.py
```

Expected artifacts:

```text
config/baseline_config.json
data/weak_questions.json
outputs/baseline_report.txt
outputs/retrieval_failure_diagnosis.json
outputs/controlled_experiment_results.json
outputs/day09_final_report.json
```

## Day 10 — Runtime outputs

```powershell
python .\src\day10\task1_experiments.py
python .\src\day10\task1_chunking_experiment.py
python .\src\day10\task2_multi_query.py
python .\src\day10\task3_reranking.py
python .\src\day10\task4_choose_best_configuration.py
python .\src\day10\task5_before_after_report.py
```

Expected artifacts:

```text
outputs/day10_task1_baseline_results.json
outputs/day10_task1_chunking_experiment.json
outputs/day10_task1_experiment_results.json
outputs/day10_task2_multi_query_results.json
outputs/day10/task3/reranking_results.json
outputs/day10_task4_best_configuration.json
outputs/day10_task5_before_after_report.json
outputs/day10_task5_before_after_report.txt
```

## Tests

```powershell
pytest -v .\tests\test_baseline.py
pytest -v .\tests\test_select_weak_questions.py
pytest -v .\tests\test_diagnose_retrieval_failures.py
pytest -v .\tests\test_controlled_experiment.py
pytest -v .\tests\test_task1_experiments.py
pytest -v .\tests\test_task1_chunking_experiment.py
pytest -v .\tests\test_task2_multi_query.py
pytest -v .\tests\test_day10_task3.py
pytest -v .\tests\test_task4_choose_best_configuration.py
pytest -v .\tests\test_task5_before_after_report.py
pytest -v
```
