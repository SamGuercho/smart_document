"""
Concrete PDF extractor implementation using pdfplumber.
"""

from typing import Union, Dict, Any, List, Optional
from pathlib import Path
import logging
import pdfplumber

from .base_pdf_extractor import BasePDFExtractor

logger = logging.getLogger(__name__)


class PDFExtractor(BasePDFExtractor):
    """
    Concrete implementation of PDF extractor using pdfplumber.
    
    This class provides methods to extract text, tables, images, and metadata
    from PDF documents using the pdfplumber library.
    """
    
    def __init__(self):
        """Initialize the PDF extractor."""
        super().__init__()
        self._pdf_cache = {}  # Simple cache for PDF objects
    
    def extract_text(self, pdf_path: Union[str, Path]) -> str:
        """
        Extract text content from a PDF file using pdfplumber.
        
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
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                
                for page_num, page in enumerate(pdf.pages):
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
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
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
            with pdfplumber.open(pdf_path) as pdf:
                metadata = pdf.metadata
                
                if metadata:
                    return {
                        'title': metadata.get('Title', ''),
                        'author': metadata.get('Author', ''),
                        'subject': metadata.get('Subject', ''),
                        'creator': metadata.get('Creator', ''),
                        'producer': metadata.get('Producer', ''),
                        'creation_date': metadata.get('CreationDate', ''),
                        'modification_date': metadata.get('ModDate', ''),
                        'page_count': len(pdf.pages)
                    }
                else:
                    return {'page_count': len(pdf.pages)}
                    
        except Exception as e:
            logger.error(f"Error extracting metadata from {pdf_path}: {e}")
            return {}
    
    def _validate_pdf_internal(self, pdf_path: Path) -> bool:
        """
        Internal method to validate PDF file structure using pdfplumber.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if file is a valid PDF, False otherwise
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Just test if we can open and access pages
                _ = len(pdf.pages)
            return True
        except Exception:
            return False
    
    def extract_tables(self, pdf_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Extract table data from PDF using pdfplumber.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of extracted tables as dictionaries
        """
        pdf_path = Path(pdf_path)
        tables = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_tables = page.extract_tables()
                        for table_num, table in enumerate(page_tables):
                            if table:  # Only add non-empty tables
                                tables.append({
                                    'page': page_num + 1,
                                    'table_index': table_num,
                                    'data': table,
                                    'bbox': page.find_tables()[table_num].bbox if page.find_tables() else None
                                })
                    except Exception as e:
                        logger.warning(f"Error extracting tables from page {page_num + 1}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error extracting tables from {pdf_path}: {e}")
            
        return tables
    
    def extract_images(self, pdf_path: Union[str, Path], 
                      output_dir: Optional[Path] = None) -> List[Path]:
        """
        Extract images from PDF using pdfplumber.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted images (optional)
            
        Returns:
            List of paths to extracted image files
        """
        pdf_path = Path(pdf_path)
        image_paths = []
        
        if output_dir is None:
            output_dir = pdf_path.parent / f"{pdf_path.stem}_images"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        # Extract images from the page
                        images = page.images
                        for img_num, img in enumerate(images):
                            try:
                                # Save image to file
                                img_filename = f"page_{page_num + 1}_img_{img_num + 1}.png"
                                img_path = output_dir / img_filename
                                
                                # Convert image data to file
                                if hasattr(img, 'stream') and img.stream:
                                    with open(img_path, 'wb') as f:
                                        f.write(img.stream.get_data())
                                    image_paths.append(img_path)
                                    
                            except Exception as e:
                                logger.warning(f"Error saving image {img_num + 1} from page {page_num + 1}: {e}")
                                continue
                                
                    except Exception as e:
                        logger.warning(f"Error extracting images from page {page_num + 1}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error extracting images from {pdf_path}: {e}")
            
        return image_paths
    
    def extract_text_chunk(self, pdf_path: Union[str, Path], max_chars: int = 2000) -> str:
        """
        Extract text content from PDF, truncated to specified length.
        Enhanced version with better text extraction using pdfplumber.
        
        Args:
            pdf_path: Path to the PDF file
            max_chars: Maximum number of characters to extract
            
        Returns:
            Extracted text content (truncated)
        """
        pdf_path = Path(pdf_path)
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                
                for page in pdf.pages:
                    try:
                        # Use pdfplumber's enhanced text extraction
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                            
                        # Stop if we've reached the character limit
                        if len(text) >= max_chars:
                            break
                            
                    except Exception as e:
                        logger.warning(f"Error extracting text from page: {e}")
                        continue
                
                return text[:max_chars].strip()
                
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def clear_cache(self):
        """Clear the PDF cache."""
        self._pdf_cache.clear() 