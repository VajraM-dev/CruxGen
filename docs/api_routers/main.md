# CruxGen API

Create LLM-ready datasets. Straight from the source.

## Overview

FastAPI application for document processing, chunking, and QA pair generation for LLM training datasets.

## Base URL
```
http://localhost:8000
```

## Core Endpoints

### Root
```
GET /
```
Returns basic API greeting.

**Response:**
```json
{
  "Hello": "World"
}
```

### Health Check
```
GET /health
```
Comprehensive system health status.

**Response:**
- `200`: All systems operational
- `500`: System failure

**Checks:**
- Vault connection
- Database connection  
- MinIO connection

**Response Format:**
```json
{
  "status": "ok|error",
  "message": "error details (if any)"
}
```

## API Routes

### Document Management
```
/document/*
```
MinIO-based file storage and management.
- Upload/delete files
- Bucket operations
- Object metadata

### Chunk Management  
```
/chunks/*
```
Document chunking operations.
- Create chunks from documents
- Delete/retrieve chunks
- Chunk configuration

### QA Management
```
/qa/*
```
Question-Answer pair generation.
- Process chunks to QA pairs
- Export QA datasets
- QA pair management

## Dependencies

**Core Stack:**
- FastAPI 0.116.1+
- SQLAlchemy 2.0.43+
- MinIO 7.2.16+
- Uvicorn 0.35.0+

**LLM Processing:**
- OpenAI 1.102.0+
- LangChain Docling 1.0.0+
- LangChain Text Splitters 0.3.9+

**Infrastructure:**
- PostgreSQL (psycopg2 2.9.10+)
- HashiCorp Vault (hvac 2.3.0+)
- Tenacity 9.1.2+ (retry logic)

**Utilities:**
- Python Multipart 0.0.20+
- Python DotEnv 1.1.1+
- PyFuncMonitor 0.1.2+

## Configuration

**Python:** 3.11+

**Environment Variables:**
- Database connection details
- Vault configuration  
- MinIO credentials
- OpenAI API keys

## Running

```bash
python main.py
```

**Server Details:**
- Host: 0.0.0.0
- Port: 8000
- Auto-reload: Enabled in development