# System Architecture

## End-to-End Flow

User
 ↓
Audio Validation
 ↓
Speech-to-Text
 ↓
Transcript
 ↓
Input Validation
 ↓
RAG Retrieval
 ↓
Grounded Answer
 ↓
Source Citations
 ↓
Text-to-Speech
 ↓
Audio Response
 ↓
User

## Observability

Request ID
 ↓
STT latency
 ↓
RAG latency
 ↓
TTS latency
 ↓
Total latency

## Failure Handling

STT failure
 ↓
Stop

Empty transcript
 ↓
Stop before RAG

RAG failure
 ↓
Record failure

TTS failure
 ↓
Text answer + sources

## Example Request

POST /ask

Content-Type: application/json

{
    "question": "What is the leave policy?"
}

{
    "answer": "Employees can take annual leave according to the company leave policy.",
    "sources": [
        {
            "document_id": "DOC001",
            "title": "Company Leave Policy"
        }
    ]
}

{
    "answer": "Employees can take annual leave according to the company leave policy.",
    "sources": [
        {
            "document_id": "DOC001",
            "title": "Company Leave Policy"
        }
    ]
}

# Unsupported Use Cases

The system should not be treated as:

- a general-purpose chatbot
- an authoritative source outside the configured knowledge base
- a substitute for human approval of sensitive decisions
- a system with guaranteed real-time voice latency
- a system that can answer questions without supporting evidence
- a system that should synthesize speech from ungrounded answers