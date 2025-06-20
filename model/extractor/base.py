"""
Base extractor interface for metadata extraction.
"""

from abc import ABC, abstractmethod
from typing import Union, Dict, Any, List
from pathlib import Path
from datetime import datetime

from ..types import ExtractedMetadata, ExtractionResult


class BaseExtractor(ABC):
    """
    Abstract base class for metadata extractors.
    
    All extractor implementations must inherit from this class and
    implement the required methods.
    """
    
    def __init__(self, document_type: str = None):
        """
        Initialize the extractor.
        
        Args:
            document_type: Type of document this extractor is specialized for
        """
        self.document_type = document_type
        self.extraction_fields = []
    
    @abstractmethod
    def extract(self, document_path: Union[str, Path], 
                document_type: str = None) -> ExtractionResult:
        """
        Extract metadata from a document.
        
        Args:
            document_path: Path to the document
            document_type: Type of document (if known)
            
        Returns:
            ExtractionResult with extracted metadata
        """
        pass
    
    @abstractmethod
    def extract_batch(self, document_paths: List[Union[str, Path]], 
                     document_types: List[str] = None) -> List[ExtractionResult]:
        """
        Extract metadata from multiple documents.
        
        Args:
            document_paths: List of document paths
            document_types: List of document types (if known)
            
        Returns:
            List of ExtractionResult objects
        """
        pass
    
    def get_supported_fields(self) -> List[str]:
        """
        Get list of metadata fields this extractor can extract.
        
        Returns:
            List of supported field names
        """
        return self.extraction_fields
    
    def validate_metadata(self, metadata: ExtractedMetadata) -> List[str]:
        """
        Validate extracted metadata for consistency and completeness.
        
        Args:
            metadata: Extracted metadata to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Basic validation
        if metadata.confidence_score < 0 or metadata.confidence_score > 1:
            errors.append("Confidence score must be between 0 and 1")
        
        if metadata.total_amount is not None and metadata.total_amount < 0:
            errors.append("Total amount cannot be negative")
        
        if metadata.document_date is not None:
            if metadata.document_date > datetime.now():
                errors.append("Document date cannot be in the future")
        
        return errors
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from PDF for processing.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        # Implementation for PDF text extraction
        pass
    
    def _extract_tables_from_pdf(self, pdf_path: Path) -> List[Dict]:
        """
        Extract table data from PDF for processing.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of extracted tables as dictionaries
        """
        # Implementation for table extraction
        pass 