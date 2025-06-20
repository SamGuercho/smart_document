"""
Smart Document Model Package

This package provides models for PDF document classification and metadata extraction.
Supports both LLM-based and classical ML approaches.
"""

from .classifier import DocumentClassifier
from .extractor import MetadataExtractor
from .pipeline import DocumentPipeline
from .types import DocumentType, ExtractedMetadata

__version__ = "0.1.0"
__all__ = [
    "DocumentClassifier",
    "MetadataExtractor", 
    "DocumentPipeline",
    "DocumentType",
    "ExtractedMetadata"
] 