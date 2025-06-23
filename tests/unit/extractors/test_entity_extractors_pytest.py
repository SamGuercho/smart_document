"""
Pytest tests for Entity Extractors
"""

import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from model.extractor.contract_extractor import ContractExtractor
from model.extractor.invoice_extractor import InvoiceExtractor
from model.extractor.report_extractor import ReportExtractor

# Load environment variables
load_dotenv(project_root / ".env")

@pytest.fixture
def data_dir():
    """Get the data directory path."""
    return project_root / "src" / "resources" / "data"

@pytest.fixture
def contract_pdf(data_dir):
    """Get the contract PDF path."""
    return data_dir / "Contract.pdf"

@pytest.fixture
def invoice_pdfs(data_dir):
    """Get the invoice PDF paths."""
    return [data_dir / "invoice1.pdf", data_dir / "invoice2.pdf"]

@pytest.fixture
def earnings_pdf(data_dir):
    """Get the earnings PDF path."""
    return data_dir / "Earnings.pdf"

class TestContractExtractor:
    """Test cases for ContractExtractor."""
    
    def test_contract_extractor_initialization(self):
        """Test that ContractExtractor can be initialized."""
        extractor = ContractExtractor()
        assert extractor is not None
        assert extractor.document_type.value == "contract"
    
    def test_contract_extractor_fields_setup(self):
        """Test that extraction fields are properly set up."""
        extractor = ContractExtractor()
        assert hasattr(extractor, 'rule_based_fields')
        assert hasattr(extractor, 'llm_based_fields')
        assert hasattr(extractor, 'extraction_fields')
        assert len(extractor.extraction_fields) > 0
    
    def test_contract_extraction(self, contract_pdf):
        """Test contract entity extraction."""
        if not contract_pdf.exists():
            pytest.skip(f"Contract PDF not found: {contract_pdf}")
        
        extractor = ContractExtractor()
        result = extractor.extract(contract_pdf)
        
        # Basic assertions
        assert result is not None
        assert result.metadata is not None
        assert result.metadata.document_type.value == "contract"
        assert result.processing_time >= 0
        
        # Check that extraction completed (even if no entities found)
        assert result.extraction_method == "hybrid_entity_extraction"
        
        print(f"\nContract extraction results:")
        print(f"  Confidence: {result.metadata.confidence_score:.2%}")
        print(f"  Processing time: {result.processing_time:.2f}s")
        print(f"  Entities extracted: {len(result.metadata.additional_fields) if result.metadata.additional_fields else 0}")
        if result.errors:
            print(f"  Errors: {result.errors}")

class TestInvoiceExtractor:
    """Test cases for InvoiceExtractor."""
    
    def test_invoice_extractor_initialization(self):
        """Test that InvoiceExtractor can be initialized."""
        extractor = InvoiceExtractor()
        assert extractor is not None
        assert extractor.document_type.value == "invoice"
    
    def test_invoice_extractor_fields_setup(self):
        """Test that extraction fields are properly set up."""
        extractor = InvoiceExtractor()
        assert hasattr(extractor, 'rule_based_fields')
        assert hasattr(extractor, 'llm_based_fields')
        assert hasattr(extractor, 'extraction_fields')
        assert len(extractor.extraction_fields) > 0
    
    @pytest.mark.parametrize("invoice_index", [0, 1])
    def test_invoice_extraction(self, invoice_pdfs, invoice_index):
        """Test invoice entity extraction."""
        if invoice_index >= len(invoice_pdfs):
            pytest.skip(f"Invoice PDF {invoice_index} not available")
        
        invoice_pdf = invoice_pdfs[invoice_index]
        if not invoice_pdf.exists():
            pytest.skip(f"Invoice PDF not found: {invoice_pdf}")
        
        extractor = InvoiceExtractor()
        result = extractor.extract(invoice_pdf)
        
        # Basic assertions
        assert result is not None
        assert result.metadata is not None
        assert result.metadata.document_type.value == "invoice"
        assert result.processing_time >= 0
        
        # Check that extraction completed (even if no entities found)
        assert result.extraction_method == "hybrid_entity_extraction"
        
        print(f"\nInvoice extraction results ({invoice_pdf.name}):")
        print(f"  Confidence: {result.metadata.confidence_score:.2%}")
        print(f"  Processing time: {result.processing_time:.2f}s")
        print(f"  Entities extracted: {len(result.metadata.additional_fields) if result.metadata.additional_fields else 0}")
        if result.errors:
            print(f"  Errors: {result.errors}")

class TestReportExtractor:
    """Test cases for ReportExtractor."""
    
    def test_report_extractor_initialization(self):
        """Test that ReportExtractor can be initialized."""
        extractor = ReportExtractor()
        assert extractor is not None
        assert extractor.document_type.value == "earnings_report"
    
    def test_report_extractor_fields_setup(self):
        """Test that extraction fields are properly set up."""
        extractor = ReportExtractor()
        assert hasattr(extractor, 'rule_based_fields')
        assert hasattr(extractor, 'llm_based_fields')
        assert hasattr(extractor, 'extraction_fields')
        assert len(extractor.extraction_fields) > 0
    
    def test_report_extraction(self, earnings_pdf):
        """Test report entity extraction."""
        if not earnings_pdf.exists():
            pytest.skip(f"Earnings PDF not found: {earnings_pdf}")
        
        extractor = ReportExtractor()
        result = extractor.extract(earnings_pdf)
        
        # Basic assertions
        assert result is not None
        assert result.metadata is not None
        assert result.metadata.document_type.value == "earnings_report"
        assert result.processing_time >= 0
        
        # Check that extraction completed (even if no entities found)
        assert result.extraction_method == "hybrid_entity_extraction"
        
        print(f"\nReport extraction results:")
        print(f"  Confidence: {result.metadata.confidence_score:.2%}")
        print(f"  Processing time: {result.processing_time:.2f}s")
        print(f"  Entities extracted: {len(result.metadata.additional_fields) if result.metadata.additional_fields else 0}")
        if result.errors:
            print(f"  Errors: {result.errors}")

class TestExtractorIntegration:
    """Integration tests for all extractors."""
    
    def test_all_extractors_with_same_file(self, contract_pdf):
        """Test that all extractors can process the same file (they should handle it differently)."""
        if not contract_pdf.exists():
            pytest.skip(f"Contract PDF not found: {contract_pdf}")
        
        extractors = [
            ContractExtractor(),
            InvoiceExtractor(),
            ReportExtractor()
        ]
        
        results = []
        for extractor in extractors:
            result = extractor.extract(contract_pdf)
            results.append(result)
            
            # Each should complete without crashing
            assert result is not None
            assert result.metadata is not None
            assert result.processing_time >= 0
        
        # All should have different document types
        doc_types = [r.metadata.document_type.value for r in results]
        assert len(set(doc_types)) == 3  # All different
        
        print(f"\nIntegration test results:")
        for i, (extractor, result) in enumerate(zip(extractors, results)):
            print(f"  {type(extractor).__name__}: {result.metadata.document_type.value}, "
                  f"confidence: {result.metadata.confidence_score:.2%}") 