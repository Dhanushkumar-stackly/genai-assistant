# GenAI Assistant - Architecture

## 1. System Overview

The GenAI Assistant is a retrieval-augmented AI system that
accepts text and voice input, retrieves relevant knowledge,
generates a grounded response, validates the response, and
optionally converts the response to speech.

## 2. Major Components

### Input Layer

Receives:

- Text
- Audio

### STT

Converts audio into text.

### API Layer

Provides application endpoints including:

- /health
- /ingest
- /ask

### Retrieval Layer

Searches indexed documents for relevant context.

### Generation Layer

Uses the configured model to generate the response.

### Validation Layer

Checks the generated response against configured
application rules.

### TTS

Converts the final text response into speech.

### Evaluation

Measures system quality using predefined datasets
and adversarial cases.

## 3. Architecture Flow

User
→ Input
→ STT
→ Validation
→ /ask
→ Retrieval
→ Model
→ Response Validation
→ TTS
→ User

## 4. Failure Handling

If STT fails:
return an appropriate error.

If retrieval fails:
do not fabricate unsupported information.

If the model fails:
return an error or configured fallback.

If TTS fails:
return text when text fallback is supported.

## 5. Observability

Track:

- Request ID
- Stage
- Status
- Latency
- Error category

Never expose secrets through logs.