# Smart Document Analyzer API

This document describes the FastAPI endpoints for the Smart Document Analyzer.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API server:
```bash
python run_api.py
```

3. The API will be available at `http://localhost:8000`

4. Access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### 1. Root Endpoint
- **URL**: `GET /`
- **Description**: Returns API information and available endpoints
- **Response**: JSON with API details

### 2. Document Analysis
- **URL**: `POST /documents/analyze`
- **Description**: Analyze a PDF document by classifying it and extracting metadata. Results are automatically stored for later retrieval.
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: PDF file (required)
- **Response**: JSON with analysis results including a `document_id` for retrieval

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/documents/analyze" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/your/document.pdf"
```

**Example using Python requests:**
```python
import requests

with open('document.pdf', 'rb') as f:
    files = {'file': ('document.pdf', f, 'application/pdf')}
    response = requests.post('http://localhost:8000/documents/analyze', files=files)
    
if response.status_code == 200:
    result = response.json()
    document_id = result['document_id']
    print(f"Document ID: {document_id}")
    print(f"Document type: {result['classification']['type']}")
    print(f"Confidence: {result['classification']['confidence']}")
    print(f"Metadata: {result['metadata']}")
```

### 3. Retrieve Stored Analysis
- **URL**: `GET /documents/{document_id}`
- **Description**: Retrieve a previously stored document analysis result
- **Parameters**:
  - `document_id`: The document ID returned from the analyze endpoint
- **Response**: JSON with the complete analysis result

**Example:**
```bash
curl -X GET "http://localhost:8000/documents/your-document-id-here"
```

### 4. List All Documents
- **URL**: `GET /documents`
- **Description**: List all stored document analyses with basic metadata
- **Response**: JSON with list of documents and storage statistics

**Example:**
```bash
curl -X GET "http://localhost:8000/documents"
```

### 5. Delete Stored Analysis
- **URL**: `DELETE /documents/{document_id}`
- **Description**: Delete a stored document analysis result
- **Parameters**:
  - `document_id`: The document ID to delete
- **Response**: JSON confirmation of deletion

**Example:**
```bash
curl -X DELETE "http://localhost:8000/documents/your-document-id-here"
```

### 6. Storage Statistics
- **URL**: `GET /documents/storage/stats`
- **Description**: Get storage statistics for the document store
- **Response**: JSON with storage information

**Example:**
```bash
curl -X GET "http://localhost:8000/documents/storage/stats"
```

### 7. Supported Document Types
- **URL**: `GET /documents/supported-types`
- **Description**: Get list of supported document types
- **Response**: JSON with supported document types

## Response Format

### Analysis Response (`POST /documents/analyze`)

```json
{
  "document_id": "uuid-string",
  "filename": "document.pdf",
  "original_filename": "original_name.pdf",
  "classification": {
    "type": "contract|invoice|earnings_report",
    "confidence": 0.95
  },
  "metadata": {
    "document_date": "2023-01-15T00:00:00",
    "total_amount": 1500.00,
    "currency": "USD",
    "parties": ["Company A", "Company B"],
    "additional_fields": {}
  },
  "processing_info": {
    "processing_time": 2.5,
    "extraction_method": "llm",
    "errors": []
  },
  "stored_at": "2024-01-15T10:30:00.123456"
}
```

### Document List Response (`GET /documents`)

```json
{
  "documents": [
    {
      "document_id": "uuid-string",
      "filename": "document.pdf",
      "classification": "contract",
      "stored_at": "2024-01-15T10:30:00.123456",
      "file_size": 2048
    }
  ],
  "total_count": 1,
  "storage_stats": {
    "total_documents": 1,
    "total_size_bytes": 2048,
    "total_size_mb": 0.0,
    "storage_directory": "/path/to/document_store"
  }
}
```

### Storage Stats Response (`GET /documents/storage/stats`)

```json
{
  "total_documents": 5,
  "total_size_bytes": 10240,
  "total_size_mb": 0.01,
  "storage_directory": "/path/to/document_store"
}
```

## Document Storage

The API automatically stores all analysis results in JSON files for persistent storage. Each analysis is assigned a unique document ID that can be used to retrieve the results later.

### Storage Features:
- **Automatic Storage**: All analysis results are automatically stored
- **Unique IDs**: Each document gets a UUID for identification
- **Metadata Tracking**: Storage timestamps and file information are preserved
- **File-based Storage**: Results are stored as JSON files in a `document_store` directory
- **Statistics**: Track total documents and storage usage

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid file type (non-PDF) or file too large (>10MB)
- **404 Not Found**: Document ID not found when retrieving or deleting
- **500 Internal Server Error**: Analysis failure or server error

Error responses include a `detail` field with the error message:

```json
{
  "detail": "Only PDF files are supported. Please upload a PDF file."
}
```

## Testing

Use the provided test script to test the API:

```bash
# Test with a sample PDF
python test_api.py

# Test with a specific PDF file
python test_api.py path/to/your/document.pdf
```

The test script will:
1. Analyze a document and get the document ID
2. Retrieve the stored analysis using the document ID
3. List all stored documents
4. Show storage statistics
5. Test supported document types

## Configuration

The API uses the same configuration as the core analyzer. Make sure to set up your environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LLM_MODEL_NAME`: Model name (defaults to "gpt-4")

## Development

To run the API in development mode with auto-reload:

```bash
python run_api.py
```

The server will automatically reload when you make changes to the code.

## API Documentation

Once the server is running, you can access:

- **Interactive API docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative API docs**: `http://localhost:8000/redoc` (ReDoc)
- **OpenAPI schema**: `http://localhost:8000/openapi.json` 