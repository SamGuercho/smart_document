#!/usr/bin/env python3
"""
Test script for LLMClassifier with PDF files
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
from model.classifier.llm_classifier import LLMClassifier

def test_llm_classifier():
    """Test the LLMClassifier with PDF files from resources/data."""
    
    # Load environment variables from project root
    load_dotenv(project_root / ".env")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("   You can create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    
    # Initialize the classifier
    print("🚀 Initializing LLMClassifier...")
    classifier = LLMClassifier(model_name="gpt-4")
    print("✅ LLMClassifier initialized successfully!")
    
    # Test PDFs with expected classifications
    test_files = [
        ("invoice1.pdf", "Invoice"),
        ("invoice2.pdf", "Invoice"),
        ("Contract.pdf", "Contract"),
        ("Earnings.pdf", "Earnings"),
    ]
    
    # Path to resources from tests directory
    data_dir = project_root / "src" / "resources" / "data"
    
    print("\n" + "="*60)
    print("📋 Testing LLMClassifier with PDF files...")
    print("="*60)
    
    results = []
    
    for filename, expected_type in test_files:
        pdf_path = data_dir / filename
        if not pdf_path.exists():
            print(f"❌ File not found: {filename}")
            continue
            
        print(f"\n📄 Testing: {filename}")
        print(f"🎯 Expected: {expected_type}")
        print("-" * 40)
        
        # Classify the document
        result = classifier.predict(pdf_path)
        logging.info(f"Results for {filename}: {result.raw_response}")
        
        # Extract results
        predicted_type = result.document_type.value
        confidence = result.confidence_score[predicted_type]
        
        print(f"✅ Predicted: {predicted_type}")
        print(f"📊 Confidence: {confidence:.2%}")
        
        # Check if prediction matches expected
        is_correct = False
        if predicted_type.lower() in expected_type.lower() or expected_type.lower() in predicted_type.lower():
            print("🎯 CORRECT!")
            is_correct = True
        else:
            print("❌ INCORRECT!")
        
        # Store results
        results.append({
            'filename': filename,
            'expected': expected_type,
            'predicted': predicted_type,
            'confidence': confidence,
            'is_correct': is_correct,
        })
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    correct_count = sum(1 for r in results if r['is_correct'])
    total_count = len(results)
    
    print(f"Total tests: {total_count}")
    print(f"Correct predictions: {correct_count}")
    print(f"Accuracy: {correct_count/total_count:.1%}")
    
    print("\nDetailed Results:")
    for result in results:
        status = "✅" if result['is_correct'] else "❌"
        print(f"{status} {result['filename']}: {result['expected']} → {result['predicted']} ({result['confidence']:.1%})")
    
    return correct_count == total_count

if __name__ == "__main__":
    print("🧪 LLMClassifier Test Suite")
    print("This will test the classifier with PDF files from resources/data/")
    print("\nPrerequisites:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set OpenAI API key in .env file")
    print("3. Ensure PDF files are in resources/data/")
    
    input("\nPress Enter to continue...")
    
    success = test_llm_classifier()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.") 