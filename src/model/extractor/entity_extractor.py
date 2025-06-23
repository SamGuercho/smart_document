"""
Hybrid entity extraction system combining rule-based and LLM-based extraction.
"""

from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import time
import re
import pdfplumber

from .base import BaseExtractor
from .llm_extractor import LLMExtractor
from .field_extractors import DateExtractor, AmountExtractor, PartyExtractor, CurrencyExtractor
from ..types import ExtractedMetadata, ExtractionResult, DocumentType
from ..config.settings import get_settings


class BaseEntityExtractor(BaseExtractor):
    """
    Base class for hybrid entity extraction combining rule-based and LLM-based methods.
    
    This extractor uses rule-based extraction for standard, easily identifiable entities
    and LLM-based extraction for complex, context-dependent entities.
    """
    
    def __init__(self, document_type: DocumentType, llm_model: str = None, api_key: str = None):
        """
        Initialize the base entity extractor.
        
        Args:
            document_type: Type of document this extractor is specialized for
            llm_model: LLM model to use for complex entity extraction (optional, uses settings if not provided)
            api_key: API key for LLM service (optional, uses settings if not provided)
        """
        super().__init__(document_type=document_type.value)
        self.document_type = document_type
        
        # Get settings
        self.settings = get_settings()
        
        # Use settings if not provided
        if llm_model is None:
            llm_model = self.settings.get_model_name()
        if api_key is None:
            api_key = self.settings.get('openai', {}).get('api_key')
        
        # Initialize specialized extractors
        self.date_extractor = DateExtractor()
        self.amount_extractor = AmountExtractor()
        self.party_extractor = PartyExtractor()
        self.currency_extractor = CurrencyExtractor()
        self.llm_extractor = LLMExtractor(model_name=llm_model, api_key=api_key)
        
        # Define extraction fields for this document type
        self.rule_based_fields = []
        self.llm_based_fields = []
        self._setup_extraction_fields()
    
    @abstractmethod
    def _setup_extraction_fields(self):
        """
        Setup which fields should be extracted using rule-based vs LLM-based methods.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def _extract_rule_based_entities(self, text_content: str) -> Dict[str, Any]:
        """
        Extract entities using rule-based methods.
        Must be implemented by subclasses.
        
        Args:
            text_content: Extracted text from the document
            
        Returns:
            Dictionary of extracted entities
        """
        pass
    
    @abstractmethod
    def _extract_llm_entities(self, text_content: str, rule_based_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract complex entities using LLM-based methods.
        Must be implemented by subclasses.
        
        Args:
            text_content: Extracted text from the document
            rule_based_results: Results from rule-based extraction
            
        Returns:
            Dictionary of extracted entities
        """
        pass
    
    def extract(self, document_path: Union[str, Path], 
                document_type: str = None) -> ExtractionResult:
        """
        Extract entities from a document using hybrid approach.
        
        Args:
            document_path: Path to the document
            document_type: Type of document (if known)
            
        Returns:
            ExtractionResult with extracted entities
        """
        start_time = time.time()
        errors = []
        
        try:
            # Extract text from PDF
            text_content = self._extract_text_from_pdf(Path(document_path))
            
            # Step 1: Rule-based extraction for standard entities
            rule_based_results = self._extract_rule_based_entities(text_content)
            
            # Step 2: LLM-based extraction for complex entities
            combined_results = self._extract_llm_entities(text_content, rule_based_results)
            
            # Step 4: Create metadata object
            metadata = self._create_metadata(combined_results)
            
            # Step 5: Validate results
            validation_errors = self.validate_metadata(metadata)
            errors.extend(validation_errors)
            
            processing_time = time.time() - start_time
            extraction_result = ExtractionResult(
                metadata=metadata,
                extraction_method="hybrid_entity_extraction", # TODO change it later depending on a mode of extraction, do as enum
                processing_time=processing_time,
                errors=errors
            )

            return extraction_result
            
        except Exception as e:
            processing_time = time.time() - start_time
            errors.append(f"Extraction failed: {str(e)}")
            
            # Return empty metadata on error
            metadata = ExtractedMetadata(
                document_type=self.document_type,
                confidence_score=0.0,
                extraction_date=datetime.now()
            )
            
            return ExtractionResult(
                metadata=metadata,
                extraction_method="hybrid_entity_extraction",
                processing_time=processing_time,
                errors=errors
            )
    
    def extract_batch(self, document_paths: List[Union[str, Path]], 
                     document_types: List[str] = None) -> List[ExtractionResult]:
        """
        Extract entities from multiple documents.
        
        Args:
            document_paths: List of document paths
            document_types: List of document types (if known)
            
        Returns:
            List of ExtractionResult objects
        """
        results = []
        for i, doc_path in enumerate(document_paths):
            doc_type = document_types[i] if document_types and i < len(document_types) else None
            result = self.extract(doc_path, doc_type)
            results.append(result)
        return results
    
    def _create_metadata(self, extracted_entities: Dict[str, Any]) -> ExtractedMetadata:
        """
        Create ExtractedMetadata from extracted entities.
        
        Args:
            extracted_entities: Dictionary of extracted entities
            
        Returns:
            ExtractedMetadata object
        """
        # Extract common fields
        document_date = extracted_entities.get('document_date')
        total_amount = extracted_entities.get('total_amount')
        currency = extracted_entities.get('currency')
        parties = extracted_entities.get('parties', [])
        
        # Calculate confidence score based on extraction success
        confidence_score = self._calculate_confidence_score(extracted_entities)
        
        # Create metadata object
        metadata = ExtractedMetadata(
            document_type=self.document_type,
            confidence_score=confidence_score,
            extraction_date=datetime.now(),
            document_date=document_date,
            total_amount=total_amount,
            currency=currency,
            parties=parties,
            additional_fields=extracted_entities
        )
        
        return metadata
    
    def _calculate_confidence_score(self, extracted_entities: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on extraction success.
        
        Args:
            extracted_entities: Dictionary of extracted entities
            
        Returns:
            Confidence score between 0 and 1
        """
        total_fields = len(self.rule_based_fields) + len(self.llm_based_fields)
        if total_fields == 0:
            return 0.0
        
        extracted_count = sum(1 for field in self.rule_based_fields + self.llm_based_fields 
                            if field in extracted_entities and extracted_entities[field] is not None)
        
        return extracted_count / total_fields
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from PDF for processing.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        # This would typically use a PDF processing library like PyPDF2 or pdfplumber
        # For now, we'll use a placeholder implementation
        try:
            text_content = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text_content += page.extract_text() + "\n"
            
            if not text_content.strip():
                raise Exception("No text content extracted from PDF")
                
            return text_content
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")