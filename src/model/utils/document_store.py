"""
Document store for persisting and retrieving document analysis results.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class DocumentStore:
    """
    A simple document store that persists analysis results to JSON files.
    """
    
    def __init__(self, storage_dir: str = "data/document_store"):
        """
        Initialize the document store.
        
        Args:
            storage_dir: Directory to store JSON files (relative to current working directory)
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Document store initialized at: {self.storage_dir.absolute()}")
    
    def store_analysis(self, analysis_result: Dict[str, Any], document_id: Optional[str] = None) -> str:
        """
        Store a document analysis result.
        
        Args:
            analysis_result: The analysis result dictionary
            document_id: Optional document ID. If not provided, a UUID will be generated
            
        Returns:
            The document ID used for storage
        """
        if document_id is None:
            document_id = str(uuid.uuid4())
        
        # Add metadata
        analysis_result["document_id"] = document_id
        analysis_result["stored_at"] = datetime.utcnow().isoformat()
        
        # Create filename
        filename = f"{document_id}.json"
        file_path = self.storage_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Stored analysis result for document ID: {document_id}")
            return document_id
            
        except Exception as e:
            logger.error(f"Failed to store analysis result for document ID {document_id}: {e}")
            raise
    
    def get_analysis(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document analysis result.
        
        Args:
            document_id: The document ID to retrieve
            
        Returns:
            The analysis result dictionary or None if not found
        """
        filename = f"{document_id}.json"
        file_path = self.storage_dir / filename
        
        if not file_path.exists():
            logger.warning(f"Analysis result not found for document ID: {document_id}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                result = json.load(f)
            
            logger.info(f"Retrieved analysis result for document ID: {document_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve analysis result for document ID {document_id}: {e}")
            raise
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all stored documents with basic metadata.
        
        Returns:
            List of document metadata dictionaries
        """
        documents = []
        
        for json_file in self.storage_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract basic metadata
                doc_info = {
                    "document_id": data.get("document_id"),
                    "filename": data.get("original_filename") or data.get("filename"),
                    "classification": data.get("classification"),
                    "stored_at": data.get("stored_at"),
                    "file_size": json_file.stat().st_size
                }
                documents.append(doc_info)
                
            except Exception as e:
                logger.warning(f"Failed to read document file {json_file}: {e}")
                continue
        
        # Sort by stored_at timestamp (newest first)
        documents.sort(key=lambda x: x.get("stored_at", ""), reverse=True)
        
        logger.info(f"Listed {len(documents)} documents")
        return documents
    
    def delete_analysis(self, document_id: str) -> bool:
        """
        Delete a document analysis result.
        
        Args:
            document_id: The document ID to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        filename = f"{document_id}.json"
        file_path = self.storage_dir / filename
        
        if not file_path.exists():
            logger.warning(f"Analysis result not found for deletion: {document_id}")
            return False
        
        try:
            file_path.unlink()
            logger.info(f"Deleted analysis result for document ID: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete analysis result for document ID {document_id}: {e}")
            raise
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.
        
        Returns:
            Dictionary with storage statistics
        """
        json_files = list(self.storage_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in json_files)
        
        return {
            "total_documents": len(json_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "storage_directory": str(self.storage_dir.absolute())
        } 