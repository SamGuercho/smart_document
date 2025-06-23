# Smart Document Analyzer

A comprehensive Python library for intelligent document analysis using Large Language Models (LLMs). This project provides a unified framework for classifying and extracting metadata from business documents such as invoices, contracts, and financial reports using OpenAI's GPT models.

## Features

- **Unified Document Analysis**: Single interface for classification and metadata extraction
- **LLM-based Classification**: Uses OpenAI GPT models for intelligent document classification
- **Advanced Metadata Extraction**: Extracts structured data based on document type
- **PDF Processing**: Extracts text from PDF documents using PyPDF2
- **Document Storage**: Persistent storage of analysis results with unique document IDs
- **REST API**: FastAPI-based web service for document analysis
- **Modular Architecture**: Clean separation between classifiers, extractors, and utilities
- **Configurable Prompts**: Customizable system and user prompts for classification and extraction
- **Batch Processing**: Support for processing multiple documents at once
- **Action Generation**: Automatically generates workflow actions based on document type

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Core Dependencies

```bash
pip install -r requirements.txt
```

### Development Dependencies

```bash
pip install -r requirements-dev.txt
```

## Configuration

1. **Set up your OpenAI API key** by creating a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

2. **Customize prompts** (optional) by editing the files in `src/resources/prompts/`:
   - `classification_system_prompt.txt` - System instructions for classification
   - `classification_user_prompt.txt` - User prompt template for classification
   - `*_entity_extract_system_prompt.txt` - System prompts for metadata extraction
   - `*_entity_extract_user_prompt.txt` - User prompts for metadata extraction

## Usage

### Basic Document Analysis

```python
from src.model.analyzer import DocumentAnalyzer
from pathlib import Path

# Initialize the analyzer
analyzer = DocumentAnalyzer()

# Analyze a document
pdf_path = Path("src/resources/data/Contract.pdf")
result = analyzer.analyze(str(pdf_path))

# Access results
print(f"Document ID: {result['document_id']}")
print(f"Document type: {result['classification']['type']}")
print(f"Confidence: {result['classification']['confidence']:.2%}")
print(f"Metadata: {result['metadata']}")
print(f"Processing time: {result['processing_info']['processing_time']:.2f}s")
```

### Batch Document Analysis

```python
# Analyze multiple documents
document_paths = [
    "src/resources/data/Contract.pdf",
    "src/resources/data/invoice1.pdf",
    "src/resources/data/Earnings.pdf"
]

results = analyzer.analyze_batch(document_paths)

# Save results to file
analyzer.save_results(results, "analysis_results.json")
```

### Using the Document Store

```python
from src.model.utils.document_store import DocumentStore

# Initialize document store
store = DocumentStore()

# Store analysis result
store.store_analysis(result)

# Retrieve analysis by ID
retrieved_result = store.get_analysis(result['document_id'])

# List all stored documents
documents = store.list_documents()

# Get storage statistics
stats = store.get_storage_stats()
```

### Supported Document Types

The system can classify and extract metadata from the following document types:

- **Contract** - Legal agreements, contracts, terms of service
  - Extracts: effective date, termination date, parties, key terms
- **Invoice** - Bills, invoices, payment requests
  - Extracts: vendor, amount, currency, due date, line items
- **Financial** - Financial reports, earnings reports, business summaries
  - Extracts: company name, reporting period, key metrics, executive summary

### Running Tests

Test the analyzer with the provided PDF files:

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run specific test
python -m pytest tests/unit/test_analyzer.py -v
```

## API Usage

### Start the API Server

```bash
python api/server.py
```

The API will be available at `http://localhost:8000`

### API Examples

```python
import requests

# Analyze a document
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

# Retrieve stored analysis
response = requests.get(f'http://localhost:8000/documents/{document_id}')
if response.status_code == 200:
    analysis = response.json()
    print(f"Retrieved analysis: {analysis}")

# Get document actions
response = requests.get(f'http://localhost:8000/documents/{document_id}/actions')
if response.status_code == 200:
    actions = response.json()
    print(f"Generated actions: {actions['actions']}")
```

For complete API documentation, see [API_README.md](API_README.md).

## Architecture

### Core Components

- **DocumentAnalyzer**: Main interface for document analysis
- **LLMClassifier**: OpenAI GPT-based classifier
- **ExtractorFactory**: Factory for creating document-specific extractors
- **DocumentStore**: Persistent storage for analysis results

### Extractors

- **EntityExtractor**: Base class for metadata extraction
- **ContractExtractor**: Extracts contract-specific metadata
- **InvoiceExtractor**: Extracts invoice-specific metadata
- **ReportExtractor**: Extracts financial report metadata
- **LLMExtractor**: LLM-based extraction using custom prompts

### Utilities

- **DocumentStore**: JSON-based storage with unique document IDs
- **PDFUtils**: PDF text extraction utilities
- **TextUtils**: Text processing utilities
- **Validation**: Data validation utilities

### Types

- **DocumentType**: Enumeration of supported document types
- **ClassificationResult**: Result container with type and confidence
- **ExtractionResult**: Metadata extraction results with validation
- **Action**: Workflow action items for document processing

## Dependencies

### Core Dependencies (`requirements.txt`)
- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `PyPDF2>=3.0.0` - PDF text extraction
- `fastapi>=0.100.0` - Web API framework
- `uvicorn>=0.20.0` - ASGI server
- `python-multipart>=0.0.6` - File upload support

### Development Dependencies (`requirements-dev.txt`)
- `pytest>=7.0.0` - Testing framework
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking
- `requests>=2.31.0` - HTTP client for testing