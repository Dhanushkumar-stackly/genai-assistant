$ErrorActionPreference = "Continue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "GENAI ASSISTANT - DAY 5 TO DAY 7 ROADMAP VALIDATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$results = @()

function Run-Step($name, $path, $command) {
    Write-Host "`n[$name]" -ForegroundColor Yellow
    Push-Location $path
    Invoke-Expression $command
    $code = $LASTEXITCODE
    Pop-Location

    if ($code -eq 0) {
        Write-Host "PASS: $name" -ForegroundColor Green
        $script:results += "PASS - $name"
    }
    else {
        Write-Host "FAIL: $name" -ForegroundColor Red
        $script:results += "FAIL - $name"
    }
}

# DAY 5: chunk-quality automated evidence + review output
Run-Step "Day 5 - Chunk Quality Pytest" ".\day-5\task-5" "python -m pytest -v"
Run-Step "Day 5 - Chunk Quality Review" ".\day-5\task-5" "python .\scripts\inspect_chunks.py"

# DAY 6: retrieval test-set validation + actual top-3 evaluation
Run-Step "Day 6 - Retrieval Dataset Pytest" ".\day-6\task-5" "python -m pytest -v"
Run-Step "Day 6 - Top-3 Retrieval Evaluation" ".\day-6\task-5" "python .\scripts\evaluate_retrieval.py"

# DAY 7: roadmap-required integration tests
Run-Step "Day 7 - RAG Integration Pytest" ".\day-7\task-5" "python -m pytest -v"
Run-Step "Day 7 - RAG Pipeline Runtime" ".\day-7\task-5" "python .\scripts\test_rag_pipeline.py"

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "ROADMAP VALIDATION SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
$results | ForEach-Object { Write-Host $_ }
Write-Host "============================================================" -ForegroundColor Cyan
