# Smart Document Model Package

This package provides a comprehensive framework for PDF document classification and metadata extraction, supporting both LLM-based and classical ML approaches.

## Overview

The model package is designed to:
- Classify PDF documents into types (contract, invoice, procurement bill, etc.)
- Extract key metadata (dates, amounts, parties, etc.)
- Support both LLM-based and traditional ML methods
- Provide a unified pipeline for end-to-end document processing

## Package Structure

```
model/
├── __init__.py                 # Main package initialization
├── types.py                   # Type definitions and data classes
├── pipeline.py                # Main processing pipeline
├── classifier/                # Document classification components
│   ├── __init__.py
│   ├── base.py               # Abstract base classifier
│   ├── llm_classifier.py     # LLM-based classifier
│   └── ml_classifier.py      # ML-based classifier
├── extractor/                 # Metadata extraction components
│   ├── __init__.py
│   ├── base.py               # Abstract base extractor
│   ├── llm_extractor.py      # LLM-based extractor
│   ├── rule_extractor.py     # Rule-based extractor
│   └── field_extractors.py   # Specialized field extractors
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── pdf_utils.py          # PDF processing utilities
│   ├── text_utils.py         # Text processing utilities
│   └── validation.py         # Validation utilities
├── config/                    # Configuration management
│   ├── __init__.py
│   ├── default_config.py     # Default configuration
│   └── config_manager.py     # Configuration manager
├── example_usage.py          # Usage examples
└── README.md                 # This file
```

## Key Components

### 1. Document Types
- `DocumentType`: Enumeration of supported document types
- `ExtractedMetadata`: Data class for extracted metadata
- `ClassificationResult`: Result of document classification
- `ExtractionResult`: Result of metadata extraction

### 2. Classifiers
- **BaseClassifier**: Abstract interface for all classifiers
- **LLMClassifier**: Uses language models (GPT, Claude, etc.)
- **MLClassifier**: Uses traditional ML (TF-IDF, BERT, etc.)

### 3. Extractors
- **BaseExtractor**: Abstract interface for all extractors
- **LLMExtractor**: Uses language models for extraction
- **RuleExtractor**: Uses regex patterns and heuristics
- **Field Extractors**: Specialized extractors for specific fields

### 4. Pipeline
- **DocumentPipeline**: Orchestrates classification and extraction
- Handles batch processing and result validation
- Provides unified interface for end-to-end processing

## Quick Start

### Basic Usage

```python
from model import DocumentPipeline, LLMClassifier, LLMExtractor
from pathlib import Path

# Initialize components
classifier = LLMClassifier(model_name="gpt-4", api_key="your-api-key")
extractor = LLMExtractor(model_name="gpt-4", api_key="your-api-key")

# Create pipeline
pipeline = DocumentPipeline(classifier=classifier, extractor=extractor)

# Process a document
document_path = Path("path/to/document.pdf")
result = pipeline.process_single(document_path)

print(f"Document type: {result['classification'].document_type}")
print(f"Confidence: {result['classification'].confidence_score}")
print(f"Extracted metadata: {result['extraction'].metadata}")
```

### Configuration Management

```python
from model.config import ConfigManager

# Load configuration
config_manager = ConfigManager(Path("config.yaml"))

# Update settings
config_manager.update_config({
    "classifier": {"confidence_threshold": 0.8},
    "extractor": {"confidence_threshold": 0.7}
})

# Get configuration
classifier_config = config_manager.get_config("classifier")
```

### Using Specialized Extractors

```python
from model.extractor import DateExtractor, AmountExtractor

# Initialize specialized extractors
date_extractor = DateExtractor()
amount_extractor = AmountExtractor()

# Extract specific fields
document_path = Path("path/to/document.pdf")
date_result = date_extractor.extract(document_path)
amount_result = amount_extractor.extract(document_path)
```

## Supported Document Types

- **Contract**: Legal agreements and contracts
- **Invoice**: Billing documents and invoices
- **Procurement Bill**: Purchase orders and procurement documents
- **Accountability Report**: Financial and accountability reports
- **Earnings Report**: Financial earnings and performance reports

## Extracted Metadata Fields

- **Document Date**: Date of the document
- **Total Amount**: Monetary amounts
- **Currency**: Currency codes (USD, EUR, GBP, etc.)
- **Parties**: Names of involved parties/entities
- **Additional Fields**: Custom metadata as key-value pairs

## Configuration Options

The package supports configuration for:
- Classifier type and parameters
- Extractor type and parameters
- Processing options (batch size, timeouts, etc.)
- Logging settings
- File handling options

## Future Implementation

This skeleton provides the foundation for:
1. **LLM Integration**: Connect to OpenAI, Anthropic, or other LLM APIs
2. **ML Model Training**: Implement traditional ML classifiers
3. **PDF Processing**: Add PDF text and table extraction
4. **Validation Logic**: Implement comprehensive validation
5. **Performance Optimization**: Add caching and batch processing
6. **API Development**: Create REST API endpoints

## Dependencies

When implementing, you'll likely need:
- `openai` or `anthropic` for LLM integration
- `scikit-learn` for ML classifiers
- `PyPDF2` or `pdfplumber` for PDF processing
- `pandas` for data handling
- `numpy` for numerical operations
- `pydantic` for data validation

## Contributing

When adding implementations:
1. Follow the established interfaces
2. Add comprehensive docstrings
3. Include error handling
4. Add unit tests
5. Update configuration as needed 