# CruxGen

Create LLM-ready datasets. Straight from the source.

## What is CruxGen?

CruxGen automates the creation of synthetic question-answer datasets from your company's unstructured documents. Upload PDFs and DOCX files, and let AI generate contextually relevant Q&A pairs ready for LLM training.

**Problem**: Creating training datasets manually is time-intensive and expensive.  
**Solution**: Automated pipeline that processes documents and generates structured Q&A pairs.

## Key Features

- **Document Processing**: Upload and manage PDF/DOCX files
- **Intelligent Chunking**: Automatically split documents into meaningful segments
- **QA Generation**: Generate contextual question-answer pairs using LLM
- **Export Ready**: Download datasets in JSONL format for training
- **Enterprise Ready**: Vault integration, PostgreSQL storage, MinIO object storage

## Quick Start

### 1. Install the SDK

```bash
pip install cruxgen-sdk
```

### 2. Process Your First Document

```python
from cruxgen_sdk import CruxGenSDK

with CruxGenSDK("http://localhost:8000") as sdk:
    # Upload document
    result = sdk.upload_file("company-policy.pdf")
    file_id = result["response"]
    
    # Create chunks
    sdk.create_chunks(file_id, "default-bucket")
    
    # Generate QA pairs
    sdk.create_qa_pairs(file_id)
    
    # Export dataset
    qa_data = sdk.get_qa_pairs(file_id, generate_jsonl=True)
    with open("training_data.jsonl", "wb") as f:
        f.write(qa_data)
```

### 3. Use Your Dataset

The generated JSONL file contains structured Q&A pairs ready for LLM training:

```json
{"question": "What is the company's remote work policy?", "answer": "Employees may work remotely up to 3 days per week..."}
{"question": "How do I submit vacation requests?", "answer": "Vacation requests must be submitted through the HR portal..."}
```

## Architecture

CruxGen follows a modular pipeline architecture:

1. **Document Storage** → MinIO object storage
2. **Document Chunking** → Docling text splitters
3. **QA Generation** → OpenAI API processing
4. **Data Management** → PostgreSQL with SQLAlchemy
5. **API Layer** → FastAPI with automatic documentation

## API Components

### Core Services

- **[Main Application](api_routers/main.md)** - FastAPI server with health checks
- **[Document Management](api_routers/document_router.md)** - File upload, storage, and metadata
- **[Chunk Management](api_routers/chunk_management.md)** - Document splitting and chunk operations
- **[QA Management](api_routers/qa_management.md)** - Question-answer pair generation

### Client SDK

- **[Python SDK](sdk.md)** - Complete SDK for CruxGen API

## Dependencies

**Core Stack:**

- FastAPI 0.116.1+ (API framework)
- SQLAlchemy 2.0.43+ (database ORM)
- MinIO 7.2.16+ (object storage)
- PostgreSQL (primary database)

**LLM Processing:**

- Litellm (llm management)

**Infrastructure:**

- HashiCorp Vault (secrets management)
- Tenacity 9.1.2+ (retry logic)
- Python 3.11+ required

## Getting Started

### Prerequisites

1. **Database**: PostgreSQL instance
2. **Object Storage**: MinIO server
3. **Secrets**: HashiCorp Vault
4. **LLM API**: OpenAI API key

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/cruxgen
cd cruxgen

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Start server
python main.py
```

### Health Check

Verify all systems are operational:

```bash
curl http://localhost:8000/health
```

## Workflow

### Document to Dataset Pipeline

1. **Upload** documents (PDF/DOCX) to MinIO storage
2. **Process** files into database-tracked chunks
3. **Generate** Q&A pairs using LLM processing
4. **Export** structured datasets for training

### Typical Usage Pattern

```python
# 1. Document Management
sdk.create_bucket("documents")
result = sdk.upload_file("manual.pdf", "documents")
file_id = result["response"]

# 2. Content Processing
sdk.create_chunks(file_id, "documents")
chunks = sdk.get_chunks(file_id)

# 3. Dataset Generation
sdk.create_qa_pairs(file_id)
dataset = sdk.get_qa_pairs(file_id, generate_jsonl=True)

# 4. Export and Use
with open("training_set.jsonl", "wb") as f:
    f.write(dataset)
```