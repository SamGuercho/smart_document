#!/usr/bin/env python3
"""
Test script for DocumentAnalyzer
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
from model.analyzer import DocumentAnalyzer

def test_analyzer():
    """Test the DocumentAnalyzer with various PDF files."""
    
    print("\n" + "="*60)
    print("🧪 Testing DocumentAnalyzer...")
    print("="*60)
    
    # Initialize analyzer
    print("🚀 Initializing DocumentAnalyzer...")
    analyzer = DocumentAnalyzer()
    print("✅ DocumentAnalyzer initialized successfully!")
    
    # Path to test files
    data_dir = project_root / "src" / "resources" / "data"
    test_files = ["Contract.pdf", "invoice1.pdf", "invoice2.pdf", "Earnings.pdf"]
    
    results = []
    
    for filename in test_files:
        pdf_path = data_dir / filename
        if not pdf_path.exists():
            print(f"❌ File not found: {filename}")
            continue
            
        print(f"\n📄 Testing: {filename}")
        print("-" * 40)
        
        try:
            # Analyze the document
            result = analyzer.analyze(str(pdf_path))
            
            # Display results
            print(f"✅ Analysis completed")
            print(f"📋 Document ID: {result['document_id']}")
            print(f"🎯 Type: {result['classification']['type']}")
            print(f"📊 Confidence: {result['classification']['confidence']:.2%}")
            
            # Display metadata
            if result['metadata']:
                print(f"📋 Metadata:")
                for key, value in result['metadata'].items():
                    print(f"  {key}: {value}")
            else:
                print("  No metadata extracted")
            
            # Display processing info
            processing_info = result.get('processing_info', {})
            if processing_info:
                print(f"⏱️  Processing time: {processing_info.get('processing_time', 0):.2f}s")
                if processing_info.get('errors'):
                    print(f"⚠️  Errors: {processing_info['errors']}")
            
            results.append({
                'filename': filename,
                'success': True,
                'result': result
            })
            
        except Exception as e:
            print(f"❌ Error analyzing {filename}: {e}")
            results.append({
                'filename': filename,
                'success': False,
                'error': str(e)
            })
    
    # Print summary
    print("\n" + "="*60)
    print("📊 ANALYZER TEST SUMMARY")
    print("="*60)
    
    successful_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"Total tests: {total_tests}")
    print(f"Successful analyses: {successful_tests}")
    print(f"Success rate: {successful_tests/total_tests:.1%}")
    
    print("\nDetailed Results:")
    for result in results:
        status = "✅" if result['success'] else "❌"
        if result['success']:
            doc_type = result['result']['classification']['type']
            confidence = result['result']['classification']['confidence']
            print(f"{status} {result['filename']}: {doc_type} ({confidence:.1%})")
        else:
            print(f"{status} {result['filename']}: {result['error']}")
    
    # Save results
    if successful_tests > 0:
        successful_results = [r['result'] for r in results if r['success']]
        analyzer.save_results(successful_results, "test_analysis_results.json")
        print(f"\n💾 Results saved to: test_analysis_results.json")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    test_analyzer() 