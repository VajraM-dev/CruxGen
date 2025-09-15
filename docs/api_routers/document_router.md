# Document Management API

MinIO-based document storage and management endpoints.

## Endpoints

### Create Bucket
```
POST /document/create-bucket
```
Creates a new MinIO bucket.

**Request Body:**
```json
{
  "bucket_name": "string"
}
```

**Response:** `APIOutputResponse`

### Upload File
```
POST /document/upload-file
```
Uploads a file to MinIO bucket and registers it in the database.

**Parameters:**
- `file`: UploadFile (multipart/form-data)
- `bucket_name`: string (default: "default-bucket")

**Response:** `APIOutputResponse` with `file_id` in response field

**Notes:**
- Checks for existing files in database
- Creates database record
- Uses temporary file storage during upload

### Delete Object
```
DELETE /document/delete-object
```
Deletes object from MinIO and removes all associated database records.

**Request Body:**
```json
{
  "bucket_name": "string",
  "object_name": "string"
}
```

**Response:** `APIOutputResponse`

**Notes:**
- Removes QA pairs, chunks, and file records from database
- Deletes object from MinIO storage

### Delete Bucket
```
DELETE /document/delete-bucket
```
Deletes a MinIO bucket.

**Request Body:**
```json
{
  "bucket_name": "string"
}
```

**Response:** `APIOutputResponse`

### List Objects
```
GET /document/list-objects
```
Lists objects in a MinIO bucket.

**Query Parameters:**
- `bucket_name`: string (optional)
- `prefix`: string (optional)
- `recursive`: boolean (default: false)

**Response:** `APIOutputResponse` with object list

### List Buckets
```
POST /document/list-buckets
```
Lists all MinIO buckets.

**Response:** `APIOutputResponse` with bucket list

### Get Object Info
```
GET /document/get-object-info
```
Retrieves metadata for a specific object.

**Query Parameters:**
- `bucket_name`: string (required)
- `object_name`: string (required)

**Response:** `APIOutputResponse` with object metadata

### Get File ID
```
GET /document/get_file_id_from_name
```
Retrieves file ID from database using filename.

**Query Parameters:**
- `file_name`: string (required)

**Response:** `APIOutputResponse` with `file_id`

## Error Handling

All endpoints return standardized error responses:
- `400`: Bad Request
- `404`: Not Found  
- `500`: Internal Server Error

## Dependencies

- MinIO for object storage
- Database for file metadata
- Temporary file handling for uploads