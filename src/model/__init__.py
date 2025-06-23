"""
Smart Document Model Package

This package provides models for PDF document classification and metadata extraction.
Supports both LLM-based and classical ML approaches.
"""

# Import only what actually exists
from .types import DocumentType, ClassificationResult, ExtractedMetadata
from .analyzer import DocumentAnalyzer

__version__ = "0.1.0"
__all__ = [
    "DocumentType",
    "ClassificationResult", 
    "ExtractedMetadata",
    "DocumentAnalyzer"
] 