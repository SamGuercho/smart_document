#!/usr/bin/env python3
"""
Example script demonstrating the DocumentStore functionality.
"""

import json
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model.utils import DocumentStore

def main():
    """Demonstrate DocumentStore functionality."""
    
    # Initialize the document store
    print("Initializing DocumentStore...")
    store = DocumentStore("data/example_document_store")
    
    # Create a sample analysis result
    sample_analysis = {
        "classification": "contract",
        "filename": "sample_contract.pdf",
        "metadata": {
            "parties": ["Company A", "Company B"],
            "contract_type": "Service Agreement",
            "effective_date": "2024-01-01",
            "expiration_date": "2024-12-31"
        },
        "processing_info": {
            "extraction_method": "LLM",
            "confidence_score": 0.95,
            "processing_time": 2.3
        }
    }
    
    # Store the analysis
    print("\nStoring sample analysis...")
    document_id = store.store_analysis(sample_analysis)
    print(f"Stored with document ID: {document_id}")
    
    # Retrieve the analysis
    print("\nRetrieving the analysis...")
    retrieved = store.get_analysis(document_id)
    if retrieved:
        print("✅ Retrieved successfully!")
        print(f"Document ID: {retrieved['document_id']}")
        print(f"Filename: {retrieved['original_filename']}")
        print(f"Classification: {retrieved['classification']}")
        print(f"Stored at: {retrieved['stored_at']}")
    
    # List all documents
    print("\nListing all documents...")
    documents = store.list_documents()
    print(f"Found {len(documents)} documents:")
    for doc in documents:
        print(f"  - {doc['document_id']}: {doc['filename']} ({doc['classification']})")
    
    # Get storage stats
    print("\nStorage statistics:")
    stats = store.get_storage_stats()
    print(f"  Total documents: {stats['total_documents']}")
    print(f"  Total size: {stats['total_size_mb']} MB")
    print(f"  Storage directory: {stats['storage_directory']}")
    
    # Clean up (optional)
    print(f"\nCleaning up - deleting document {document_id}...")
    deleted = store.delete_analysis(document_id)
    if deleted:
        print("✅ Document deleted successfully!")
    
    # Show final stats
    final_stats = store.get_storage_stats()
    print(f"Final document count: {final_stats['total_documents']}")

if __name__ == "__main__":
    main() 