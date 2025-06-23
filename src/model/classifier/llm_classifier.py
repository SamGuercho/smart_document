"""
LLM-based document classifier using OpenAI API.
"""

import os
import json
import logging
import math
from typing import Dict, Any, List, Optional
from pathlib import Path
from openai import OpenAI

from .base import BaseClassifier
from ..types import ClassificationResult, DocumentType
from ..config.settings import get_settings
from ..extractor.pdf_extractor import PDFExtractor

logger = logging.getLogger(__name__)


class LLMClassifier(BaseClassifier):
    """
    LLM-based document classifier using OpenAI API.
    """
    
    def __init__(self, model_name: str = None, api_key: str = None, **kwargs):
        """
        Initialize the LLM classifier.
        
        Args:
            model_name: Name of the LLM to use (e.g., "gpt-4", "claude-3")
            api_key: API key for the LLM service
            **kwargs: Additional configuration parameters
        """
        super().__init__()
        
        # Get settings
        self.settings = get_settings()
        
        # Use settings if not provided
        if model_name is None:
            model_name = self.settings.get("llm.model_name")
        if api_key is None:
            api_key = self.settings.get("openai.api_key")
        
        self.model_name = model_name
        self.api_key = api_key
        
        # Initialize OpenAI client
        self.client = self._initialize_client()
        
        # Initialize PDF extractor for text extraction
        self.pdf_extractor = PDFExtractor()
        
        # Load prompts
        self.system_prompt = self._load_system_prompt()
        self.user_prompt_template = self._load_user_prompt()
    
    def _initialize_client(self):
        """Initialize the OpenAI client."""
        if not self.api_key:
            logger.warning("No API key provided - LLM classification will not work")
            return None
        
        try:
            return OpenAI(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            return None
    
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
    
    def _load_system_prompt(self):
        """Load system prompt from resources."""
        prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / "classification_system_prompt.txt"
        with open(prompt_path, "r") as f:
            return f.read().strip()

    def _load_user_prompt(self):
        """Load user prompt template from resources."""
        prompt_path = Path(__file__).parent.parent.parent / "resources" / "prompts" / "classification_user_prompt.txt"
        with open(prompt_path, "r") as f:
            return f.read().strip()

    def predict(self, document_path: str) -> ClassificationResult:
        text = self._extract_text_from_pdf(Path(document_path))
        # Escape any curly braces in the text to avoid format errors
        escaped_text = text[:5000].replace("{", "{{").replace("}", "}}")
        user_prompt = self.user_prompt_template.format(document_content=escaped_text)
        
        # Use chat completions API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1,
            temperature=0,
            # Get logprobs for the response tokens
            logprobs=True,
            top_logprobs=20
        )
        
        content = response.choices[0].message.content.strip()
        token_confidences = {
            logprob.token: math.exp(logprob.logprob)  # Convert log probability to confidence
            for logprob in response.choices[0].logprobs.content[0].top_logprobs
        }

        # for each document type, get the confidence score
        # Initialize confidence scores for all document types to 0
        type_confidences = {doc_type.value: 0.0 for doc_type in DocumentType}
        # Update confidence scores from token probabilities
        for doc_type, confidence in token_confidences.items():
            if doc_type in type_confidences:
                type_confidences[doc_type] = confidence
        
        return ClassificationResult(
                document_type=DocumentType(max(type_confidences.items(), key=lambda x: x[1])[0]),
                confidence_score=type_confidences,
                raw_response=content)
    
    def predict_batch(self, document_paths: List[str]) -> List[ClassificationResult]:
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
        return self.pdf_extractor.extract_text(pdf_path)
    
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