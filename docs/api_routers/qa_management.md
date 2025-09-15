# QA Management API

Question-Answer pair generation and management endpoints.

## Endpoints

### Process Chunks to QA
```
POST /qa/process-chunks-to-qa
```
Generates QA pairs from document chunks.

**Request Body:**
```json
{
  "file_id": "string",
  "chunk_id": "string (optional)"
}
```

**Response:** `APIOutputResponse` with QA generation results

**Notes:**
- Processes all chunks for the file if `chunk_id` not provided
- Generates QA pairs using LLM processing
- Stores QA pairs in database

### Delete QA Pairs
```
DELETE /qa/delete-qa-pairs
```
Deletes all QA pairs associated with a file.

**Request Body:**
```json
{
  "file_id": "string"
}
```

**Response:** `APIOutputResponse` with deletion results

### Get QA Pairs
```
GET /qa/get-qa-pairs/{file_id}
```
Retrieves all QA pairs for a specific file.

**Path Parameters:**
- `file_id`: string (required)

**Query Parameters:**
- `generate_jsonl`: boolean (default: false)

**Response:** 
- If `generate_jsonl=false`: `APIOutputResponse` with QA pairs array
- If `generate_jsonl=true`: JSONL file download (`application/jsonl`)

**Notes:**
- JSONL download includes filename: `qa_pairs_{file_id}.jsonl`
- Each line in JSONL contains a single QA pair object

## Error Handling

All endpoints return standardized error responses:
- `400`: Bad Request
- `500`: Internal Server Error

## Dependencies

- LLM processing pipeline for QA generation
- Database for QA pair storage and retrieval
- Chunk data for QA generation