"""
Type definitions for document classification and metadata extraction.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class DocumentType(Enum):
    """Enumeration of supported document types."""
    CONTRACT = "Contract"
    INVOICE = "Invoice"
    EARNINGS_REPORT = "Earnings_report"
    UNKNOWN = "Unknown"


@dataclass
class ExtractedMetadata:
    """Data class for extracted metadata from documents."""
    document_type: DocumentType
    confidence_score: float
    extraction_date: datetime
    
    # Common metadata fields
    document_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    
    # Parties involved
    parties: List[str] = None
    
    # Additional metadata as key-value pairs
    additional_fields: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parties is None:
            self.parties = []
        if self.additional_fields is None:
            self.additional_fields = {}


@dataclass
class ClassificationResult:
    """Result of document classification."""
    document_type: DocumentType
    confidence_score: Dict[DocumentType, float]
    raw_response: Optional[str] = None
    
    def __post_init__(self):
        if self.raw_response is None:
            self.raw_response = ""


@dataclass
class ExtractionResult:
    """Result of metadata extraction."""
    metadata: ExtractedMetadata
    extraction_method: str
    processing_time: float
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = [] 