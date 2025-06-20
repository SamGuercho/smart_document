#!/usr/bin/env python3
"""
Test script for LLMClassifier with PDF files
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the model directory to Python path
sys.path.append(str(Path(__file__).parent / "model"))

from classifier.llm_classifier import LLMClassifier

def test_llm_classifier():
    """Test the LLMClassifier with PDF files from resources/data."""
    
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("   You can create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    
    # Initialize the classifier
    print("🚀 Initializing LLMClassifier...")
    try:
        classifier = LLMClassifier(model_name="gpt-4")
        print("✅ LLMClassifier initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize LLMClassifier: {e}")
        return False
    
    # Test PDFs with expected classifications
    test_files = [
        ("Contract.pdf", "Contract"),
        ("Earnings.pdf", "Business Report"), 
        ("invoice1.pdf", "Invoice"),
        ("invoice2.pdf", "Invoice")
    ]
    
    data_dir = Path("resources/data")
    
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
        
        try:
            # Classify the document
            result = classifier.predict(pdf_path)
            
            # Extract results
            predicted_type = result["result"].document_type.value
            confidence = result["result"].confidence_score
            justification = result["justification"]
            logprobs = result["logprobs"]
            
            print(f"✅ Predicted: {predicted_type}")
            print(f"📊 Confidence: {confidence:.2%}")
            print(f"💭 Justification: {justification}")
            
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
                'justification': justification
            })
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            results.append({
                'filename': filename,
                'expected': expected_type,
                'predicted': 'ERROR',
                'confidence': 0.0,
                'is_correct': False,
                'justification': f"Error: {str(e)}"
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
    print("Make sure you have:")
    print("1. OpenAI API key in .env file")
    print("2. Required packages installed (openai, python-dotenv, PyPDF2)")
    print("3. PDF files in resources/data/")
    
    input("\nPress Enter to continue...")
    
    success = test_llm_classifier()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")