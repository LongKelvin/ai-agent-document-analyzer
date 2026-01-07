"""
LLM Service - Wrapper for Google Gemini API.

This module isolates LLM interaction logic and provides:
- Configuration management
- Error handling
- Response parsing
- JSON extraction from LLM output
"""

import json
import re
from typing import Dict, Any
import google.generativeai as genai
from app.config import settings


class GeminiService:
    """
    Service layer for Google Gemini API interaction.
    
    Responsibilities:
    - Configure Gemini API with appropriate settings
    - Send prompts and receive responses
    - Extract and parse JSON from LLM output
    - Handle API errors gracefully
    """
    
    def __init__(self):
        """
        Initialize Gemini API with configuration from settings.
        
        Low temperature (0.1-0.2) ensures:
        - Deterministic output
        - Less creativity, more accuracy
        - Better JSON compliance
        """
        genai.configure(api_key=settings.gemini_api_key)
        
        # Generation config for predictable, structured output
        self.generation_config = {
            "temperature": settings.temperature,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model_name,
            generation_config=self.generation_config
        )
    
    def generate_response(self, prompt: str) -> str:
        """
        Send prompt to Gemini and get raw response.
        
        Args:
            prompt: The complete prompt (system + user context)
            
        Returns:
            Raw text response from LLM
            
        Raises:
            Exception: If API call fails
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract and parse JSON from LLM response.
        
        LLMs sometimes wrap JSON in markdown code blocks or add text.
        This function handles common formats:
        - Plain JSON
        - JSON in ```json ... ``` blocks
        - JSON with surrounding text
        
        Args:
            response_text: Raw LLM response text
            
        Returns:
            Parsed JSON as dictionary
            
        Raises:
            ValueError: If no valid JSON found
        """
        # Try to find JSON in markdown code block
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON object
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                # Assume entire response is JSON
                json_str = response_text.strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from LLM response: {str(e)}\nResponse: {response_text[:200]}...")
    
    def generate_structured_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate response and extract JSON in one call.
        
        Convenience method combining generate_response and extract_json_from_response.
        
        Args:
            prompt: The complete prompt
            
        Returns:
            Parsed JSON dictionary
        """
        raw_response = self.generate_response(prompt)
        return self.extract_json_from_response(raw_response)


# Singleton instance for reuse across requests
_gemini_service_instance = None


def get_gemini_service() -> GeminiService:
    """
    Get singleton instance of GeminiService.
    
    Avoids recreating model on every request.
    """
    global _gemini_service_instance
    if _gemini_service_instance is None:
        _gemini_service_instance = GeminiService()
    return _gemini_service_instance
