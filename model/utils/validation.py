"""
Validation utility functions.
"""

from typing import List, Dict, Any, Union
from pathlib import Path
from datetime import datetime
import logging

from ..types import ExtractedMetadata, DocumentType

logger = logging.getLogger(__name__)


def validate_document_path(document_path: Union[str, Path]) -> List[str]:
    """
    Validate document path and file.
    
    Args:
        document_path: Path to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    path = Path(document_path)
    
    if not path.exists():
        errors.append(f"File does not exist: {path}")
        return errors
    
    if not path.is_file():
        errors.append(f"Path is not a file: {path}")
    
    if path.suffix.lower() != '.pdf':
        errors.append(f"File is not a PDF: {path}")
    
    if path.stat().st_size == 0:
        errors.append(f"File is empty: {path}")
    
    return errors


def validate_metadata(metadata: ExtractedMetadata) -> List[str]:
    """
    Validate extracted metadata for consistency and completeness.
    
    Args:
        metadata: Metadata to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Basic field validation
    if metadata.confidence_score < 0 or metadata.confidence_score > 1:
        errors.append("Confidence score must be between 0 and 1")
    
    if metadata.total_amount is not None and metadata.total_amount < 0:
        errors.append("Total amount cannot be negative")
    
    if metadata.document_date is not None:
        if metadata.document_date > datetime.now():
            errors.append("Document date cannot be in the future")
    
    if metadata.currency is not None:
        valid_currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY']
        if metadata.currency not in valid_currencies:
            errors.append(f"Invalid currency: {metadata.currency}")
    
    return errors


def validate_classification_result(result: Dict[str, Any]) -> List[str]:
    """
    Validate classification result structure.
    
    Args:
        result: Classification result to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    required_fields = ['document_type', 'confidence_score']
    
    for field in required_fields:
        if field not in result:
            errors.append(f"Missing required field: {field}")
    
    if 'confidence_score' in result:
        score = result['confidence_score']
        if not isinstance(score, (int, float)) or score < 0 or score > 1:
            errors.append("Confidence score must be a number between 0 and 1")
    
    if 'document_type' in result:
        doc_type = result['document_type']
        if not isinstance(doc_type, DocumentType):
            errors.append("Document type must be a valid DocumentType enum")
    
    return errors


def validate_extraction_result(result: Dict[str, Any]) -> List[str]:
    """
    Validate extraction result structure.
    
    Args:
        result: Extraction result to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    required_fields = ['metadata', 'extraction_method', 'processing_time']
    
    for field in required_fields:
        if field not in result:
            errors.append(f"Missing required field: {field}")
    
    if 'processing_time' in result:
        time = result['processing_time']
        if not isinstance(time, (int, float)) or time < 0:
            errors.append("Processing time must be a non-negative number")
    
    if 'metadata' in result:
        metadata_errors = validate_metadata(result['metadata'])
        errors.extend(metadata_errors)
    
    return errors


def validate_pipeline_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate pipeline configuration.
    
    Args:
        config: Pipeline configuration to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate classifier configuration
    if 'classifier' in config:
        classifier_config = config['classifier']
        if not isinstance(classifier_config, dict):
            errors.append("Classifier config must be a dictionary")
    
    # Validate extractor configuration
    if 'extractor' in config:
        extractor_config = config['extractor']
        if not isinstance(extractor_config, dict):
            errors.append("Extractor config must be a dictionary")
    
    # Validate processing options
    if 'batch_size' in config:
        batch_size = config['batch_size']
        if not isinstance(batch_size, int) or batch_size <= 0:
            errors.append("Batch size must be a positive integer")
    
    return errors 