#!/usr/bin/env python3
"""
Test script for the FastAPI document analyzer endpoint.
"""

import requests
import json
import sys
import os
from pathlib import Path

def test_analyze_document(pdf_path: str, api_url: str = "http://localhost:8000"):
    """
    Test the document analysis endpoint.
    
    Args:
        pdf_path: Path to the PDF file to test
        api_url: Base URL of the API
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return
    
    print(f"Testing document analysis with: {pdf_path}")
    print(f"API URL: {api_url}")
    print("-" * 50)
    
    # Test the analyze endpoint
    analyze_url = f"{api_url}/documents/analyze"
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            response = requests.post(analyze_url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis successful!")
            print(f"Document ID: {result.get('document_id')}")
            print(f"Filename: {result.get('original_filename')}")
            print(f"Classification: {result.get('classification')}")
            print(f"Metadata: {json.dumps(result.get('metadata', {}), indent=2)}")
            print(f"Processing Info: {json.dumps(result.get('processing_info', {}), indent=2)}")
            return result.get('document_id')  # Return the document ID for further testing
        else:
            print(f"❌ Analysis failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the API server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_get_analysis(document_id: str, api_url: str = "http://localhost:8000"):
    """Test retrieving a stored analysis result."""
    print(f"\nTesting get analysis for document ID: {document_id}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{api_url}/documents/{document_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis retrieved successfully!")
            print(f"Document ID: {result.get('document_id')}")
            print(f"Filename: {result.get('original_filename')}")
            print(f"Classification: {result.get('classification')}")
            print(f"Stored at: {result.get('stored_at')}")
        else:
            print(f"❌ Failed to retrieve analysis: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the API server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_list_documents(api_url: str = "http://localhost:8000"):
    """Test listing all stored documents."""
    print("\nTesting list documents endpoint...")
    print("-" * 50)
    
    try:
        response = requests.get(f"{api_url}/documents")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Documents listed successfully!")
            print(f"Total documents: {result.get('total_count')}")
            print(f"Storage stats: {json.dumps(result.get('storage_stats', {}), indent=2)}")
            
            documents = result.get('documents', [])
            if documents:
                print("\nDocument list:")
                for i, doc in enumerate(documents[:5], 1):  # Show first 5 documents
                    print(f"  {i}. ID: {doc.get('document_id')}")
                    print(f"     Filename: {doc.get('filename')}")
                    print(f"     Classification: {doc.get('classification')}")
                    print(f"     Stored at: {doc.get('stored_at')}")
                    print()
            else:
                print("No documents found.")
        else:
            print(f"❌ Failed to list documents: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the API server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_storage_stats(api_url: str = "http://localhost:8000"):
    """Test getting storage statistics."""
    print("\nTesting storage stats endpoint...")
    print("-" * 50)
    
    try:
        response = requests.get(f"{api_url}/documents/storage/stats")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Storage stats retrieved successfully!")
            print(f"Total documents: {result.get('total_documents')}")
            print(f"Total size: {result.get('total_size_mb')} MB")
            print(f"Storage directory: {result.get('storage_directory')}")
        else:
            print(f"❌ Failed to get storage stats: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the API server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_supported_types(api_url: str = "http://localhost:8000"):
    """Test the supported document types endpoint."""
    print("\nTesting supported document types endpoint...")
    print("-" * 50)
    
    try:
        response = requests.get(f"{api_url}/documents/supported-types")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Supported types retrieved successfully!")
            print(f"Supported document types: {result.get('supported_document_types')}")
            print(f"Count: {result.get('count')}")
        else:
            print(f"❌ Failed to get supported types: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the API server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Check if a PDF file was provided as argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Use a sample PDF from the resources directory
        sample_pdf = Path("src/resources/data/Contract.pdf")
        if sample_pdf.exists():
            pdf_path = str(sample_pdf)
        else:
            print("Usage: python test_api.py [path_to_pdf_file]")
            print("Or place a PDF file in src/resources/data/ and run without arguments")
            sys.exit(1)
    
    # Test the API
    document_id = test_analyze_document(pdf_path)
    
    if document_id:
        # Test the new DocumentStore endpoints
        test_get_analysis(document_id)
        test_list_documents()
        test_storage_stats()
    
    test_supported_types() 