"""
Concrete PDF extractor implementation using PyPDF2.
"""

from typing import Union, Dict, Any, List, Optional
from pathlib import Path
import logging
import PyPDF2

from .base_pdf_extractor import BasePDFExtractor

logger = logging.getLogger(__name__)


class PDFExtractor(BasePDFExtractor):
    """
    Concrete implementation of PDF extractor using PyPDF2.
    
    This class provides methods to extract text, tables, images, and metadata
    from PDF documents using the PyPDF2 library.
    """
    
    def __init__(self):
        """Initialize the PDF extractor."""
        super().__init__()
        self._pdf_reader_cache = {}  # Simple cache for PDF readers
    
    def extract_text(self, pdf_path: Union[str, Path]) -> str:
        """
        Extract text content from a PDF file using PyPDF2.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If file is not a valid PDF
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not self.validate_pdf(pdf_path):
            raise ValueError(f"File is not a valid PDF: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                        continue
                
                return text.strip()
                
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    def get_page_count(self, pdf_path: Union[str, Path]) -> int:
        """
        Get the number of pages in a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
        """
        pdf_path = Path(pdf_path)
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            logger.error(f"Error getting page count for {pdf_path}: {e}")
            return 0
    
    def get_metadata(self, pdf_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Extract metadata from PDF file properties.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF metadata
        """
        pdf_path = Path(pdf_path)
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                if metadata:
                    return {
                        'title': metadata.get('/Title', ''),
                        'author': metadata.get('/Author', ''),
                        'subject': metadata.get('/Subject', ''),
                        'creator': metadata.get('/Creator', ''),
                        'producer': metadata.get('/Producer', ''),
                        'creation_date': metadata.get('/CreationDate', ''),
                        'modification_date': metadata.get('/ModDate', ''),
                        'page_count': len(pdf_reader.pages)
                    }
                else:
                    return {'page_count': len(pdf_reader.pages)}
                    
        except Exception as e:
            logger.error(f"Error extracting metadata from {pdf_path}: {e}")
            return {}
    
    def _validate_pdf_internal(self, pdf_path: Path) -> bool:
        """
        Internal method to validate PDF file structure using PyPDF2.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if file is a valid PDF, False otherwise
        """
        try:
            with open(pdf_path, 'rb') as file:
                PyPDF2.PdfReader(file)
            return True
        except Exception:
            return False
    
    def extract_tables(self, pdf_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Extract table data from PDF using PyPDF2.
        
        Note: PyPDF2 has limited table extraction capabilities.
        For better table extraction, consider using pdfplumber or tabula-py.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of extracted tables as dictionaries
        """
        logger.warning("PyPDF2 has limited table extraction capabilities. "
                      "Consider using pdfplumber or tabula-py for better results.")
        return []
    
    def extract_images(self, pdf_path: Union[str, Path], 
                      output_dir: Optional[Path] = None) -> List[Path]:
        """
        Extract images from PDF using PyPDF2.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted images (optional)
            
        Returns:
            List of paths to extracted image files
        """
        logger.warning("Image extraction not implemented in PyPDF2 version. "
                      "Consider using pdfplumber for image extraction.")
        return []
    
    def clear_cache(self):
        """Clear the PDF reader cache."""
        self._pdf_reader_cache.clear() 