# Day 18 - GenAI Assistant Training Project

## Voice Assistant: TTS, Full Audio-to-Audio Flow, Failure Recovery, Latency Tracking and Voice Evaluation

---

## 1. Day 18 Overview

Day 18 extends the voice capability of the GenAI Assistant.

The main objective is to take a user's audio question, convert it into text, process the question through the grounded RAG flow, convert the validated answer back into audio, and evaluate the complete voice interaction.

The Day 18 flow is:

```text
User Audio
    |
    v
Audio Validation
    |
    v
Speech-to-Text (STT)
    |
    v
Transcript
    |
    v
RAG / Grounded Answer
    |
    v
Source Citations
    |
    v
Text-to-Speech (TTS)
    |
    v
Audio Response
```

Day 18 also adds failure recovery, latency measurement, and voice-specific evaluation.

---

# 2. Day 18 Objectives

The main objectives are:

- Convert validated grounded answers into audio.
- Complete the audio-to-audio voice pipeline.
- Preserve source citations in voice responses.
- Use one request ID across STT, RAG and TTS.
- Handle STT, RAG and TTS failures safely.
- Keep the validated text answer available when TTS fails.
- Prevent RAG from receiving an empty or unreliable transcript.
- Measure STT, RAG, TTS and total latency.
- Identify the slowest pipeline stage.
- Evaluate at least five voice-question cases.
- Record transcript quality, task completion, citation correctness, response delay and failure stage.

---

# 3. Project Scope

Day 18 covers five implementation tasks.

| Task | Module | Purpose |
|---|---|---|
| Task 1 | `app/tts.py` | Text-to-Speech |
| Task 2 | `app/pipeline.py` | Complete voice flow |
| Task 3 | `app/failure_recovery.py` | Failure recovery |
| Task 4 | `app/latency_tracker.py` | Latency tracking |
| Task 5 | `app/voice_evaluation.py` | Voice-specific evaluation |

---

# 4. Folder Structure

```text
day18/
│
├── app/
│   ├── __init__.py
│   ├── tts.py
│   ├── pipeline.py
│   ├── failure_recovery.py
│   ├── latency_tracker.py
│   └── voice_evaluation.py
│
├── tests/
│   ├── test_task1_tts.py
│   ├── test_task2_voice_flow.py
│   ├── test_task3_failure_recovery.py
│   ├── test_task4_latency.py
│   └── test_task5_voice_evaluation.py
│
├── audio/
│   └── generated audio files
│
├── outputs/
│   └── task5_voice_evaluation.json
│
├── run_task1.py
├── run_task2.py
├── run_task3.py
├── run_task4.py
├── run_task5.py
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# 5. Technologies Used

- Python
- pytest
- Text-to-Speech
- Speech-to-Text flow
- Retrieval-Augmented Generation (RAG)
- WAV audio
- JSON evaluation report
- `time.perf_counter()` for latency measurement
- UUID request IDs
- Git and GitHub

---

# 6. System Architecture

```text
                         +------------------+
                         |   User Audio     |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Audio Validation |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |       STT        |
                         | Speech-to-Text   |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Transcript    |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |   RAG Pipeline   |
                         | Retrieval +      |
                         | Grounded Answer  |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Sources/Citation |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |       TTS        |
                         | Text-to-Speech   |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |  Audio Response  |
                         +------------------+
```

Every request uses a unique request ID so the stages can be correlated.

---

# 7. Task 1 - Text-to-Speech

## 7.1 Objective

Task 1 converts a validated, grounded answer into an audio response.

The TTS layer must not generate speech from an unvalidated answer or an answer without sources.

## 7.2 Implementation

Main file:

```text
app/tts.py
```

The module contains:

- `GroundedAnswer`
- TTS provider abstraction
- Demo eSpeak provider
- OpenAI provider interface
- Grounded-answer validation
- WAV generation
- Synthetic voice indication

The validation checks:

```text
Validated answer
        +
Non-empty answer
        +
At least one source
        =
TTS allowed
```

## 7.3 Real-Time Example

Question:

```text
What is the leave policy?
```

The RAG system produces a source-backed answer.

The TTS module converts that answer into a WAV file.

## 7.4 Run Command

```powershell
python run_task1.py
```

## 7.5 Actual Output

```text
DAY 18 - TASK 1: TEXT-TO-SPEECH
Provider          : demo-espeak
Synthetic voice   : True
Format            : wav
MIME type         : audio/wav
Audio file        : audio/synthetic_day18-task1-demo.wav
Audio size (bytes): 189316
TTS latency (ms)  : 19.545
Grounded answer   : validated + source-backed
STATUS            : PASS
```

## 7.6 Test

```powershell
pytest -v tests/test_task1_tts.py
```

Result:

```text
4 passed
```

## 7.7 Task 1 Result

```text
PASS
```

A grounded answer was successfully converted to audio.

---

# 8. Task 2 - Complete Voice Flow

## 8.1 Objective

Task 2 integrates the complete voice pipeline.

```text
Audio
 ↓
STT
 ↓
RAG
 ↓
TTS
 ↓
Audio
```

A single request ID is maintained across all stages.

## 8.2 Implementation

Main file:

```text
app/pipeline.py
```

The pipeline returns:

- Request ID
- Status
- Transcript
- Answer
- Sources
- Audio reference
- Audio format
- MIME type
- Synthetic voice flag
- STT latency
- RAG latency
- TTS latency
- Total latency

## 8.3 Real-Time Example

User asks:

```text
What is the leave policy?
```

The system:

1. Validates the audio.
2. Transcribes the speech.
3. Sends the transcript to RAG.
4. Generates a grounded answer.
5. Retains the source citation.
6. Sends the grounded answer to TTS.
7. Returns text and audio.

## 8.4 Run Command

```powershell
python run_task2.py
```

## 8.5 Actual Output

```text
DAY 18 - TASK 2: COMPLETE VOICE FLOW
Request ID        : c3f2c6b2-c839-4d1b-993f-25ed6aa56932
Status            : completed
Transcript        : What is the leave policy?
Answer            : Employees can take annual leave according to the company leave policy, subject to the applicable approval process.
Sources           : [{'document_id': 'DOC001', 'title': 'Company Leave Policy', 'citation': 'DOC001'}]
Audio             : audio/synthetic_c3f2c6b2-c839-4d1b-993f-25ed6aa56932.wav
Audio format      : audio/wav
Synthetic voice   : True
STT latency (ms)  : 0.0
RAG latency (ms)  : 0.0
TTS latency (ms)  : 17.14
Total latency(ms) : 17.31
Audio size(bytes) : 298486
Same request ID across STT -> RAG -> TTS : YES
STATUS            : PASS
```

## 8.6 Test

```powershell
pytest -v tests/test_task2_voice_flow.py
```

Result:

```text
4 passed
```

## 8.7 Task 2 Result

```text
PASS
```

The complete voice flow successfully produced a grounded answer and audio response.

---

# 9. Task 3 - Failure Recovery

## 9.1 Objective

Task 3 ensures that failures in one stage do not create unsafe or misleading downstream behavior.

The two major requirements are:

1. If TTS fails, the validated text answer and sources must remain available.
2. If STT fails or returns an empty transcript, RAG must not be called.

## 9.2 Failure Flow

### TTS Failure

```text
Audio
 ↓
STT
 ↓
RAG
 ↓
TTS Failure
 ↓
Validated Text + Sources
```

### STT Failure

```text
Audio
 ↓
STT Failure
 ↓
STOP
```

### Empty Transcript

```text
Audio
 ↓
STT
 ↓
Empty Transcript
 ↓
STOP
```

## 9.3 Implementation

Main file:

```text
app/failure_recovery.py
```

Main function:

```python
recoverable_voice_flow()
```

Failure stages are recorded as:

```text
stt
rag
tts
```

When TTS fails:

```text
status = completed_text_only
```

## 9.4 Run Command

```powershell
python run_task3.py
```

## 9.5 Actual Output

```text
DAY 18 - TASK 3: FAILURE RECOVERY
Request ID     : 6ee99be2-8fdd-458d-a9ae-5b99da698176
Status         : completed_text_only
Failure stage  : tts
Transcript     : What is the leave policy?
Answer         : Employees can take annual leave according to thecompany leave policy.
Sources        : [{'document_id': 'DOC001', 'title': 'Company Leave Policy'}]
Audio          : None
Error          : TTS service temporarily unavailable
Total latency  : 0.011 ms
TEXT FALLBACK  : AVAILABLE
STATUS         : PASS
```

## 9.6 Tests

```powershell
pytest -v tests/test_task3_failure_recovery.py
```

Result:

```text
3 passed
```

The tests verify:

- TTS failure preserves answer and sources.
- STT failure prevents RAG.
- Empty transcript prevents RAG.

## 9.7 Task 3 Result

```text
PASS
```

The text fallback remains available when TTS fails.

---

# 10. Task 4 - Latency Budget Tracking

## 10.1 Objective

Task 4 measures the latency contribution of each major stage.

```text
STT
 ↓
RAG
 ↓
TTS
 ↓
TOTAL
```

## 10.2 Implementation

Main file:

```text
app/latency_tracker.py
```

Timing uses:

```python
time.perf_counter()
```

The tracker records:

- Request ID
- Stage name
- Stage latency
- Total latency

## 10.3 Run Command

```powershell
python run_task4.py
```

## 10.4 Actual Output

```text
DAY 18 - TASK 4: LATENCY BUDGET TRACKING
Request ID : 0ccd13f0-af31-42c3-994f-04b7427fcfe8
STT latency : 50.272 ms
RAG latency : 80.279 ms
TTS latency : 60.629 ms
Total latency : 191.927 ms

Latency breakdown:
  stt: 50.272 ms
  rag: 80.279 ms
  tts: 60.629 ms

STATUS : PASS
```

## 10.5 Slowest Stage

For the demonstrated run:

| Stage | Latency |
|---|---:|
| STT | 50.272 ms |
| RAG | 80.279 ms |
| TTS | 60.629 ms |

The largest measured stage was:

```text
RAG = 80.279 ms
```

## 10.6 Practical Improvement

A practical optimization is to reduce unnecessary retrieval work.

Possible changes:

- Reduce the retrieval candidate set.
- Tune `top-k`.
- Avoid redundant retrieval operations.
- Keep retrieved context focused.
- Re-test citation correctness and answer quality after optimization.

The optimization should reduce latency without weakening grounding quality.

## 10.7 Test

```powershell
pytest -v tests/test_task4_latency.py
```

Result:

```text
4 passed
```

## 10.8 Task 4 Result

```text
PASS
```

The latency budget is measured and the slowest stage is documented.

---

# 11. Task 5 - Voice-Specific Evaluation

## 11.1 Objective

Task 5 evaluates five voice-question cases.

The evaluation records:

- Transcript quality
- Task completion
- Citation correctness
- Response delay
- Failure stage
- Overall status

## 11.2 Evaluation Cases

| Case | Question | Expected Source |
|---|---|---|
| voice_01 | What is the leave policy? | DOC001 |
| voice_02 | How do I apply for leave? | DOC001 |
| voice_03 | What documents are required for onboarding? | DOC002 |
| voice_04 | What is the work from home policy? | DOC003 |
| voice_05 | Who approves annual leave? | DOC001 |

## 11.3 Implementation

Main file:

```text
app/voice_evaluation.py
```

The evaluator checks:

### Transcript Quality

A transcript is considered valid when it is present and non-empty.

### Task Completion

The result must contain a valid answer and a completed or text-only completion status.

### Citation Correctness

The expected document ID must appear in the returned source list.

### Response Delay

The total response latency is recorded in milliseconds.

### Failure Stage

The system records the stage where a failure occurred.

## 11.4 Run Command

```powershell
python run_task5.py
```

## 11.5 Actual Output

```text
DAY 18 - TASK 5: VOICE-SPECIFIC EVALUATION

voice_01
Question              : What is the leave policy?
Transcript quality    : PASS
Task completion       : PASS
Citation correctness  : PASS
Response delay        : 190.0 ms
Failure stage         : None
Status                : PASS

voice_02
Question              : How do I apply for leave?
Transcript quality    : PASS
Task completion       : PASS
Citation correctness  : PASS
Response delay        : 190.0 ms
Failure stage         : None
Status                : PASS

voice_03
Question              : What documents are required for onboarding?
Transcript quality    : PASS
Task completion       : PASS
Citation correctness  : PASS
Response delay        : 190.0 ms
Failure stage         : None
Status                : PASS

voice_04
Question              : What is the work from home policy?
Transcript quality    : PASS
Task completion       : PASS
Citation correctness  : PASS
Response delay        : 190.0 ms
Failure stage         : None
Status                : PASS

voice_05
Question              : Who approves annual leave?
Transcript quality    : PASS
Task completion       : PASS
Citation correctness  : PASS
Response delay        : 190.0 ms
Failure stage         : None
Status                : PASS

==================================================
VOICE EVALUATION SUMMARY
==================================================
Total cases            : 5
Transcript quality     : 5/5
Task completion        : 5/5
Citation correctness   : 5/5
Overall pass           : 5/5
Average response delay: 190.0 ms

Evaluation report     : outputs/task5_voice_evaluation.json

STATUS : PASS
```

## 11.6 Test

```powershell
pytest -v tests/test_task5_voice_evaluation.py
```

Result:

```text
4 passed
```

## 11.7 Evaluation Result

```text
Total cases            : 5
Transcript quality     : 5/5
Task completion        : 5/5
Citation correctness   : 5/5
Overall pass           : 5/5
Average response delay: 190.0 ms
```

## 11.8 Evaluation Evidence Note

The current Task 5 runner uses deterministic voice-flow test fixtures and five question cases.

Therefore, the implementation should be described as a **voice evaluation test fixture**, not as five independently recorded human audio questions.

For stronger real-audio evidence, the five cases can later be connected to actual recorded audio files and executed through the real STT stage.

---

# 12. Complete Day 18 Testing

After all five tasks are implemented, run the complete test suite:

```powershell
pytest -v
```

Verified full result:

```text
19 passed
```

## Test Breakdown

| Task | Tests | Result |
|---|---:|---|
| Task 1 | 4 | PASS |
| Task 2 | 4 | PASS |
| Task 3 | 3 | PASS |
| Task 4 | 4 | PASS |
| Task 5 | 4 | PASS |
| **Total** | **19** | **19/19 PASS** |

---

# 13. Day 18 Completion Gate

The Day 18 completion requirements are checked below.

| Requirement | Status |
|---|---|
| Grounded answer returned as text | PASS |
| Grounded answer returned as audio | PASS |
| TTS integration implemented | PASS |
| Complete audio-to-audio flow | PASS |
| Text remains when TTS fails | PASS |
| STT failure prevents RAG | PASS |
| Empty transcript prevents RAG | PASS |
| Source citations retained | PASS |
| Same request ID across stages | PASS |
| STT latency measured | PASS |
| RAG latency measured | PASS |
| TTS latency measured | PASS |
| Total latency measured | PASS |
| Slowest stage identified | PASS |
| Practical latency improvement documented | PASS |
| Five voice evaluation cases | PASS |
| Transcript quality recorded | PASS |
| Task completion recorded | PASS |
| Citation correctness recorded | PASS |
| Response delay recorded | PASS |
| Failure stage recorded | PASS |
| Automated tests | 19/19 PASS |

---

# 14. Outputs and Evidence

Generated evidence includes:

```text
audio/synthetic_day18-task1-demo.wav
audio/synthetic_<request-id>.wav
outputs/task5_voice_evaluation.json
```

The generated TTS audio can be played to demonstrate the audio response.

The Task 5 JSON file contains the evaluation summary and individual case results.

---

# 15. Error Handling and Reliability

Day 18 introduces explicit stage-level failure handling.

## STT Failure

The pipeline stops before RAG.

This prevents empty or unreliable input from being processed.

## RAG Failure

The request is marked as failed at the RAG stage.

## TTS Failure

The grounded text answer and sources are retained.

The response becomes:

```text
completed_text_only
```

This provides graceful degradation instead of losing the complete response.

---

# 16. Security / Guardrails

The voice pipeline maintains the existing grounded-answer principle.

Important controls include:

- Do not synthesize speech from an unvalidated answer.
- Require source-backed grounded content before TTS.
- Do not send an empty transcript to RAG.
- Track failure stage.
- Preserve source metadata.
- Maintain request IDs for traceability.
- Keep text fallback available when TTS fails.
- Mark the demo voice as synthetic.

---

# 17. Latency Analysis

The demonstrated Task 4 latency was:

```text
STT : 50.272 ms
RAG : 80.279 ms
TTS : 60.629 ms
Total : 191.927 ms
```

The RAG stage contributed the largest measured latency in this test run.

A practical improvement is retrieval optimization through candidate-set and `top-k` tuning and removal of redundant retrieval operations.

Any optimization should be validated against:

- Answer correctness
- Citation correctness
- Grounding quality
- Total latency

---

# 18. Voice Evaluation Summary

The five evaluation cases produced:

```text
Transcript Quality     : 5/5
Task Completion        : 5/5
Citation Correctness   : 5/5
Overall Pass           : 5/5
Average Response Delay : 190.0 ms
```

The evaluation report is stored at:

```text
outputs/task5_voice_evaluation.json
```

---

# 19. Installation and Requirements

Activate the virtual environment:

```powershell
.env\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the complete tests:

```powershell
pytest -v
```

---

# 20. Run All Day 18 Tasks

```powershell
python run_task1.py
python run_task2.py
python run_task3.py
python run_task4.py
python run_task5.py
```

Then:

```powershell
pytest -v
```

Expected final test result:

```text
19 passed
```

---

# 21. Git and GitHub

Day 18 changes should be committed to the existing Day 17-18 branch.

Check the current branch:

```powershell
git branch
```

Check changes:

```powershell
git status
```

Add Day 18 files:

```powershell
git add app tests run_task1.py run_task2.py run_task3.py run_task4.py run_task5.py requirements.txt pytest.ini README.md outputs
```

Commit:

```powershell
git commit -m "day 18 complete voice assistant pipeline"
```

Push:

```powershell
git push origin day-17-18
```

Verify:

```powershell
git status
```

Expected:

```text
nothing to commit, working tree clean
```

The push should only be considered successful after the terminal confirms it.

---

# 22. Recommended Git Evidence

Before finalizing Day 18, capture:

```powershell
git status
git log --oneline -5
git branch
```

The commit should contain the Day 18 implementation, tests and documentation.

---

# 23. Challenges Faced and Solutions

## Challenge 1 - Converting grounded text to audio

### Solution

A dedicated TTS module was created with grounded-answer validation before speech generation.

## Challenge 2 - Maintaining source citations

### Solution

Sources are retained as part of the pipeline response and passed alongside the answer.

## Challenge 3 - TTS service failure

### Solution

The system returns the validated text answer and sources even when TTS fails.

## Challenge 4 - STT failure

### Solution

The pipeline stops before RAG when STT fails or returns an empty transcript.

## Challenge 5 - Voice latency

### Solution

A dedicated latency tracker records each major stage and total request time.

## Challenge 6 - Voice-specific evaluation

### Solution

A structured evaluation module records five cases and the required quality and performance metrics.

---

# 24. Final Day 18 Result

Day 18 successfully implements the voice-response layer around the grounded GenAI Assistant.

The completed workflow is:

```text
Audio Input
    ↓
STT
    ↓
Grounded RAG
    ↓
Source Citations
    ↓
TTS
    ↓
Audio Output
```

Additional reliability and evaluation features include:

```text
Failure Recovery
+
Latency Tracking
+
Voice Evaluation
+
Automated Testing
```

Final automated test result:

```text
19 / 19 PASSED
```

## Day 18 Status

```text
========================================
DAY 18 - COMPLETED
========================================

Task 1 : PASS
Task 2 : PASS
Task 3 : PASS
Task 4 : PASS
Task 5 : PASS

Full Test Suite : 19/19 PASS

Voice Flow       : COMPLETE
Failure Recovery: COMPLETE
Latency Tracking : COMPLETE
Voice Evaluation : COMPLETE
========================================
```

---

# 25. Future Enhancements

Possible improvements for a production implementation:

- Connect Task 5 to real recorded audio questions.
- Replace deterministic STT fixtures with production STT.
- Add streaming TTS.
- Add asynchronous pipeline execution where appropriate.
- Add persistent voice request logs.
- Add real latency dashboards.
- Add more voice evaluation cases.
- Evaluate transcription accuracy using reference transcripts.
- Add multilingual voice support.
- Add authentication and rate limiting to voice endpoints.
- Add audio retention and privacy controls.
- Optimize RAG retrieval latency while monitoring grounding quality.

---

# 26. Conclusion

Day 18 extends the GenAI Assistant from a text-oriented grounded assistant into a complete voice interaction workflow.

The system can process audio, generate a grounded answer, retain source citations, and convert the response into audio.

The implementation also demonstrates graceful failure handling. A TTS failure does not remove the validated text answer, while STT failures are prevented from reaching the RAG layer.

Latency is measured at individual stages, and voice-specific evaluation is performed across five test cases.

The complete Day 18 test suite passed with:

```text
19/19 tests passed
```

This provides the implementation and automated evidence required for the Day 18 voice-assistant workflow.
test_task1_tts.py
test_task2_voice_flow.py
test_task3_failure_recovery.py
test_task4_latency.py
test_task5_voice_evaluation.py