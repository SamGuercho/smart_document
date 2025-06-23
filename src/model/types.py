"""
Type definitions for document classification and metadata extraction.
"""

from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class DocumentType(Enum):
    """Enumeration of supported document types."""
    CONTRACT = "Contract"
    INVOICE = "Invoice"
    EARNINGS_REPORT = "Financial"
    UNKNOWN = "Unknown"


class Action(BaseModel):
    """Model for document actions."""
    id: str
    title: str
    description: Optional[str] = None
    status: str  # e.g., "pending", "completed"
    priority: Optional[str] = "medium"  # e.g., "low", "medium", "high"
    deadline: Optional[date] = None


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