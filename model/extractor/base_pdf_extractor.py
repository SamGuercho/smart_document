"""
Base class for PDF extraction operations.
"""

from abc import ABC, abstractmethod
from typing import Union, Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BasePDFExtractor(ABC):
    """
    Abstract base class for PDF extraction operations.
    
    This class defines the interface for PDF content extraction,
    including text, tables, images, and metadata extraction.
    """
    
    def __init__(self):
        """Initialize the base PDF extractor."""
        self.supported_formats = ['.pdf']
    
    @abstractmethod
    def extract_text(self, pdf_path: Union[str, Path]) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If file is not a valid PDF
        """
        pass
    
    @abstractmethod
    def get_page_count(self, pdf_path: Union[str, Path]) -> int:
        """
        Get the number of pages in a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
        """
        pass
    
    @abstractmethod
    def get_metadata(self, pdf_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Extract metadata from PDF file properties.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF metadata
        """
        pass
    
    def validate_pdf(self, pdf_path: Union[str, Path]) -> bool:
        """
        Validate that a file is a valid PDF.
        
        Args:
            pdf_path: Path to the file to validate
            
        Returns:
            True if file is a valid PDF, False otherwise
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            return False
        
        if not pdf_path.suffix.lower() in self.supported_formats:
            return False
        
        return self._validate_pdf_internal(pdf_path)
    
    @abstractmethod
    def _validate_pdf_internal(self, pdf_path: Path) -> bool:
        """
        Internal method to validate PDF file structure.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if file is a valid PDF, False otherwise
        """
        pass
    
    def extract_text_chunk(self, pdf_path: Union[str, Path], 
                          max_chars: int = 2000) -> str:
        """
        Extract text content from PDF, truncated to specified length.
        
        Args:
            pdf_path: Path to the PDF file
            max_chars: Maximum number of characters to extract
            
        Returns:
            Extracted text content (truncated)
        """
        full_text = self.extract_text(pdf_path)
        return full_text[:max_chars]
    
    def extract_tables(self, pdf_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Extract table data from PDF for processing.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of extracted tables as dictionaries
        """
        # Default implementation - can be overridden by subclasses
        logger.warning("Table extraction not implemented in this extractor")
        return []
    
    def extract_images(self, pdf_path: Union[str, Path], 
                      output_dir: Optional[Path] = None) -> List[Path]:
        """
        Extract images from PDF for processing.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted images (optional)
            
        Returns:
            List of paths to extracted image files
        """
        # Default implementation - can be overridden by subclasses
        logger.warning("Image extraction not implemented in this extractor")
        return []
    
    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.
        
        Returns:
            List of supported file extensions
        """
        return self.supported_formats.copy() 