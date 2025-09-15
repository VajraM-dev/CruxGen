# CruxGen

[![Documentation](https://img.shields.io/badge/Documentation-8A2BE2)](https://vajram-dev.github.io/CruxGen/index.html)

Transform your internal documents into high-quality Q&A datasets for LLM training.

## What is CruxGen?

CruxGen automates the creation of synthetic question-answer datasets from your company's unstructured documents. Upload PDFs and DOCX files, and let AI generate contextually relevant Q&A pairs ready for LLM training.

**Problem**: Creating training datasets manually is time-intensive and expensive.  
**Solution**: Automated pipeline that processes documents and generates structured Q&A pairs.

## Key Features

- **Document Processing**: Upload and manage PDF/DOCX files
- **Intelligent Chunking**: Automatically splits documents into processable segments
- **AI-Powered Generation**: Creates contextual Q&A pairs using advanced LLMs
- **Export Ready**: Output in JSON/JSONL formats for immediate use
- **Scalable Storage**: Built on MinIO for handling large document collections

## How It Works

```
Your Documents → Upload → Chunk → AI Processing → Q&A Dataset
```

1. **Upload** your internal documents (PDFs, DOCX)
2. **Process** documents into manageable chunks
3. **Generate** Q&A pairs using context-aware AI
4. **Export** structured datasets for training

## Quick Start

### Installation
```bash
uv pip install -r requirements.txt
```

### Run Server
```bash
python main.py
```
Server available at `http://localhost:8000`

### Basic Workflow

1. **Upload Document**
   - POST to `/document/upload-file`
   - Specify bucket and upload your file

2. **Create Chunks**
   - POST to `/chunks/create-chunks`
   - System intelligently segments your document

3. **Generate Q&A Pairs**
   - POST to `/qa/process-chunks-to-qa`
   - AI creates contextual question-answer pairs

4. **Export Dataset**
   - GET `/qa/get-qa-pairs/{file_id}`
   - Download as JSON or JSONL format

## Tech Foundation

Built with enterprise-grade components:
- **FastAPI** for robust API framework
- **SQLAlchemy** for reliable data persistence
- **MinIO** for scalable object storage
- **Pydantic** for data validation
- **HashiCorp Vault** for secure configuration

## Health Monitoring

Check system status at `/health` - validates database, storage, and configuration services.

## Use Cases

- **Training Data Creation**: Generate datasets for domain-specific LLM fine-tuning
- **Knowledge Base Enhancement**: Convert documentation into Q&A format
- **Content Standardization**: Ensure consistent question-answer formatting
- **Rapid Prototyping**: Quickly create training data for AI experiments

Ready to transform your documents into training gold.