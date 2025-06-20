"""
Document classification models and utilities.
"""

from .base import BaseClassifier
from .llm_classifier import LLMClassifier
from .ml_classifier import MLClassifier

class DocumentClassifier:
    """
    Factory class for creating document classifiers.
    """
    
    @staticmethod
    def create(classifier_type: str = "llm", **kwargs):
        """
        Create a document classifier of the specified type.
        
        Args:
            classifier_type: Type of classifier ("llm" or "ml")
            **kwargs: Additional arguments for the classifier
            
        Returns:
            Classifier instance
        """
        if classifier_type.lower() == "llm":
            return LLMClassifier(**kwargs)
        elif classifier_type.lower() == "ml":
            return MLClassifier(**kwargs)
        else:
            raise ValueError(f"Unknown classifier type: {classifier_type}")

__all__ = ["BaseClassifier", "LLMClassifier", "MLClassifier", "DocumentClassifier"] 