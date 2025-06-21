# Smart Document Classification

A Python library for intelligent document classification using Large Language Models (LLMs). This project provides a modular framework for classifying business documents such as invoices, contracts, and earnings reports using OpenAI's GPT models.

## Features

- **LLM-based Classification**: Uses OpenAI GPT models for intelligent document classification
- **PDF Processing**: Extracts text from PDF documents using PyPDF2
- **Modular Architecture**: Clean separation between classifiers, extractors, and utilities
- **Configurable Prompts**: Customizable system and user prompts for classification
- **Logprobs Support**: Returns OpenAI logprobs for detailed model confidence analysis
- **Batch Processing**: Support for processing multiple documents at once

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

2. **Customize prompts** (optional) by editing the files in `resources/prompts/`:
   - `classification_system_prompt.txt` - System instructions for the LLM
   - `classification_user_prompt.txt` - User prompt template with `{DOCUMENT_CONTENT}` placeholder

## Usage

### Basic Document Classification

```python
from model.classifier.llm_classifier import LLMClassifier
from pathlib import Path

# Initialize the classifier
classifier = LLMClassifier(model_name="gpt-4")

# Classify a document
pdf_path = Path("path/to/your/document.pdf")
result = classifier.predict(pdf_path)

# Access results
print(f"Document type: {result['result'].document_type}")
print(f"Confidence: {result['result'].confidence_score:.2%}")
print(f"Justification: {result['justification']}")
print(f"Logprobs: {result['logprobs']}")
```

### Supported Document Types

The system can classify documents into the following categories:

- **Invoice** - Bills, invoices, payment requests
- **Contract** - Legal agreements, contracts, terms of service
- **Earnings** - Financial reports, earnings reports, business summaries

### Running Tests

Test the classifier with the provided PDF files:

```bash
python tests/test_llm_classifier.py
```

This will test classification accuracy on the sample documents in `resources/data/`.

## Architecture

### Classifiers

- **BaseClassifier**: Abstract base class defining the classifier interface
- **LLMClassifier**: OpenAI GPT-based classifier with prompt customization
- **MLClassifier**: Placeholder for traditional machine learning approaches

### Extractors

- **BaseExtractor**: Abstract base class for metadata extraction
- **BasePDFExtractor**: Abstract base class for PDF processing operations
- **PDFExtractor**: Concrete PyPDF2 implementation for text extraction
- **LLMExtractor**: LLM-based metadata extraction
- **RuleExtractor**: Rule-based extraction using predefined patterns

### Types

- **DocumentType**: Enumeration of supported document types
- **ClassificationResult**: Result container with type, confidence, and alternatives
- **ExtractionResult**: Metadata extraction results with validation

## Dependencies

### Core Dependencies (`requirements.txt`)
- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `PyPDF2>=3.0.0` - PDF text extraction

### Development Dependencies (`requirements-dev.txt`)
- `pytest>=7.0.0` - Testing framework
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking
- `sphinx>=7.0.0` - Documentation generation