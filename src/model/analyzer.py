"""
Unified document analyzer that combines classification and extraction.
"""

import uuid
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from .classifier.llm_classifier import LLMClassifier
from .extractor.extractor_factory import ExtractorFactory
from .types import DocumentType, ClassificationResult
from .config.settings import get_settings

logger = logging.getLogger(__name__)


class DocumentAnalyzer:
    """
    Unified document analyzer that combines classification and extraction.
    
    This class provides a single interface to:
    1. Classify documents using LLM
    2. Extract metadata based on document type
    3. Return results in a standardized JSON format
    """
    
    def __init__(self, model_name: str = None, api_key: str = None):
        """
        Initialize the document analyzer.
        
        Args:
            model_name: Name of the LLM model to use
            api_key: API key for the LLM service
        """
        # Get settings
        self.settings = get_settings()
        
        # Use settings if not provided
        if model_name is None:
            model_name = self.settings.get("llm.model_name")
        if api_key is None:
            api_key = self.settings.get("openai.api_key")
        
        # Initialize classifier
        self.classifier = LLMClassifier(model_name=model_name, api_key=api_key)
        
        # Initialize extractor factory
        self.extractor_factory = ExtractorFactory()
        
        logger.info("DocumentAnalyzer initialized successfully")
    
    def analyze(self, document_path: str) -> Dict[str, Any]:
        """
        Analyze a document by classifying it and extracting metadata.
        
        Args:
            document_path: Path to the document to analyze
            
        Returns:
            Dictionary with analysis results in the specified format
        """
        document_path = Path(document_path)
        
        if not document_path.exists():
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Step 1: Classify the document
        logger.info(f"Classifying document: {document_path.name}")
        classification_result = self.classifier.predict(str(document_path))
        
        # Step 2: Extract metadata based on document type
        logger.info(f"Extracting metadata for document type: {classification_result.document_type}")
        extractor = self.extractor_factory.create_extractor(
            classification_result.document_type,
            llm_model=self.classifier.model_name,
            api_key=self.classifier.api_key
        )
        
        extraction_result = extractor.extract(document_path)
        
        # Step 3: Format the results
        result = {
            "document_id": document_id,
            "filename": document_path.name,
            "classification": {
                "type": classification_result.document_type.value.lower(),
                "confidence": classification_result.confidence_score.get(
                    classification_result.document_type.value, 0.0
                )
            },
            "metadata": {}
        }
        
        # Add extracted metadata
        if extraction_result.metadata.additional_fields:
            result["metadata"].update(extraction_result.metadata.additional_fields)
        
        # Add common metadata fields
        if extraction_result.metadata.document_date:
            result["metadata"]["document_date"] = extraction_result.metadata.document_date.isoformat()
        
        if extraction_result.metadata.total_amount:
            result["metadata"]["total_amount"] = extraction_result.metadata.total_amount
        
        if extraction_result.metadata.currency:
            result["metadata"]["currency"] = extraction_result.metadata.currency
        
        if extraction_result.metadata.parties:
            result["metadata"]["parties"] = extraction_result.metadata.parties
        
        # Add processing information
        result["processing_info"] = {
            "processing_time": extraction_result.processing_time,
            "extraction_method": extraction_result.extraction_method,
            "errors": extraction_result.errors
        }
        
        logger.info(f"Analysis completed for {document_path.name}")
        return result
    
    def analyze_batch(self, document_paths: list) -> list:
        """
        Analyze multiple documents.
        
        Args:
            document_paths: List of document paths to analyze
            
        Returns:
            List of analysis results
        """
        results = []
        
        for document_path in document_paths:
            try:
                result = self.analyze(document_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing {document_path}: {e}")
                # Add error result
                results.append({
                    "document_id": str(uuid.uuid4()),
                    "filename": Path(document_path).name,
                    "error": str(e),
                    "classification": None,
                    "metadata": {}
                })
        
        return results
    
    def save_results(self, results: list, output_path: str) -> None:
        """
        Save analysis results to a JSON file.
        
        Args:
            results: List of analysis results
            output_path: Path where to save the JSON file
        """
        output_path = Path(output_path)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save results
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Results saved to: {output_path}")
    
    def get_supported_document_types(self) -> list:
        """
        Get list of supported document types.
        
        Returns:
            List of supported document type names
        """
        return [doc_type.value for doc_type in DocumentType if doc_type != DocumentType.UNKNOWN] 