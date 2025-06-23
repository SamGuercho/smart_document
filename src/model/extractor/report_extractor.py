"""
Specialized entity extractor for Financial Report documents.
"""

from typing import Dict, Any, List
import re
from datetime import datetime
import json
from pathlib import Path

from .entity_extractor import BaseEntityExtractor
from ..types import DocumentType


class ReportExtractor(BaseEntityExtractor):
    """
    Entity extractor specialized for Financial Report documents.
    
    Extracts: reporting period, key metrics, executive summary
    """
    _document_type: DocumentType = DocumentType.EARNINGS_REPORT
    _sys_prompt_name = "earnings_entity_extract_system_prompt.txt"
    _user_prompt_name = "earnings_entity_extract_user_prompt.txt"
    
    def __init__(self, llm_model: str = "gpt-4", api_key: str = None):
        super().__init__(DocumentType.EARNINGS_REPORT, llm_model, api_key)
        self._sys_prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / self._sys_prompt_name
        self._user_prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / self._user_prompt_name
    
    def _setup_extraction_fields(self):
        """Setup extraction fields for financial reports."""
        # Rule-based fields (easy to extract with patterns)
        self.rule_based_fields = [
            'reporting_period',
            'report_date',
            'company_name',
            'fiscal_year'
        ]
        
        # LLM-based fields (complex, context-dependent)
        self.llm_based_fields = [
            'key_metrics',
            'executive_summary',
            'financial_highlights',
            'risk_factors',
            'outlook'
        ]
        
        self.extraction_fields = self.rule_based_fields + self.llm_based_fields
    
    def _extract_rule_based_entities(self, text_content: str) -> Dict[str, Any]:
        """
        Extract report entities using rule-based methods.
        
        Args:
            text_content: Extracted text from the report
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        # TODO implement here a rule based extraction for the fields that are easy to extract with patterns
        
        return entities
    
    def _extract_llm_entities(self, text_content: str, rule_based_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract complex report entities using LLM-based methods.
        
        Args:
            text_content: Extracted text from the report
            rule_based_results: Results from rule-based extraction
            
        Returns:
            Dictionary of extracted entities
        """
        # Create a specialized prompt for report extraction
        sys_prompt = self._create_report_extract_sys_prompt()
        user_prompt = self._create_report_extract_user_prompt(text_content)
        
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
    
    def _create_report_extract_sys_prompt(self, **kwargs) -> str:
        """Create specialized prompt for report entity extraction."""
        with open(self._sys_prompt_path) as f:
            prompt = f.read()

        if kwargs:
            prompt = prompt.format(**kwargs)
        else:
            prompt = prompt

        return prompt
    
    def _create_report_extract_user_prompt(self, text_content: str) -> str:
        """Create specialized prompt for report entity extraction."""
        with open(self._user_prompt_path) as f:
            prompt = f.read()
        
        prompt = prompt.format(earnings_text=text_content)
        
        return prompt
    
    def _extract_key_metrics_llm(self, text_content: str) -> Dict[str, Any]:
        """Extract key metrics using LLM."""
        # Placeholder implementation
        return {}
    
    def _extract_executive_summary_llm(self, text_content: str) -> str:
        """Extract executive summary using LLM."""
        # Placeholder implementation
        return ""
    
    def _extract_financial_highlights_llm(self, text_content: str) -> List[str]:
        """Extract financial highlights using LLM."""
        # Placeholder implementation
        return []
    
    def _extract_risk_factors_llm(self, text_content: str) -> List[str]:
        """Extract risk factors using LLM."""
        # Placeholder implementation
        return []
    
    def _extract_outlook_llm(self, text_content: str) -> str:
        """Extract outlook using LLM."""
        # Placeholder implementation
        return "" 