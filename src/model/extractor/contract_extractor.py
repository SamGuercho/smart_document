"""
Specialized entity extractor for Contract documents.
"""

from typing import Dict, Any, List
import re, json
from datetime import datetime
from pathlib import Path
from .entity_extractor import BaseEntityExtractor
from ..types import DocumentType


class ContractExtractor(BaseEntityExtractor):
    """
    Entity extractor specialized for Contract documents.
    
    Extracts: parties, effective date, termination date, key terms
    """
    _document_type: DocumentType = DocumentType.CONTRACT
    _sys_prompt_name: str = "contract_entity_extract_system_prompt.txt"
    _user_prompt_name: str = "contract_entity_extract_user_prompt.txt"
    
    def __init__(self, llm_model: str = "gpt-4", api_key: str = None):
        super().__init__(DocumentType.CONTRACT, llm_model, api_key)
        self._sys_prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / self._sys_prompt_name
        self._user_prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / self._user_prompt_name
    
    def _setup_extraction_fields(self):
        """Setup extraction fields for contracts."""
        # Rule-based fields (easy to extract with patterns)
        self.rule_based_fields = [
            'parties',
            'effective_date',
            'termination_date',
            'contract_type'
        ]
        
        # LLM-based fields (complex, context-dependent)
        self.llm_based_fields = [
            'key_terms',
            'obligations',
            'payment_terms',
            'contract_value',
            'governing_law'
        ]
        
        self.extraction_fields = self.rule_based_fields + self.llm_based_fields
    
    def _extract_rule_based_entities(self, text_content: str) -> Dict[str, Any]:
        """
        Extract contract entities using rule-based methods.
        
        Args:
            text_content: Extracted text from the contract
            
        Returns:
            Dictionary of extracted entities
        """
        #TODO implement extract rules for simpler entities (ex: date) when the time to fine tune a model
        return {}
    
    def _extract_llm_entities(self, text_content: str, rule_based_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract complex contract entities using LLM-based methods.
        
        Args:
            text_content: Extracted text from the contract
            rule_based_results: Results from rule-based extraction
            
        Returns:
            Dictionary of extracted entities
        """
        # Create a specialized prompt for contract extraction
        instruction = self._create_contract_extract_sys_prompt()
        user_prompt = self._create_contract_extract_user_prompt(text_content)

        # Call LLM with the contract extraction prompt
        try:
            response = self.llm_extractor.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.llm_extractor.model_name,
                temperature=0.0,  # Use deterministic output for extraction
                max_tokens=2048,  # Allow sufficient tokens for detailed extraction
                timeout=self.settings.get('llm', {}).get('timeout', 30),
                stream=False
            )
            
            # Parse the JSON response
            extracted_entities = json.loads(response.choices[0].message.content)
            
            # Merge with rule-based results, preferring LLM results for overlapping fields
            #TODO here instead of merging, we should check if the LLM results are more accurate than the rule-based results
            entities = {**rule_based_results, **extracted_entities}
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"TODO add here a logging about JSONDecodeError: {str(e)}")
            entities = rule_based_results.copy()  # Fall back to rule-based results
        
        return entities
    
    def _create_contract_extract_sys_prompt(self, **kwargs) -> str:
        """Create specialized prompt for contract entity extraction."""
        # Load the system prompt template
        
        with open(self._sys_prompt_path) as f:
            prompt_template = f.read()
            
        # Format the prompt with the text content
        if kwargs:
            prompt = prompt_template.format(**kwargs)
        else:
            prompt = prompt_template
        
        return prompt
    
    def _create_contract_extract_user_prompt(self, text_content: str) -> str:
        """Create specialized prompt for contract entity extraction."""
        # Load the system prompt template
        
        with open(self._user_prompt_path) as f:
            prompt_template = f.read()

        prompt = prompt_template.format(
            contract_text=text_content
        )

        return prompt
    
    def _extract_key_terms_llm(self, text_content: str) -> List[str]:
        """Extract key terms using LLM."""
        # Placeholder implementation
        return []
    
    def _extract_obligations_llm(self, text_content: str) -> Dict[str, List[str]]:
        """Extract obligations using LLM."""
        # Placeholder implementation
        return {}
    
    def _extract_payment_terms_llm(self, text_content: str) -> Dict[str, Any]:
        """Extract payment terms using LLM."""
        # Placeholder implementation
        return {}
    
    def _extract_contract_value_llm(self, text_content: str) -> float:
        """Extract contract value using LLM."""
        # Placeholder implementation
        return 0.0
    
    def _extract_governing_law_llm(self, text_content: str) -> str:
        """Extract governing law using LLM."""
        # Placeholder implementation
        return "" 