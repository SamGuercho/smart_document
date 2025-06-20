"""
Base classifier interface for document classification.
"""

from abc import ABC, abstractmethod
from typing import Union, List
from pathlib import Path

from ..types import DocumentType, ClassificationResult


class BaseClassifier(ABC):
    """
    Abstract base class for document classifiers.
    
    All classifier implementations must inherit from this class and
    implement the required methods.
    """
    
    def __init__(self, model_path: Union[str, Path] = None):
        """
        Initialize the classifier.
        
        Args:
            model_path: Path to the trained model file
        """
        self.model_path = Path(model_path) if model_path else None
        self.is_trained = False
    
    @abstractmethod
    def train(self, training_data: List[tuple], **kwargs) -> None:
        """
        Train the classifier on provided data.
        
        Args:
            training_data: List of (document_path, document_type) tuples
            **kwargs: Additional training parameters
        """
        pass
    
    @abstractmethod
    def predict(self, document_path: Union[str, Path]) -> ClassificationResult:
        """
        Classify a single document.
        
        Args:
            document_path: Path to the document to classify
            
        Returns:
            ClassificationResult with predicted type and confidence
        """
        pass
    
    @abstractmethod
    def predict_batch(self, document_paths: List[Union[str, Path]]) -> List[ClassificationResult]:
        """
        Classify multiple documents.
        
        Args:
            document_paths: List of document paths to classify
            
        Returns:
            List of ClassificationResult objects
        """
        pass
    
    def save_model(self, path: Union[str, Path]) -> None:
        """
        Save the trained model to disk.
        
        Args:
            path: Path where to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        # Implementation will be provided by subclasses
    
    def load_model(self, path: Union[str, Path]) -> None:
        """
        Load a trained model from disk.
        
        Args:
            path: Path to the saved model
        """
        # Implementation will be provided by subclasses
        pass
    
    def get_supported_types(self) -> List[DocumentType]:
        """
        Get list of document types this classifier can predict.
        
        Returns:
            List of supported DocumentType values
        """
        return list(DocumentType) 