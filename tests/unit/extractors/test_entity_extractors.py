#!/usr/bin/env python3
"""
Test script for Entity Extractors with PDF files
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Add src to Python path explicitly
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Now import directly
from model.extractor.contract_extractor import ContractExtractor
from model.extractor.invoice_extractor import InvoiceExtractor
from model.extractor.report_extractor import ReportExtractor
from model.config.settings import init_settings

def test_contract_extractor():
    """Test the ContractExtractor with Contract.pdf."""
    
    print("\n" + "="*60)
    print("📋 Testing ContractExtractor with Contract.pdf...")
    print("="*60)
    
    # Initialize settings
    print("🚀 Initializing settings...")
    settings = init_settings()
    print("✅ Settings initialized successfully!")
    
    # Check API key availability
    if not settings.get('openai', {}).get('api_key'):
        print("⚠️  No API key found - LLM features will use placeholder implementations")
    
    # Initialize the extractor (no need to pass API key anymore)
    print("🚀 Initializing ContractExtractor...")
    extractor = ContractExtractor()
    print("✅ ContractExtractor initialized successfully!")
    
    # Path to test file
    data_dir = project_root / "src" / "resources" / "data"
    pdf_path = data_dir / "Contract.pdf"
    
    if not pdf_path.exists():
        print(f"❌ File not found: Contract.pdf")
        return False
    
    print(f"\n📄 Testing: Contract.pdf")
    print("-" * 40)
    
    # Extract entities
    result = extractor.extract(pdf_path)
    
    # Display results
    print(f"✅ Extraction completed in {result.processing_time:.2f}s")
    print(f"📊 Confidence Score: {result.metadata.confidence_score:.2%}")
    print(f"📋 Document Type: {result.metadata.document_type.value}")
    
    # Display extracted entities
    print("\n📋 Extracted Entities:")
    print("-" * 20)
    
    if result.metadata.additional_fields:
        for field, value in result.metadata.additional_fields.items():
            print(f"  {field}: {value}")
    else:
        print("  No entities extracted")
    
    # Display any errors
    if result.errors:
        print(f"\n⚠️  Errors encountered:")
        for error in result.errors:
            print(f"  - {error}")
    
    return len(result.errors) == 0

def test_invoice_extractor():
    """Test the InvoiceExtractor with invoice PDFs."""
    
    print("\n" + "="*60)
    print("📋 Testing InvoiceExtractor with invoice PDFs...")
    print("="*60)
    
    # Initialize settings
    print("🚀 Initializing settings...")
    settings = init_settings()
    print("✅ Settings initialized successfully!")
    
    # Check API key availability
    if not settings.get('openai', {}).get('api_key'):
        print("⚠️  No API key found - LLM features will use placeholder implementations")
    
    # Initialize the extractor (no need to pass API key anymore)
    print("🚀 Initializing InvoiceExtractor...")
    extractor = InvoiceExtractor()
    print("✅ InvoiceExtractor initialized successfully!")
    
    # Path to test files
    data_dir = project_root / "src" / "resources" / "data"
    test_files = ["invoice1.pdf", "invoice2.pdf"]
    
    results = []
    
    for filename in test_files:
        pdf_path = data_dir / filename
        if not pdf_path.exists():
            print(f"❌ File not found: {filename}")
            continue
            
        print(f"\n📄 Testing: {filename}")
        print("-" * 40)
        
        # Extract entities
        result = extractor.extract(pdf_path)
        
        # Display results
        print(f"✅ Extraction completed in {result.processing_time:.2f}s")
        print(f"📊 Confidence Score: {result.metadata.confidence_score:.2%}")
        print(f"📋 Document Type: {result.metadata.document_type.value}")
        
        # Display extracted entities
        print("\n📋 Extracted Entities:")
        print("-" * 20)
        
        if result.metadata.additional_fields:
            for field, value in result.metadata.additional_fields.items():
                print(f"  {field}: {value}")
        else:
            print("  No entities extracted")
        
        # Display any errors
        if result.errors:
            print(f"\n⚠️  Errors encountered:")
            for error in result.errors:
                print(f"  - {error}")
        
        results.append({
            'filename': filename,
            'success': len(result.errors) == 0,
            'confidence': result.metadata.confidence_score,
            'entities_count': len(result.metadata.additional_fields) if result.metadata.additional_fields else 0
        })
    
    # Print summary
    print("\n" + "="*60)
    print("📊 INVOICE EXTRACTOR SUMMARY")
    print("="*60)
    
    successful_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"Total tests: {total_tests}")
    print(f"Successful extractions: {successful_tests}")
    print(f"Success rate: {successful_tests/total_tests:.1%}")
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['filename']}: {result['entities_count']} entities, {result['confidence']:.1%} confidence")
    
    return successful_tests == total_tests

def test_report_extractor():
    """Test the ReportExtractor with Earnings.pdf."""
    
    print("\n" + "="*60)
    print("📋 Testing ReportExtractor with Earnings.pdf...")
    print("="*60)
    
    # Initialize settings
    print("🚀 Initializing settings...")
    settings = init_settings()
    print("✅ Settings initialized successfully!")
    
    # Check API key availability
    if not settings.get('openai', {}).get('api_key'):
        print("⚠️  No API key found - LLM features will use placeholder implementations")
    
    # Initialize the extractor (no need to pass API key anymore)
    print("🚀 Initializing ReportExtractor...")
    extractor = ReportExtractor()
    print("✅ ReportExtractor initialized successfully!")
    
    # Path to test file
    data_dir = project_root / "src" / "resources" / "data"
    pdf_path = data_dir / "Earnings.pdf"
    
    if not pdf_path.exists():
        print(f"❌ File not found: Earnings.pdf")
        return False
    
    print(f"\n📄 Testing: Earnings.pdf")
    print("-" * 40)
    
    # Extract entities
    result = extractor.extract(pdf_path)
    
    # Display results
    print(f"✅ Extraction completed in {result.processing_time:.2f}s")
    print(f"📊 Confidence Score: {result.metadata.confidence_score:.2%}")
    print(f"📋 Document Type: {result.metadata.document_type.name}")
    
    # Display extracted entities
    print("\n📋 Extracted Entities:")
    print("-" * 20)
    
    if result.metadata.additional_fields:
        for field, value in result.metadata.additional_fields.items():
            print(f"  {field}: {value}")
    else:
        print("  No entities extracted")
    
    # Display any errors
    if result.errors:
        print(f"\n⚠️  Errors encountered:")
        for error in result.errors:
            print(f"  - {error}")
    
    return len(result.errors) == 0

def test_all_extractors():
    """Run all extractor tests."""
    
    print("🧪 Entity Extractor Test Suite")
    print("This will test all three extractor types with PDF files from resources/data/")
    print("\nPrerequisites:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set OPENAI_API_KEY in .env file (optional - for LLM features)")
    print("3. Ensure PDF files are in resources/data/")
    print("4. Optional: Create config.yaml for custom settings")
    
    input("\nPress Enter to continue...")
    
    # Run all tests
    contract_success = test_contract_extractor()
    invoice_success = test_invoice_extractor()
    report_success = test_report_extractor()
    
    # Print final summary
    print("\n" + "="*60)
    print("📊 FINAL TEST SUMMARY")
    print("="*60)
    
    tests = [
        ("Contract Extractor", contract_success),
        ("Invoice Extractor", invoice_success),
        ("Report Extractor", report_success)
    ]
    
    successful_tests = sum(1 for _, success in tests if success)
    total_tests = len(tests)
    
    print(f"Total extractor types tested: {total_tests}")
    print(f"Successful tests: {successful_tests}")
    print(f"Overall success rate: {successful_tests/total_tests:.1%}")
    
    print("\nDetailed Results:")
    for name, success in tests:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    if successful_tests == total_tests:
        print("\n🎉 All extractor tests passed!")
    else:
        print("\n⚠️  Some extractor tests failed. Check the output above for details.")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    test_all_extractors() 