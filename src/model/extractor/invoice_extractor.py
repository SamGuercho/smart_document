"""
Specialized entity extractor for Invoice documents.
"""

from typing import Dict, Any, List
import re
from datetime import datetime
from pathlib import Path
import json

from .entity_extractor import BaseEntityExtractor
from ..types import DocumentType


class InvoiceExtractor(BaseEntityExtractor):
    """
    Entity extractor specialized for Invoice documents.
    
    Extracts: vendor, amount, due date, line items
    """
    _document_type: DocumentType = DocumentType.INVOICE
    _sys_prompt_name: str = "invoice_entity_extract_system_prompt.txt"
    _user_prompt_name: str = "invoice_entity_extract_user_prompt.txt"
    
    
    def __init__(self, llm_model: str = "gpt-4", api_key: str = None):
        super().__init__(DocumentType.INVOICE, llm_model, api_key)
        self._sys_prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / self._sys_prompt_name
        self._user_prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / self._user_prompt_name
    
    def _setup_extraction_fields(self):
        """Setup extraction fields for invoices."""
        # Rule-based fields (easy to extract with patterns)
        self.rule_based_fields = [
            'vendor_name',
            'total_amount', 
            'currency',
            'invoice_date',
            'due_date'
        ]
        
        # LLM-based fields (complex, context-dependent)
        self.llm_based_fields = [
            'line_items',
            'vendor_details',
            'payment_terms',
            'invoice_number'
        ]
        
        self.extraction_fields = self.rule_based_fields + self.llm_based_fields
    
    def _extract_rule_based_entities(self, text_content: str) -> Dict[str, Any]:
        """
        Extract invoice entities using rule-based methods.
        
        Args:
            text_content: Extracted text from the invoice
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        # TODO implement a rule based extraction for the fields that are easy to extract with patterns.
        # # Extract vendor name
        # vendor_patterns = [
        #     r'(?:From|Vendor|Bill From|Company)[:\s]*(.+?)(?:\n|$)',
        #     r'(?:Invoice from|Billed by)[:\s]*(.+?)(?:\n|$)',
        #     r'^([A-Z][A-Za-z\s&.,]+(?:Inc|Corp|LLC|Ltd|Company))'
        # ]
        
        # for pattern in vendor_patterns:
        #     match = re.search(pattern, text_content, re.IGNORECASE | re.MULTILINE)
        #     if match:
        #         entities['vendor_name'] = match.group(1).strip()
        #         break
        
        # # Extract total amount
        # amount_patterns = [
        #     r'(?:Total|Amount Due|Grand Total)[:\s]*\$?\s*([\d,]+\.?\d*)',
        #     r'\$?\s*([\d,]+\.?\d*)\s*(?:USD|EUR|GBP)?\s*(?:Total|Due)',
        #     r'(?:Total Amount)[:\s]*\$?\s*([\d,]+\.?\d*)'
        # ]
        
        # for pattern in amount_patterns:
        #     match = re.search(pattern, text_content, re.IGNORECASE)
        #     if match:
        #         amount_str = match.group(1).replace(',', '')
        #         try:
        #             entities['total_amount'] = float(amount_str)
        #             break
        #         except ValueError:
        #             continue
        
        # # Extract currency
        # currency_patterns = [
        #     r'\$([\d,]+\.?\d*)',
        #     r'([\d,]+\.?\d*)\s*(USD|EUR|GBP)',
        #     r'(USD|EUR|GBP)\s*([\d,]+\.?\d*)'
        # ]
        
        # for pattern in currency_patterns:
        #     match = re.search(pattern, text_content, re.IGNORECASE)
        #     if match:
        #         if '$' in pattern:
        #             entities['currency'] = 'USD'
        #         elif match.group(1) in ['USD', 'EUR', 'GBP']:
        #             entities['currency'] = match.group(1)
        #         elif match.group(2) in ['USD', 'EUR', 'GBP']:
        #             entities['currency'] = match.group(2)
        #         break
        
        # # Extract invoice date
        # date_patterns = [
        #     r'(?:Invoice Date|Date|Issued)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        #     r'(?:Invoice Date|Date|Issued)[:\s]*(\d{4}-\d{2}-\d{2})',
        #     r'(?:Invoice Date|Date|Issued)[:\s]*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})'
        # ]
        
        # for pattern in date_patterns:
        #     match = re.search(pattern, text_content, re.IGNORECASE)
        #     if match:
        #         try:
        #             date_str = match.group(1)
        #             # Parse date string (simplified - you'd want more robust date parsing)
        #             entities['invoice_date'] = date_str
        #             break
        #         except:
        #             continue
        
        # # Extract due date
        # due_date_patterns = [
        #     r'(?:Due Date|Payment Due|Pay By)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        #     r'(?:Due Date|Payment Due|Pay By)[:\s]*(\d{4}-\d{2}-\d{2})',
        #     r'(?:Due Date|Payment Due|Pay By)[:\s]*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})'
        # ]
        
        # for pattern in due_date_patterns:
        #     match = re.search(pattern, text_content, re.IGNORECASE)
        #     if match:
        #         try:
        #             date_str = match.group(1)
        #             entities['due_date'] = date_str
        #             break
        #         except:
        #             continue
        
        return entities
    
    def _extract_llm_entities(self, text_content: str, rule_based_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract complex invoice entities using LLM-based methods.
        
        Args:
            text_content: Extracted text from the invoice
            rule_based_results: Results from rule-based extraction
            
        Returns:
            Dictionary of extracted entities
        """
        # Create a specialized prompt for invoice extraction
        sys_prompt = self._create_invoice_extract_sys_prompt()
        user_prompt = self._create_invoice_extract_user_prompt(text_content)
        
        # Use LLM to extract complex entities
        try:
            response = self.llm_extractor.client.chat.completions.create(
                messages=[      
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.llm_extractor.model_name,
                temperature=0.0,  # Use deterministic output for extraction
                max_tokens=2048,  # Allow sufficient tokens for detailed extraction
                timeout=self.settings.get('llm', {}).get('timeout', 30),
                stream=False
            )
            extracted_entities = json.loads(response.choices[0].message.content)
            entities = {**rule_based_results, **extracted_entities}
        except Exception as e:
            print(f"TODO add here a logging about Exception: {str(e)}")
            entities = {**rule_based_results}

        return entities
    
    def _create_invoice_extract_sys_prompt(self, **kwargs) -> str:
        """Create specialized prompt for invoice entity extraction."""
        with open(self._sys_prompt_path) as f:
            prompt = f.read()

        if kwargs:
            prompt = prompt.format(**kwargs)
        else:
            prompt = prompt

        return prompt
    
    def _create_invoice_extract_user_prompt(self, text_content: str) -> str:
        """Create specialized prompt for invoice entity extraction."""
        with open(self._user_prompt_path) as f:
            prompt = f.read()

        prompt = prompt.format(invoice_text=text_content)
        return prompt
    
    def _extract_line_items_llm(self, text_content: str) -> List[Dict]:
        """Extract line items using LLM."""
        # Placeholder implementation
        return []
    
    def _extract_vendor_details_llm(self, text_content: str) -> Dict[str, str]:
        """Extract vendor details using LLM."""
        # Placeholder implementation
        return {}
    
    def _extract_payment_terms_llm(self, text_content: str) -> str:
        """Extract payment terms using LLM."""
        # Placeholder implementation
        return ""
    
    def _extract_invoice_number_llm(self, text_content: str) -> str:
        """Extract invoice number using LLM."""
        # Placeholder implementation
        return "" 