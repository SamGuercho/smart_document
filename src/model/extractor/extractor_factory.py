"""
Factory for creating entity extractors based on document type.
"""

from typing import Optional
from pathlib import Path

from .entity_extractor import BaseEntityExtractor
from .contract_extractor import ContractExtractor
from .invoice_extractor import InvoiceExtractor
from .report_extractor import ReportExtractor
from ..types import DocumentType
from ..config.settings import get_settings


class ExtractorFactory:
    """
    Factory class for creating entity extractors.
    """
    
    @staticmethod
    def create_extractor(document_type: DocumentType, 
                        llm_model: str = None, 
                        api_key: str = None) -> BaseEntityExtractor:
        """
        Create an entity extractor for the specified document type.
        
        Args:
            document_type: Type of document to extract entities from
            llm_model: LLM model to use (optional, uses settings if not provided)
            api_key: API key for LLM service (optional, uses settings if not provided)
            
        Returns:
            Entity extractor instance
        """
        # Get settings
        settings = get_settings()
        
        # Use settings if not provided
        if llm_model is None:
            llm_model = settings.get_model_name()
        if api_key is None:
            api_key = settings.get_api_key()
        
        if document_type == DocumentType.INVOICE:
            return InvoiceExtractor(llm_model=llm_model, api_key=api_key)
        elif document_type == DocumentType.CONTRACT:
            return ContractExtractor(llm_model=llm_model, api_key=api_key)
        elif document_type == DocumentType.EARNINGS_REPORT:
            return ReportExtractor(llm_model=llm_model, api_key=api_key)
        else:
            raise ValueError(f"Unsupported document type: {document_type}")
    
    @staticmethod
    def create_extractor_from_file(file_path: Path, 
                                  document_type: Optional[DocumentType] = None,
                                  llm_model: str = None, 
                                  api_key: str = None) -> BaseEntityExtractor:
        """
        Create an entity extractor based on file content or specified type.
        
        Args:
            file_path: Path to the document file
            document_type: Known document type (optional)
            llm_model: LLM model to use (optional, uses settings if not provided)
            api_key: API key for LLM service (optional, uses settings if not provided)
            
        Returns:
            Entity extractor instance
        """
        # Get settings
        settings = get_settings()
        
        # Use settings if not provided
        if llm_model is None:
            llm_model = settings.get_model_name()
        if api_key is None:
            api_key = settings.get_api_key()
        
        # If document type is provided, use it
        if document_type:
            return ExtractorFactory.create_extractor(document_type, llm_model, api_key)
        
        # Otherwise, try to infer from file content or extension
        # This is a simplified implementation - you might want to add more sophisticated detection
        file_extension = file_path.suffix.lower()
        file_name = file_path.name.lower()
        
        if 'invoice' in file_name or 'bill' in file_name:
            return InvoiceExtractor(llm_model=llm_model, api_key=api_key)
        elif 'contract' in file_name or 'agreement' in file_name:
            return ContractExtractor(llm_model=llm_model, api_key=api_key)
        elif 'report' in file_name or 'earnings' in file_name:
            return ReportExtractor(llm_model=llm_model, api_key=api_key)
        else:
            # Default to invoice extractor
            return InvoiceExtractor(llm_model=llm_model, api_key=api_key) 