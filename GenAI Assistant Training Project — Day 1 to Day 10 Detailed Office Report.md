# GENAI ASSISTANT TRAINING PROJECT

## Day 1 – Day 10 Training & Implementation Report

**Project Area:** Generative AI, Prompt Engineering and Retrieval-Augmented Generation  
**Project Type:** Practical Training and Implementation Project  
**Project Duration:** Day 1 – Day 10  
**Programming Language:** Python  
**Testing Framework:** Pytest  
**Repository:** GenAI Assistant  
**Version Control:** Git and GitHub  

---

# 1. TITLE PAGE

## GENAI ASSISTANT TRAINING PROJECT

### Day 1 – Day 10 Training & Implementation Report

This report documents the practical implementation completed during the first ten days of the GenAI Assistant training project.

The project started with basic prompt engineering concepts and gradually developed into a document-based Retrieval-Augmented Generation workflow.

The major areas covered during the training were:

- Prompt Engineering
- Classification
- Information Extraction
- Summarization
- Prompt Versioning
- Input Validation
- Document Processing
- Text Cleaning
- Text Chunking
- Metadata Management
- Embeddings
- Vector Database
- Semantic Search
- RAG
- Grounded Generation
- Citation Validation
- Abstention
- Retrieval Evaluation
- Retrieval Experiments
- Git and GitHub

The project was developed incrementally. Each day introduced a new technical concept and connected it with the previous day's work.

---

# 2. PROJECT OVERVIEW

## 2.1 Introduction

Generative AI applications are often presented as simple applications where a user asks a question and an AI model provides an answer.

In a real application, the process is more complicated.

If an organization wants an AI assistant to answer questions from its own documents, the system must first understand those documents. It must identify useful information, store that information in a searchable format and retrieve the right information when the user asks a question.

The GenAI Assistant Training Project was created to understand this complete process through hands-on implementation.

The training did not start directly with RAG.

Instead, the project was developed step by step.

The first stage focused on understanding how prompts work.

The next stage focused on preparing documents.

After that, embeddings and vector search were introduced.

Then the retrieval process was connected to a RAG workflow.

Finally, the retrieval system was evaluated and improved through controlled experiments.

The overall development path was:

```text
Prompt Engineering
        ↓
Input Validation
        ↓
Document Processing
        ↓
Text Cleaning
        ↓
Text Chunking
        ↓
Metadata Creation
        ↓
Embedding Generation
        ↓
Vector Database
        ↓
Semantic Retrieval
        ↓
RAG Pipeline
        ↓
Grounded Generation
        ↓
Citation Validation
        ↓
Abstention
        ↓
Retrieval Evaluation
        ↓
Experimentation
        ↓
Configuration Selection
```

This progression helped in understanding not only how each component works, but also why each component is required.

---

# 3. PROJECT OBJECTIVE

The main objective of this project was to gain practical experience in developing a document-based Generative AI assistant.

The project objectives were:

1. Understand prompt engineering.
2. Design prompts for different AI tasks.
3. Create structured outputs.
4. Validate user input.
5. Create prompt test cases.
6. Understand document preprocessing.
7. Clean document content.
8. Split documents into manageable chunks.
9. Add metadata to chunks.
10. Generate embeddings.
11. Store embeddings in a vector database.
12. Retrieve relevant document chunks.
13. Build a RAG workflow.
14. Generate answers using retrieved evidence.
15. Validate citations.
16. Handle insufficient evidence through abstention.
17. Measure retrieval performance.
18. Diagnose retrieval failures.
19. Experiment with different retrieval configurations.
20. Use Git and GitHub for version control.

The project therefore covered both **GenAI concepts and practical software engineering concepts**.

---

# 4. PROBLEM STATEMENT

## 4.1 Business-Level Problem

Suppose an organization has hundreds or thousands of internal documents.

These documents may contain:

- Company policies
- Technical documentation
- Employee information
- Product information
- Process documents
- Frequently asked questions
- Internal guidelines

A normal keyword search may not always understand what the user means.

For example, a user may ask:

> "What is required before deploying a trained machine learning model?"

The exact sentence may not exist in the documents.

The document may instead contain:

> "Before deployment, the trained model should be validated, packaged and prepared for the production environment."

A simple keyword search may not understand that these two statements are related.

This is where semantic retrieval becomes useful.

---

## 4.2 Technical Problem

A reliable document-based GenAI assistant needs to solve several problems:

### Problem 1 — Understanding the input

The system must identify whether the input is valid.

### Problem 2 — Preparing documents

Documents may contain unnecessary spaces, formatting issues or inconsistent line endings.

### Problem 3 — Chunking

Large documents cannot always be passed directly into a retrieval or generation process.

They need to be divided into smaller chunks.

### Problem 4 — Searching

The system needs to find the chunks that are most relevant to a user's question.

### Problem 5 — Grounding

The AI should answer based on retrieved evidence instead of freely generating information.

### Problem 6 — Insufficient evidence

If the documents do not contain enough information, the system should not simply guess.

### Problem 7 — Measuring quality

A retrieval system should not be judged only by looking at a few answers.

It needs measurable evaluation.

The training project addressed these problems progressively.

---

# 5. PROJECT SCOPE

## 5.1 Prompt Engineering Scope

The first part of the project covered:

- Classification
- Information extraction
- Summarization
- Prompt versioning
- Prompt testing
- Input validation

---

## 5.2 Document Processing Scope

The document-processing stage covered:

- Document loading
- Text cleaning
- Chunking
- Chunk overlap
- Metadata
- Chunk quality review

---

## 5.3 Retrieval Scope

The retrieval stage covered:

- Embedding generation
- Vector storage
- Semantic search
- Top-k retrieval
- Metadata
- Retrieval evaluation

---

## 5.4 RAG Scope

The RAG stage covered:

- Document ingestion
- Retrieval
- Context preparation
- Grounded prompts
- Response schema
- Citation mapping
- Abstention

---

## 5.5 Evaluation Scope

The evaluation stage covered:

- Baseline creation
- Weak-question selection
- Failure diagnosis
- Controlled experiments
- Chunking experiments
- Multi-query retrieval
- Reranking
- Before/after comparison

The project documentation confirms these evaluation components were added during Days 9 and 10.

---

# 6. TECHNOLOGIES USED

| Technology | Purpose |
|---|---|
| Python | Main development language |
| Pytest | Automated testing |
| JSON | Test data, configuration and results |
| Sentence Transformers | Embedding generation |
| all-MiniLM-L6-v2 | Embedding model |
| ChromaDB | Vector storage and semantic search |
| Pydantic | Structured response validation |
| Scikit-learn | Supporting evaluation utilities |
| SQLite | Experiment data storage |
| Git | Version control |
| GitHub | Repository hosting |

The selected technologies were suitable for the training because they allowed the project to be developed locally in small, understandable modules.

---

# 7. SYSTEM ARCHITECTURE / WORKFLOW

The complete project can be understood through two connected flows.

## 7.1 Document Flow

```text
Documents
    ↓
Document Loader
    ↓
Text Cleaning
    ↓
Text Chunking
    ↓
Metadata Creation
    ↓
Embedding Generation
    ↓
ChromaDB
```

The document is first loaded.

The text is then cleaned.

After cleaning, the document is divided into smaller chunks.

Each chunk receives metadata.

The chunk is converted into an embedding.

The embedding is stored in ChromaDB.

---

## 7.2 Question Flow

When the user asks a question:

```text
User Question
      ↓
Question Embedding
      ↓
Semantic Search
      ↓
Relevant Chunks
      ↓
Evidence Check
      ↓
 ┌───────────────┐
 │               │
Enough Evidence  Not Enough Evidence
 │               │
 ↓               ↓
Grounded        Abstention
Context
 ↓
Answer Generation
 ↓
Citation Mapping
 ↓
Structured Response
```

---

# 8. COMPLETE END-TO-END PROJECT FLOW

The complete system can therefore be explained in simple terms.

### Step 1 — Documents enter the system

The system receives approved documents.

### Step 2 — Documents are cleaned

Unnecessary formatting and inconsistent whitespace are normalized.

### Step 3 — Documents are divided

Large documents are divided into smaller chunks.

### Step 4 — Metadata is added

Each chunk receives information such as:

- Document ID
- Chunk ID
- Title
- Source path
- Chunk index
- Update information

### Step 5 — Embeddings are generated

The text is converted into a numerical representation using the embedding model.

### Step 6 — Embeddings are stored

The vectors are stored in ChromaDB.

### Step 7 — User asks a question

The question is also converted into an embedding.

### Step 8 — Semantic search happens

The system searches the vector database for similar chunks.

### Step 9 — Relevant evidence is selected

The top relevant chunks are returned.

### Step 10 — Evidence is checked

The system determines whether there is enough information.

### Step 11 — Grounded generation happens

If enough evidence exists, the response is generated using that evidence.

### Step 12 — Citations are mapped

The response is linked back to the retrieved chunks.

### Step 13 — Abstention happens when required

If evidence is insufficient, the system can avoid generating an unsupported answer.

### Step 14 — Retrieval quality is measured

The retrieval system is evaluated using metrics.

### Step 15 — Configuration is improved

Experiments are conducted and the better configuration is selected.

This is the main story of the entire ten-day project.

---

# 9. DAY-WISE IMPLEMENTATION

# DAY 1 — INTRODUCTION TO PROMPT ENGINEERING

## 9.1 Objective

Day 1 introduced prompt engineering through a document classification task.

The goal was to understand how a prompt can control an AI model's expected output.

---

## 9.2 Classification Problem

The system was designed to classify a document into one of three categories:

```text
invoice
receipt
other
```

The important requirement was that the model should not create its own category.

For example:

```text
invoice
```

is valid.

But:

```text
financial_invoice
```

would not be an allowed label.

---

## 9.3 Prompt Design

The prompt was designed to:

- Restrict the output labels.
- Ask for a short reason.
- Return JSON.
- Use only the supplied document.
- Avoid unsupported information.

Example:

```json
{
  "label": "invoice",
  "reason": "The document contains invoice-specific information."
}
```

---

## 9.4 Why This Task Was Important

This was the first step toward controlling an AI model.

Instead of asking:

> "What is this document?"

the prompt defines exactly what kind of answer is expected.

This is an important prompt-engineering principle.

The more clearly the expected output is defined, the easier it becomes to validate the result.

---

# DAY 2 — INFORMATION EXTRACTION

## 10.1 Objective

Day 2 moved from classification to structured information extraction.

The objective was to extract predefined information from documents.

The fields included:

```text
invoice_number
customer_name
customer_email
invoice_date
total_amount
```

---

## 10.2 Important Rule

The system should not invent missing information.

If a field is not available, the expected value is:

```json
null
```

This is important because a GenAI system should not create information simply because the output format requires a value.

---

## 10.3 Example

If a document contains:

```text
Invoice Number: INV001
Customer Name: ABC Technologies
```

but does not contain an email address, the response should represent the missing field as:

```json
{
  "invoice_number": "INV001",
  "customer_name": "ABC Technologies",
  "customer_email": null
}
```

This makes the output predictable.

---

## 10.4 Prompt Versioning

The extraction prompts were maintained separately:

```text
prompts/
└── extractor/
    ├── v1.txt
    └── v2.txt
```

This means the older prompt can be retained while a new version is developed.

That is useful when comparing prompt behaviour.

---

# DAY 3 — SUMMARIZATION AND PROMPT VERSIONING

## 11.1 Objective

Day 3 introduced summarization.

The objective was to convert longer text into a concise summary while keeping the important information.

---

## 11.2 Summarization Rules

The prompt was designed to:

- Identify the main topic.
- Keep important facts.
- Avoid unnecessary detail.
- Avoid unsupported information.
- Produce a concise response.

---

## 11.3 Why Summarization Matters

In a real organization, documents can be long.

A user may not want the entire document.

They may simply ask:

> "Give me a short summary."

A summarization prompt allows the system to produce a shorter version of the content.

---

## 11.4 Prompt Version Structure

The project used:

```text
prompts/
├── summarization.txt
└── summarizer/
    └── v1.txt
```

This introduced the concept of maintaining prompts like source code.

A prompt is not treated as temporary text.

It becomes part of the project implementation.

---

# DAY 4 — INPUT VALIDATION AND PROMPT TESTING

## 12.1 Objective

Day 4 focused on testing and validation.

The project created ten test cases.

The cases included:

- Valid input
- Ambiguous input
- Malformed input
- Empty input

---

## 12.2 Input Validation

The validator handled cases such as:

```text
None
non-string input
empty string
whitespace-only input
valid text
```

For example:

```text
None → malformed_input

123 → malformed_input

"" → empty_input

"   " → empty_input
```

---

## 12.3 Prompt Test Runner

The test runner performs the following flow:

```text
Load Test Cases
      ↓
Validate Input
      ↓
Measure Latency
      ↓
Record Prompt Version
      ↓
Record Model Version
      ↓
Record Validation Result
      ↓
Record Failure Reason
      ↓
Save JSON Result
      ↓
Print Summary
```

---

## 12.4 Actual Recorded Result

The prompt test result contained:

```text
Total Cases: 10
Passed: 6
Failed: 4
```

The four failed cases corresponded to malformed and empty input cases.

The important point is that these were validation outcomes, not an indication that the test runner itself crashed.

---

# DAY 5 — DOCUMENT PREPROCESSING

## 13.1 Objective

Day 5 was the transition from prompt engineering to document-based retrieval.

The objective was to prepare documents so that they could later be embedded and searched.

---

## 13.2 Document Loading

The loader reads Markdown files and creates document records.

Conceptually:

```text
Markdown File
      ↓
Read File
      ↓
Create Document ID
      ↓
Store Source Path
      ↓
Return Document
```

---

## 13.3 Text Cleaning

The cleaner handled:

- Line endings
- Extra spaces
- Multiple blank lines
- Formatting issues

This is important because poor text quality can affect later retrieval.

---

## 13.4 Chunking

A large document is divided into smaller sections.

The implementation supported:

```text
chunk_size
chunk_overlap
```

The default chunking implementation used a configurable chunk size and overlap.

---

## 13.5 Chunk Validation

The code checks that:

```text
chunk_size > 0
chunk_overlap >= 0
chunk_overlap < chunk_size
```

This prevents invalid chunk configurations.

---

## 13.6 Metadata

Each chunk receives metadata.

Example:

```json
{
  "chunk_id": "document_001_chunk_000",
  "doc_id": "document_001",
  "title": "Example Document",
  "source_path": "documents/example.md",
  "chunk_index": 0
}
```

This metadata later becomes useful for retrieval, evaluation and citations.

---

## 13.7 Actual Chunk Quality Result

The final recorded chunk-quality review showed:

```text
Documents processed : 30
Chunks created      : 60
Empty chunks        : 0
Duplicate chunk IDs : 0
Missing metadata    : 0
Minimum length      : 198
Maximum length      : 500
Average length      : 392.07
```

This provided a concrete checkpoint before moving to embeddings.

---

# DAY 6 — EMBEDDINGS AND VECTOR SEARCH

## 14.1 Objective

Day 6 introduced semantic retrieval.

The main idea was simple:

> Convert text into vectors and search for similar vectors.

---

## 14.2 Embedding Model

The project used:

```text
all-MiniLM-L6-v2
```

The embedding generation process used a batch size of:

```text
32
```

---

## 14.3 Why Embeddings?

Consider these two questions:

```text
How do I deploy a trained model?
```

and:

```text
What is needed before putting an ML model into production?
```

The wording is different.

However, the meaning can be related.

Semantic embeddings help represent the meaning of text so that related content can be retrieved even when the exact words are different.

---

## 14.4 ChromaDB

The generated vectors were stored in a ChromaDB collection:

```text
genai_documents
```

The retrieval system can then query the collection.

---

## 14.5 Search Flow

```text
User Question
      ↓
Question Embedding
      ↓
ChromaDB Search
      ↓
Relevant Chunks
      ↓
Distance / Score
      ↓
Ranked Results
```

The retrieval result contains information such as:

- Rank
- Chunk ID
- Text
- Metadata
- Distance

---

# DAY 7 — RAG INGESTION AND RETRIEVAL PIPELINE

## 15.1 Objective

Day 7 connected the previous components.

Instead of treating each script independently, the project started working as a RAG pipeline.

---

## 15.2 RAG Meaning

RAG stands for:

**Retrieval-Augmented Generation**

The basic idea is:

```text
Retrieve useful information
          +
Generate an answer using that information
```

The system does not depend only on the language model's internal knowledge.

It first retrieves relevant information from the project's document collection.

---

## 15.3 Ingestion Flow

```text
Documents
    ↓
Load
    ↓
Clean
    ↓
Chunk
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
```

---

## 15.4 Retrieval Flow

```text
Question
    ↓
Question Embedding
    ↓
Vector Search
    ↓
Relevant Chunks
    ↓
Context
```

---

## 15.5 Modular Design

The RAG implementation was separated into modules such as:

```text
src/rag/
├── ingest.py
├── retrieve.py
└── generate.py
```

This is better than placing the complete workflow into one large script.

Each module has a clear responsibility.

---

# DAY 8 — GROUNDED GENERATION, CITATIONS AND ABSTENTION

## 16.1 Objective

Day 8 addressed one of the most important GenAI problems:

> How do we prevent the assistant from answering beyond the evidence?

---

## 16.2 Grounded Generation

The grounded prompt tells the generation system:

```text
Use only the provided context.
Do not use outside knowledge.
Do not guess.
Do not invent facts.
Do not invent sources.
Only cite supplied chunk IDs.
```

This makes the retrieved documents the source of truth for the response.

---

## 16.3 Context Preparation

Retrieved chunks are converted into a context format such as:

```text
[document_001_chunk_000]

Document content...
```

Multiple chunks can then be provided as evidence.

---

## 16.4 Citation Mapping

The system validates that a citation refers to a chunk that was actually retrieved.

For example:

```text
Retrieved:
document_001_chunk_000
document_002_chunk_003
```

Valid:

```text
document_001_chunk_000
```

Invalid:

```text
document_099_chunk_002
```

because that chunk was not part of the retrieved evidence.

---

## 16.5 Abstention

Sometimes the required information is not present.

Instead of guessing, the system can return an abstention response.

Example:

```text
The answer cannot be determined from the provided documents.
```

This is an important behaviour for a reliable document assistant.

---

## 16.6 Structured Response

The project also introduced structured response objects containing fields such as:

- Answer
- Citations
- Grounded status
- Response status
- Sources

This makes the output easier for another application to consume.

---

# DAY 9 — BASELINE AND RETRIEVAL FAILURE DIAGNOSIS

## 17.1 Objective

Day 9 changed the focus from implementation to measurement.

The question was no longer:

> "Does the system work?"

The question became:

> "How well does the retrieval system work, and why does it fail?"

---

## 17.2 Baseline

A baseline was frozen before experiments were performed.

The recorded baseline included:

```text
Embedding model : all-MiniLM-L6-v2
Chunk size      : 500
Chunk overlap   : 50
Top-k           : 5
Filters         : none
Score threshold : 0.35
Prompt version  : v1
```

The report marked this configuration as:

```text
STATUS: BASELINE FROZEN
```

---

## 17.3 Weak Questions

Five weak questions were selected for diagnosis.

The project looked at reasons such as:

- Poor chunk boundary
- Vocabulary mismatch
- Broad query
- Missing metadata
- Ranking issue
- Excessive context

---

## 17.4 Important Debugging Finding

One important technical issue was identified around:

```text
doc_id
```

and:

```text
chunk_id
```

The stored retrieval identity was based on chunk-level IDs such as:

```text
document_001_chunk_000
```

while evaluation logic expected document-level identity.

This created a mapping problem.

The lesson was important:

> Document identity and chunk identity must be handled consistently throughout ingestion, retrieval and evaluation.

---

## 17.5 Controlled Experiment

The experiment changed:

```text
top-k = 5
```

to:

```text
top-k = 10
```

The result was:

| Metric | Baseline | Experiment | Change |
|---|---:|---:|---:|
| Recall | 0.9667 | 0.9667 | +0.0000 |
| Top-1 | 0.9667 | 0.9667 | +0.0000 |
| MRR | 0.9667 | 0.9667 | +0.0000 |

Therefore, increasing top-k alone did not improve the recorded result.

This was a useful lesson because an experiment should be accepted or rejected based on evidence.

---

# DAY 10 — RETRIEVAL OPTIMIZATION

## 18.1 Objective

Day 10 focused on finding a better retrieval configuration.

The project evaluated multiple approaches:

- Chunking changes
- Multi-query retrieval
- Reranking
- Configuration selection
- Before/after comparison

The project documentation specifically records these modules and evaluation areas.

---

# 18.2 Task 1 — Chunking Experiment

One configuration compared:

```text
Baseline
chunk_size = 1000
overlap = 200
top_k = 5
```

with:

```text
Experiment
chunk_size = 500
overlap = 100
top_k = 5
```

The purpose was to determine whether smaller chunks improved retrieval.

---

# 18.3 Task 2 — Multi-query Retrieval

Multi-query retrieval generates related versions of the user's question.

For example:

```text
Original:
How do I deploy a trained model?
```

Possible related queries:

```text
What is required for model deployment?
What are the steps before deploying an ML model?
How can a trained ML model be prepared for production?
```

The system can retrieve candidates for all of these queries and combine them.

However, the recorded experiment did not improve the main retrieval quality metric and increased latency.

Therefore, it was not selected as the final approach.

---

# 18.4 Task 3 — Reranking

The project also evaluated cross-encoder reranking using:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

The basic idea was:

```text
Initial Retrieval
       ↓
Top Candidate Chunks
       ↓
Cross Encoder
       ↓
Better Ranking
```

Reranking can improve ordering, but it also introduces additional processing time.

Therefore, both quality and latency need to be considered.

---

# 18.5 Task 4 — Best Configuration

The selected candidate was:

```text
SELECT_CANDIDATE
```

The reason recorded in the project was that the candidate improved retrieval performance without causing regressions in previously good questions.

---

# 18.6 Task 5 — Before and After

The final recorded comparison covered:

```text
30 questions
```

The results were:

| Metric | Before | After | Improvement |
|---|---:|---:|---:|
| Retrieval Recall | 0.8000 | 0.8667 | +0.0667 |
| Top-1 Accuracy | 0.6000 | 0.6333 | +0.0333 |
| MRR | 0.6700 | 0.7117 | +0.0417 |
| Average Latency | 1.23 ms | 1.17 ms | -0.06 ms |

The recorded output therefore showed improvement in retrieval quality as well as a small reduction in average measured latency.

---

# 19. EACH DAY — TASK AND IMPLEMENTATION SUMMARY

| Day | Main Focus | Main Outcome |
|---|---|---|
| Day 1 | Classification | Controlled document classification prompt |
| Day 2 | Extraction | Structured field extraction |
| Day 3 | Summarization | Concise summary and prompt versioning |
| Day 4 | Validation | Test cases and input validation |
| Day 5 | Preprocessing | Clean chunks with metadata |
| Day 6 | Embeddings | Vector-based semantic search |
| Day 7 | RAG | Ingestion and retrieval pipeline |
| Day 8 | Grounding | Evidence-based responses |
| Day 9 | Evaluation | Baseline and failure diagnosis |
| Day 10 | Optimization | Retrieval experiments and configuration selection |

This progression is the central story of the project.

---

# 20. CODE / MODULE EXPLANATION

## 20.1 Day 1–4 Structure

```text
prompts/
data/
datasets/
scripts/
tests/
results/
safety/
voice/
```

The first four days focused primarily on prompts, validation and testing.

---

## 20.2 Preprocessing Modules

```text
src/preprocessing/
├── loader.py
├── cleaner.py
├── chunker.py
└── metadata.py
```

### loader.py

Responsible for reading documents.

### cleaner.py

Responsible for cleaning the text.

### chunker.py

Responsible for dividing text into chunks.

### metadata.py

Responsible for generating chunk metadata.

---

# 21. CODE EXPLANATION — CHUNKING

The chunking function validates its configuration before processing.

Conceptually:

```python
if chunk_size <= 0:
    raise ValueError("chunk_size must be greater than 0")

if chunk_overlap < 0:
    raise ValueError("chunk_overlap cannot be negative")

if chunk_overlap >= chunk_size:
    raise ValueError(
        "chunk_overlap must be smaller than chunk_size"
    )
```

The reason for these checks is simple.

If the chunk size is zero, no meaningful chunk can be created.

If the overlap is negative, the configuration does not make sense.

If the overlap is equal to or greater than the chunk size, the algorithm cannot move through the text correctly.

---

# 22. CODE EXPLANATION — METADATA

The metadata structure contains:

```python
{
    "chunk_id": "...",
    "doc_id": "...",
    "title": "...",
    "source_path": "...",
    "updated_at": "...",
    "chunk_index": 0
}
```

This information helps answer questions such as:

- Which document did this chunk come from?
- Which chunk is this?
- Where was the original document stored?
- What was the chunk order?

This later became important during the Day 9 evaluation diagnosis.

---

# 23. CODE EXPLANATION — EMBEDDINGS

The embedding stage used:

```python
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 32
```

The model converts text into numerical vectors.

The process is:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

The question is converted in the same way:

```text
Question
 ↓
Embedding Model
 ↓
Question Vector
```

The system then compares the question vector with stored document vectors.

---

# 24. CODE EXPLANATION — RAG

The RAG process can be simplified as:

```text
Question
   ↓
Retrieve evidence
   ↓
Build context
   ↓
Give context to generation
   ↓
Generate answer
```

The important point is that retrieval happens before generation.

The system is therefore not simply asking the model:

> "Answer this question."

Instead, it is asking:

> "Here is the relevant evidence. Answer the question using this evidence."

---

# 25. TESTING & VALIDATION

Testing was an important part of the project.

The project used:

```text
Pytest
```

and dedicated runtime scripts.

The project also contains dedicated test modules for areas such as:

- Abstention
- Citation mapping
- Grounded generation
- Grounded prompts
- Response schema
- RAG pipeline
- Baseline evaluation
- Retrieval diagnosis
- Chunking
- Multi-query retrieval
- Reranking
- Configuration selection
- Before/after evaluation

---

# 26. VERIFIED DAY 1–4 TEST RESULT

The verified test execution was:

```text
python -m pytest -q
```

Result:

```text
......... [100%]
9 passed in 0.08s
```

This result is directly reported rather than estimated.

---

# 27. LATER-STAGE TESTING

The later project stages contain extensive test files.

However, the later RAG suite should not be represented as having a successful full-suite result unless the environment has all required dependencies installed.

A clean-environment verification attempt was blocked because:

```text
chromadb
```

was missing.

Therefore, the professional report records this as a dependency/environment issue rather than incorrectly claiming a successful test run.

This distinction is important in an office report.

---

# 28. ACTUAL OUTPUTS

The project generated multiple output artifacts.

Important examples include:

```text
results/prompt_test_results.json

outputs/chunk_quality_review.md
outputs/ingestion_events.jsonl

outputs/embeddings.npz
outputs/chroma_db/

outputs/baseline_report.txt
outputs/controlled_experiment_results.json
outputs/day09_final_report.json
outputs/retrieval_failure_diagnosis.json

outputs/day10_task2_multi_query_results.json
outputs/day10/task3/reranking_results.json
outputs/day10_task4_best_configuration.json
outputs/day10_task5_before_after_report.txt
outputs/day10_task5_before_after_report.json
```

These files provide evidence of the implementation and evaluation process.

---

# 29. ACTUAL OUTPUTS / SCREENSHOTS

For the final office report, screenshots should be inserted from the actual project environment.

## Screenshot 1 — Day 1–4 Pytest

```text
[INSERT ACTUAL TERMINAL SCREENSHOT]
```

Recommended screenshot:

```text
python -m pytest -q
......... [100%]
9 passed in 0.08s
```

---

## Screenshot 2 — Prompt Test Result

```text
[INSERT prompt_test_results.json SCREENSHOT]
```

---

## Screenshot 3 — Day 5 Chunk Quality

```text
[INSERT chunk_quality_review.md SCREENSHOT]
```

The screenshot should show:

```text
30 documents
60 chunks
0 empty chunks
0 duplicate IDs
0 missing metadata
```

---

## Screenshot 4 — Day 6 Semantic Search

```text
[INSERT ACTUAL SEMANTIC SEARCH SCREENSHOT]
```

---

## Screenshot 5 — Day 8 Grounded Response

```text
[INSERT ACTUAL GROUNDED RESPONSE SCREENSHOT]
```

---

## Screenshot 6 — Day 9 Baseline

```text
[INSERT baseline_report.txt SCREENSHOT]
```

---

## Screenshot 7 — Day 10 Before/After

```text
[INSERT day10_task5_before_after_report.txt SCREENSHOT]
```

No artificial screenshots should be used.

---

# 30. RESULTS

## 30.1 Overall Result

The project successfully progressed through the major stages required for a basic document-oriented GenAI/RAG workflow.

The major results were:

- Prompt classification implemented.
- Information extraction implemented.
- Summarization implemented.
- Prompt versioning established.
- Input validation implemented.
- Prompt testing implemented.
- Document preprocessing implemented.
- Chunking implemented.
- Metadata implemented.
- Embeddings implemented.
- ChromaDB indexing implemented.
- Semantic search implemented.
- RAG ingestion implemented.
- RAG retrieval implemented.
- Grounded generation implemented.
- Citation validation implemented.
- Abstention implemented.
- Retrieval baseline created.
- Retrieval failures diagnosed.
- Retrieval experiments performed.
- Final candidate selected based on measured results.

---

# 31. DAY 5 RESULT

The final chunk-quality review recorded:

```text
Documents processed : 30
Chunks created      : 60
Empty chunks        : 0
Duplicate IDs       : 0
Missing metadata    : 0
Average chunk length: 392.07
```

This indicates that the final reviewed preprocessing output was ready for the next retrieval stage.

---

# 32. DAY 9 RESULT

The top-k experiment showed:

```text
Recall : 0.9667 → 0.9667
Top-1  : 0.9667 → 0.9667
MRR    : 0.9667 → 0.9667
```

Therefore:

> Increasing top-k alone did not solve the identified retrieval problem.

This was an important negative result.

A negative result is still useful because it prevents the team from selecting an ineffective configuration.

---

# 33. DAY 10 RESULT

The selected configuration produced:

```text
Recall : 0.8000 → 0.8667
Top-1  : 0.6000 → 0.6333
MRR    : 0.6700 → 0.7117
```

The recorded comparison also showed:

```text
Average Latency:
1.23 ms → 1.17 ms
```

The project selected the candidate because it improved retrieval performance without regression among previously good questions.

---

# 34. CHALLENGES FACED & SOLUTIONS

## Challenge 1 — Invalid Input

### Problem

The system could receive:

```text
None
123
""
"   "
```

### Solution

Input validation was introduced.

---

## Challenge 2 — Prompt Changes

### Problem

Changing a prompt can make it difficult to know which version produced a result.

### Solution

Prompt versioning was introduced:

```text
v1
v2
```

---

## Challenge 3 — Document Formatting

### Problem

Raw documents can contain inconsistent whitespace and formatting.

### Solution

A cleaning module was introduced.

---

## Challenge 4 — Chunk Configuration

### Problem

Invalid chunk size or overlap could break the chunking logic.

### Solution

Validation rules were added.

---

## Challenge 5 — Traceability

### Problem

After retrieval, the system must know where a chunk came from.

### Solution

Chunk metadata was introduced.

---

## Challenge 6 — Retrieval Failure

### Problem

Some questions were not correctly associated with their expected source documents.

### Solution

The project diagnosed the difference between:

```text
doc_id
```

and:

```text
chunk_id
```

and identified the mapping issue.

---

## Challenge 7 — Top-k Did Not Improve Retrieval

### Problem

Increasing top-k did not improve the recorded metrics.

### Solution

The experiment was measured and not selected as the solution.

---

## Challenge 8 — Multi-query Increased Latency

### Problem

Multi-query retrieval introduced additional processing.

### Solution

Quality and latency were compared before selecting it.

---

## Challenge 9 — Reranking Latency

### Problem

Cross-encoder reranking can add significant processing time.

### Solution

Reranking was evaluated as a trade-off rather than automatically accepted.

---

# 35. SECURITY / GUARDRAILS

Because this was a training project, security work was focused on application-level GenAI safeguards.

## 35.1 Input Validation

Invalid and empty inputs are identified before normal processing.

---

## 35.2 Grounded Responses

The grounded prompt instructs the system to use only the provided evidence.

---

## 35.3 No Guessing

The system is instructed not to:

- Guess
- Invent facts
- Invent sources
- Make unsupported assumptions

---

## 35.4 Citation Validation

Citations must correspond to retrieved chunks.

---

## 35.5 Abstention

If sufficient evidence is not available, the system can return an abstention response.

These controls represent basic responsible GenAI application practices within the scope of the training project.

---

# 36. GIT & GITHUB

Git was used to manage the project development.

The project was divided into development branches so that different training stages could be maintained separately.

The GitHub repository is:

[GenAI Assistant GitHub Repository](https://github.com/Dhanushkumar-stackly/genai-assistant?utm_source=chatgpt.com)

The default branch is:

```text
main
```

---

# 37. GIT BRANCHES

The relevant Day 1–10 branches are:

```text
main
│
├── day-1-4
├── day-5-8
└── day-09
```

## day-1-4

Contains the first four days of prompt engineering, validation and testing.

## day-5-8

Contains preprocessing, embeddings, vector retrieval, RAG and grounded-generation work.

## day-09

Contains baseline evaluation, retrieval diagnosis and controlled experiments.

## main

Contains the integrated project history.

There is no separate verified `day-10` branch in the repository branch list, so the report does not invent one.

---

# 38. GIT & VERSION CONTROL WORKFLOW

The development workflow was:

```text
Create Day Branch
        ↓
Create Files / Folders
        ↓
Implement Task
        ↓
Run Application
        ↓
Run Tests
        ↓
Verify Actual Output
        ↓
Git Add
        ↓
Git Commit
        ↓
Push Day Branch
        ↓
Checkout Main
        ↓
Pull Main
        ↓
Merge Day Branch
        ↓
Push Main
```

This gives a clear relationship between:

```text
Task
 ↓
Code
 ↓
Test
 ↓
Output
 ↓
Commit
 ↓
Branch
 ↓
Main
```

---

# 39. TYPICAL GIT COMMANDS

```bash
git status
```

Check the current repository status.

```bash
git add .
```

Stage the changes.

```bash
git commit -m "Day work completed"
```

Create a commit.

```bash
git push origin <day-branch>
```

Push the Day branch.

Then:

```bash
git checkout main
git pull origin main
git merge <day-branch>
git push origin main
```

This keeps the main branch synchronized with completed training work.

---

# 40. REQUIREMENTS / INSTALLATION

## Step 1 — Create Virtual Environment

```bash
python -m venv venv
```

---

## Step 2 — Activate Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

For the Day 5–8 RAG environment, the documented dependencies include:

```bash
pip install numpy chromadb sentence-transformers pydantic scikit-learn python-dotenv pytest
```

The project documentation records these installation commands.

---

# 41. DAY 5 COMMANDS

```bash
python .\scripts\generate_documents.py
python .\scripts\preprocess_documents.py
python .\scripts\inspect_chunks.py
```

---

# 42. DAY 6 COMMANDS

```bash
python .\scripts\generate_embeddings.py
python .\scripts\build_vector_index.py
python .\scripts\semantic_search.py
python .\scripts\search_with_filters.py
python .\scripts\evaluate_retrieval.py
```

---

# 43. DAY 7 COMMANDS

```bash
python .\src\rag\ingest.py
python .\src\rag\retrieve.py
python .\scripts\run_rag.py
python .\scripts\test_rag_pipeline.py
```

---

# 44. DAY 8 COMMANDS

```bash
python .\src\rag\demo_grounded_prompt.py
python .\src\rag\demo_citation_mapper.py
python .\src\rag\demo_abstention.py
python .\src\rag\demo_response_schema.py
python .\src\rag\demo_grounded_generation.py
```

These commands are documented in the project materials.

---

# 45. REQUIREMENTS FILE OBSERVATION

One important repository-cleanliness issue was identified.

The archived Day 1–4 `requirements.txt` contains an unresolved Git merge conflict:

```text
<<<<<<< HEAD
...
=======
...
>>>>>>> ...
```

For a final office submission, this should be resolved.

The final file should contain only the intended dependencies.

The Day 5–8 archive also contains a virtual environment.

A virtual environment should not normally be committed to GitHub.

Instead:

```text
requirements.txt
```

should describe the dependencies required to recreate the environment.

---

# 46. PROJECT DOCUMENTATION

The project contains documentation for the different stages.

```text
Day 1–4
README.md

Day 5
README_Day05.md

Day 6
README_Day06.md

Day 7
README_Day07.md

Day 8
README_Day08.md

Day 9
README_Day09.md

Day 10
README_Day10.md
```

Additional documentation includes:

```text
REQUIREMENTS.md
DAY9-10_TERMINAL_COMMANDS.md
requirements.txt
```

The README documentation is important because it explains how to run and verify each stage.

---

# 47. PROJECT OUTPUT REGISTER

| Output | Purpose |
|---|---|
| prompt_test_results.json | Prompt validation results |
| chunk_quality_review.md | Chunk quality statistics |
| ingestion_events.jsonl | Ingestion event history |
| embeddings.npz | Embedding output |
| chroma_db | Vector database |
| baseline_report.txt | Day 9 baseline |
| controlled_experiment_results.json | Controlled experiment |
| retrieval_failure_diagnosis.json | Failure analysis |
| day10_task2_multi_query_results.json | Multi-query evaluation |
| reranking_results.json | Reranking evaluation |
| day10_task4_best_configuration.json | Selected configuration |
| day10_task5_before_after_report.txt | Final comparison |

---

# 48. WHAT THE PROJECT ACHIEVED END TO END

At the beginning of the project, the work was mainly about writing prompts.

By the end of Day 10, the project had reached a much broader workflow.

The project could be explained as:

```text
We start with documents.
        ↓
We clean the documents.
        ↓
We divide them into chunks.
        ↓
We attach metadata.
        ↓
We convert chunks into embeddings.
        ↓
We store them in a vector database.
        ↓
A user asks a question.
        ↓
The question is converted into an embedding.
        ↓
Relevant document chunks are retrieved.
        ↓
The evidence is checked.
        ↓
The response is generated using the evidence.
        ↓
Citations are validated.
        ↓
If evidence is insufficient, the system can abstain.
        ↓
Retrieval quality is measured.
        ↓
Weak areas are diagnosed.
        ↓
Experiments are performed.
        ↓
The better configuration is selected.
```

That is the complete end-to-end story of the ten-day training project.

---

# 49. WHAT WAS LEARNED FROM THE PROJECT

The project provided practical learning in several areas.

## Prompt Engineering

A prompt should clearly explain:

- What the model should do.
- What the output should look like.
- What the model should not do.

## Data Preparation

Good retrieval starts with good document preparation.

## Embeddings

Text can be represented as vectors so that semantic similarity can be measured.

## Vector Search

A vector database allows relevant content to be retrieved efficiently.

## RAG

Retrieval can provide external evidence to a generation process.

## Grounding

The response should be tied to retrieved evidence.

## Evaluation

A system should be measured rather than judged only by a few examples.

## Experimentation

Changing a parameter does not automatically mean the system improved.

## Version Control

Git makes the development process traceable.

---

# 50. CONCLUSION

The first ten days of the GenAI Assistant Training Project provided a practical introduction to building a document-based Generative AI workflow.

The project started with simple prompt-engineering tasks.

Classification was implemented first.

Information extraction followed.

Summarization and prompt versioning were then introduced.

Testing and validation were added to make the prompt behaviour measurable.

The project then moved into document processing.

Documents were loaded, cleaned, divided into chunks and enriched with metadata.

After that, embeddings and vector search were introduced using Sentence Transformers and ChromaDB.

The retrieval components were then connected into a RAG workflow.

The next stage focused on reliability.

Grounded prompts were introduced so that responses would use supplied evidence.

Citation mapping helped connect answers back to retrieved chunks.

Abstention provided a way to handle questions where the documents did not provide enough information.

The final two days focused on evaluation.

A baseline was created.

Weak questions were identified.

Retrieval failures were investigated.

Controlled experiments were performed.

Different retrieval strategies were compared.

The final recorded Day 10 comparison showed an improvement in retrieval recall, top-1 accuracy and MRR.

The project therefore demonstrates the complete learning path from:

```text
Prompt
   ↓
Data
   ↓
Retrieval
   ↓
Generation
   ↓
Evaluation
   ↓
Optimization
```

From a training perspective, the most important outcome was not only that individual modules were implemented, but that the relationship between those modules became clear.

The project showed how a GenAI assistant can be developed incrementally, tested at each stage, evaluated using measurable results and maintained using version control.

---

# 51. FUTURE ENHANCEMENTS

The following improvements can be considered for future stages.

## 51.1 Hybrid Search

Combine:

```text
Keyword Search
+
Semantic Search
```

This can help when exact terminology is important.

---

## 51.2 Better Query Rewriting

The system could automatically rewrite user questions into clearer retrieval queries.

---

## 51.3 Advanced Reranking

More reranking strategies could be evaluated while controlling latency.

---

## 51.4 Larger Evaluation Dataset

The retrieval evaluation could be expanded from the current training dataset to a much larger and more diverse set of questions.

---

## 51.5 Evaluation Dashboard

A dashboard could display:

- Recall
- Top-1
- MRR
- Latency
- Failure categories
- Experiment comparison

---

## 51.6 User Interface

The RAG workflow could later be connected to a web interface.

---

## 51.7 Voice Integration

The project already contains voice/audio scaffolding in the early project structure. A future stage could connect this to speech input and output.

---

## 51.8 Production Deployment

A future production-oriented phase could introduce:

- Authentication
- Authorization
- API security
- Logging
- Monitoring
- Model management
- Database management
- Deployment infrastructure

These are future enhancements and are not presented as completed Day 1–10 functionality.

---

# 52. REFERENCES

## Project Repository

[GenAI Assistant GitHub Repository](https://github.com/Dhanushkumar-stackly/genai-assistant?utm_source=chatgpt.com)

## Project Documentation

```text
README.md
README_Day05.md
README_Day06.md
README_Day07.md
README_Day08.md
README_Day09.md
README_Day10.md
```

## Additional Documentation

```text
REQUIREMENTS.md
DAY9-10_TERMINAL_COMMANDS.md
requirements.txt
```

## Project Evidence

The report is supported by:

- Source code
- Test files
- Runtime scripts
- JSON output files
- Chunk quality reports
- Retrieval evaluation reports
- Experiment results
- Git branch history
- GitHub repository

---

# 53. FINAL OFFICE PRESENTATION SUMMARY

If this project needs to be explained to a manager or reviewer in a short form, the project can be described as follows:

> The GenAI Assistant Training Project was developed as a ten-day practical learning project. It started with prompt engineering tasks such as classification, extraction and summarization. The project then moved into document preprocessing, where documents were cleaned, chunked and given metadata. These chunks were converted into embeddings and stored in ChromaDB for semantic retrieval. The retrieval process was then connected to a RAG workflow. Grounded generation, citation validation and abstention were added to improve response reliability. During the final stages, retrieval quality was measured using recall, top-1 accuracy and MRR. Weak retrieval cases were diagnosed and multiple configurations were tested. The final recorded Day 10 comparison showed measurable improvement in retrieval performance. Git and GitHub were used throughout the project to maintain development history and branch-based implementation.

---

# 54. FINAL PROJECT FLOW

```text
                 GENAI ASSISTANT
                       │
                       ▼
              ┌─────────────────┐
              │ Prompt Design   │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Input Validation│
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Document Input  │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Text Cleaning   │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Chunking        │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Metadata        │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Embeddings      │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ ChromaDB        │
              └────────┬────────┘
                       │
                       │
                USER QUESTION
                       │
                       ↓
              ┌─────────────────┐
              │ Query Embedding │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Semantic Search │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Relevant Chunks │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Evidence Check  │
              └───────┬─┬───────┘
                      │ │
          Enough ─────┘ └──── Not Enough
             │                   │
             ↓                   ↓
      Grounded Context       Abstention
             │
             ↓
      Answer Generation
             │
             ↓
      Citation Mapping
             │
             ↓
     Structured Response
             │
             ↓
       Evaluation
             │
             ↓
      Experimentation
             │
             ↓
    Better Configuration
```

# END OF DAY 1–10 REPORT

**Project:** GenAI Assistant Training Project  
**Coverage:** Day 1 – Day 10  
**Focus:** Prompt Engineering → RAG → Evaluation → Optimization