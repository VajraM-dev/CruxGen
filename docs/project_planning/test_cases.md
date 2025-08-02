

| Test Case ID | Component | Test Description | Expected Result | Type |
| :---- | :---- | :---- | :---- | :---- |
| TC-001 | PDF Extractor | Process a standard, text-based PDF file. | Text is extracted correctly with minimal formatting loss. | Happy Path |
| TC-002 | DOCX Extractor | Process a standard .docx file with paragraphs and headings. | Text is extracted in the correct order. | Happy Path |
| TC-003 | End-to-End | Drop a valid PDF into MinIO, run the pipeline, check for Q\&A in DB. | Master table contains new Q\&A entries linked to the new document. | Integration |
| TC-004 | JSON Export | Run the export function on a populated database. | A valid JSON file is created with the expected structure and content. | Happy Path |
| TC-005 | SDK | Call the generate\_from\_new\_docs() function in the SDK. | The full pipeline is triggered, and the function returns a success status. | SDK |
| TC-006 | PDF Extractor | Process a PDF that is a scanned image (no selectable text). | The system gracefully fails or logs a warning that no text could be extracted. No Q\&A is generated. | Edge Case |
| TC-007 | Extractor | Process an empty (0 KB) PDF or DOCX file. | The system logs the empty file and skips it without errors. | Edge Case |
| TC-008 | LLM API | The LLM API returns an error code (e.g., 429 Rate Limit, 500 Server Error). | The system should handle the error, log it, and potentially retry after a backoff period. | Edge Case |
| TC-009 | LLM API | The LLM returns a malformed response (not valid Q\&A format). | The system should fail to parse the response, log the failure and the bad response, and move to the next chunk. | Edge Case |
| TC-010 | Document Store | The MinIO bucket is unreachable or credentials are invalid. | The system fails on startup with a clear error message about connectivity. | Constraint |
| TC-011 | Database | The PostgreSQL database is unreachable. | The system fails to store results and logs a clear error about DB connectivity. | Constraint |
| TC-012 | Scalability | Process 100 documents simultaneously. | The system remains stable and processes all documents, though processing time may increase. No crashes. | Constraint |
| TC-013 | Chunking | Process a document with extremely long, unbroken paragraphs. | The chunking logic correctly splits the text without losing content, respecting chunk size limits. | Edge Case |

