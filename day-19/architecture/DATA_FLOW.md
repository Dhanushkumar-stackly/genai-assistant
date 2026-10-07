# Data Flow

## 1. Voice Query

Audio
→ STT
→ Transcript
→ Query Validation
→ Retrieval
→ Context
→ Model
→ Answer
→ Response Validation
→ TTS
→ Audio Response

## 2. Text Query

Text
→ Query Validation
→ Retrieval
→ Context
→ Model
→ Response Validation
→ Text Response

## 3. Document Ingestion

Document
→ Validation
→ Processing
→ Chunking
→ Embedding
→ Vector Storage
→ Available for Retrieval

## 4. Evaluation

Test Dataset
→ Test Runner
→ Model/RAG Pipeline
→ Scoring
→ Result Artifact
→ Regression Comparison