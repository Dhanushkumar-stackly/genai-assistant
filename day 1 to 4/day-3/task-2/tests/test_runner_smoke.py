from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
def test_runner_executes():
    r=subprocess.run([sys.executable,str(ROOT/'summarizer_runner.py')],capture_output=True,text=True)
    assert r.returncode==0
    assert 'MODEL:' in r.stdout and 'LATENCY_MS:' in r.stdout
