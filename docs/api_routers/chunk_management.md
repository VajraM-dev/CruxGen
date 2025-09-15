# Chunk Management API

Document chunking and chunk management endpoints.

## Endpoints

### Create Chunks
```
POST /chunks/create-chunks
```
Creates chunks from a document stored in MinIO.

**Request Body:**
```json
{
  "file_id": "string",
  "bucket_name": "string"
}
```

**Response:** `APIOutputResponse` with chunk creation results

**Notes:**
- Uses `DocumentSplitter` with default `ChunkerConfig`
- Loads document from MinIO and splits into chunks
- Stores chunks in database

### Delete Chunks
```
DELETE /chunks/delete-chunks
```
Deletes all chunks associated with a file ID.

**Request Body:**
```json
{
  "file_id": "string"
}
```

**Response:** `APIOutputResponse` with deletion count

### Get Chunks
```
GET /chunks/get-chunks
```
Retrieves all chunks for a specific file.

**Query Parameters:**
- `file_id`: string (required)

**Response:** `APIOutputResponse` with array of chunk texts

## Error Handling

All endpoints return standardized error responses:
- `400`: Bad Request
- `500`: Internal Server Error

## Dependencies

- `DocumentSplitter` for chunk creation
- Database for chunk storage and retrieval
- MinIO for document access