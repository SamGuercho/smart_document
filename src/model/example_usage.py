"""
Example usage of the model components.

This script demonstrates how to use the document classification
and metadata extraction pipeline.
"""

from pathlib import Path
from model import DocumentPipeline, LLMClassifier, LLMExtractor, MLClassifier, RuleExtractor
from model.config import ConfigManager
from model.types import DocumentType


def example_llm_pipeline():
    """Example using LLM-based classification and extraction."""
    print("=== LLM Pipeline Example ===")
    
    # Initialize components
    classifier = LLMClassifier(model_name="gpt-4", api_key="your-api-key")
    extractor = LLMExtractor(model_name="gpt-4", api_key="your-api-key")
    
    # Create pipeline
    pipeline = DocumentPipeline(classifier=classifier, extractor=extractor)
    
    # Process a document
    document_path = Path("resources/data/Contract.pdf")
    if document_path.exists():
        result = pipeline.process_single(document_path)
        print(f"Classification: {result['classification']}")
        print(f"Extraction: {result['extraction']}")
    else:
        print(f"Document not found: {document_path}")


def example_ml_pipeline():
    """Example using ML-based classification and rule-based extraction."""
    print("\n=== ML Pipeline Example ===")
    
    # Initialize components
    classifier = MLClassifier(model_type="tfidf_svm")
    extractor = RuleExtractor()
    
    # Create pipeline
    pipeline = DocumentPipeline(classifier=classifier, extractor=extractor)
    
    # Process multiple documents
    document_paths = [
        Path("resources/data/Contract.pdf"),
        Path("resources/data/invoice1.pdf"),
        Path("resources/data/Earnings.pdf")
    ]
    
    existing_paths = [p for p in document_paths if p.exists()]
    if existing_paths:
        results = pipeline.process_batch(existing_paths)
        for i, result in enumerate(results):
            print(f"Document {i+1}: {result['classification']}")
    else:
        print("No documents found")


def example_configuration():
    """Example of configuration management."""
    print("\n=== Configuration Example ===")
    
    # Create configuration manager
    config_manager = ConfigManager()
    
    # Update configuration
    config_manager.update_config({
        "classifier": {
            "confidence_threshold": 0.8
        },
        "extractor": {
            "confidence_threshold": 0.7
        }
    })
    
    # Get configuration
    classifier_config = config_manager.get_config("classifier")
    print(f"Classifier config: {classifier_config}")
    
    # Validate configuration
    errors = config_manager.validate_config()
    if errors:
        print(f"Configuration errors: {errors}")
    else:
        print("Configuration is valid")


def example_field_extractors():
    """Example of using specialized field extractors."""
    print("\n=== Field Extractors Example ===")
    
    from model.extractor import DateExtractor, AmountExtractor, PartyExtractor
    
    # Initialize specialized extractors
    date_extractor = DateExtractor()
    amount_extractor = AmountExtractor()
    party_extractor = PartyExtractor()
    
    document_path = Path("resources/data/invoice1.pdf")
    if document_path.exists():
        # Extract specific fields
        date_result = date_extractor.extract(document_path)
        amount_result = amount_extractor.extract(document_path)
        party_result = party_extractor.extract(document_path)
        
        print(f"Date extraction: {date_result}")
        print(f"Amount extraction: {amount_result}")
        print(f"Party extraction: {party_result}")


if __name__ == "__main__":
    # Run examples
    example_configuration()
    example_field_extractors()
    
    # Note: LLM and ML examples require actual implementation
    # and API keys/trained models
    print("\nNote: LLM and ML examples require actual implementation")
    print("and API keys/trained models to run.") 