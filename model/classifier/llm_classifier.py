"""
LLM-based document classifier using language models.
"""

from typing import Union, List, Dict, Any
from pathlib import Path
import os
from dotenv import load_dotenv
import openai
import json

from .base import BaseClassifier
from ..types import DocumentType, ClassificationResult
from ..extractor.pdf_extractor import PDFExtractor

PROMPT_PATH = Path(__file__).parent.parent.parent / "resources" / "prompts"
SYSTEM_PROMPT_PATH = PROMPT_PATH / "classification_system_prompts.txt"
USER_PROMPT_PATH = PROMPT_PATH / "classification_user_prompt.txt"
CATEGORIES = ["Invoice", "Contract", "Business Report"]

class LLMClassifier(BaseClassifier):
    """
    Document classifier using Large Language Models.
    
    This classifier leverages LLMs like GPT, Claude, or other language models
    to classify documents based on their content and structure.
    """
    
    def __init__(self, model_name: str = "gpt-4", api_key: str = None, **kwargs):
        """
        Initialize the LLM classifier.
        
        Args:
            model_name: Name of the LLM to use (e.g., "gpt-4", "claude-3")
            api_key: API key for the LLM service
            **kwargs: Additional configuration parameters
        """
        super().__init__()
        self.model_name = model_name
        self.api_key = api_key
        self.config = kwargs
        self._system_prompt = self._load_prompt("classification_system_prompt.txt")  # Load system prompt once
        self._user_prompt_template = self._load_prompt("classification_user_prompt.txt")  # Load user prompt template once
        self.client = self._get_openai_client()  # Initialize client once
        self._pdf_extractor = PDFExtractor()  # Add PDF extractor
    
    def train(self, training_data: List[tuple], **kwargs) -> None:
        """
        Fine-tune or configure the LLM classifier.
        
        For LLM classifiers, this might involve:
        - Creating few-shot examples
        - Setting up prompts
        - Configuring model parameters
        
        Args:
            training_data: List of (document_path, document_type) tuples
            **kwargs: Additional training parameters
        """
        # Implementation for LLM training/fine-tuning
        pass
    
    def _load_prompt(self, filename: str) -> str:
        """
        Load a prompt file from the prompts directory.
        
        Args:
            filename: Name of the prompt file to load
            
        Returns:
            String content of the prompt file
        """
        prompt_path = PROMPT_PATH / filename
        with open(prompt_path, "r") as f:
            return f.read().strip()

    def _get_openai_client(self):
        load_dotenv()
        api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = api_key
        return openai

    def predict(self, document_path: Union[str, Path]) -> Dict[str, Any]:
        text = self._extract_text_from_pdf(Path(document_path))
        user_prompt = self._user_prompt_template.format(DOCUMENT_CONTENT=text[:2000])
        
        response = self.client.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=200,
            logprobs=True,
            temperature=0
        )
        
        content = response['choices'][0]['message']['content']
        logprobs = response['choices'][0].get('logprobs', {})
        
        # Parse JSON response
        try:
            result = json.loads(content)
            doc_type = result.get('document_type', 'unknown')
            confidence = result.get('confidence', 0) / 100.0  # Convert to 0-1 scale
            justification = result.get('justification', '')
            
            # Map to DocumentType enum
            if doc_type == "Invoice":
                enum_type = DocumentType.INVOICE
            elif doc_type == "Contract":
                enum_type = DocumentType.CONTRACT
            elif doc_type == "Business Report":
                enum_type = DocumentType.EARNINGS_REPORT  # Assuming this maps to Business Report
            else:
                enum_type = DocumentType.UNKNOWN
                
        except (json.JSONDecodeError, KeyError) as e:
            # Fallback parsing if JSON fails
            enum_type = DocumentType.UNKNOWN
            confidence = 0.0
            justification = f"Failed to parse response: {str(e)}"
        
        return {
            "result": ClassificationResult(
                document_type=enum_type, 
                confidence_score=confidence
            ),
            "logprobs": logprobs,
            "justification": justification,
            "raw_response": content
        }
    
    def predict_batch(self, document_paths: List[Union[str, Path]]) -> List[ClassificationResult]:
        """
        Classify multiple documents using LLM.
        
        Args:
            document_paths: List of document paths to classify
            
        Returns:
            List of ClassificationResult objects
        """
        # Implementation for batch LLM classification
        pass
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from PDF for LLM processing.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        return self.pdf_extractor.extract_text_chunk(pdf_path, max_chars=2000)
    
    def _create_classification_prompt(self, text_content: str) -> str:
        """
        Create a prompt for document classification.
        
        Args:
            text_content: Extracted text from the document
            
        Returns:
            Formatted prompt for the LLM
        """
        # Implementation for prompt creation
        pass
    
    def _parse_llm_response(self, response: str) -> ClassificationResult:
        """
        Parse LLM response into ClassificationResult.
        
        Args:
            response: Raw response from the LLM
            
        Returns:
            Parsed ClassificationResult
        """
        # Implementation for response parsing
        pass 