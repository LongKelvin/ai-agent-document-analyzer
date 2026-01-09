"""
LLM Service using LangChain - Educational Version

WHAT IS THIS FILE?
This replaces the custom GeminiService (llm.py) with LangChain's ChatGoogleGenerativeAI.

WHY USE LANGCHAIN?
- Provides a standardized interface for LLM interactions
- Easier to swap between different LLM providers (OpenAI, Anthropic, etc.)
- Built-in prompt templates and output parsers
- Better error handling and retry logic

WHAT CHANGED?
Before: We manually called google.generativeai and parsed JSON from responses
After: LangChain handles the API calls, we focus on prompts and validation
"""

from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel

from app.config import settings


class LangChainLLMService:
    """
    LangChain-based LLM service for Google Gemini.
    
    KEY CONCEPTS:
    1. ChatGoogleGenerativeAI: LangChain's wrapper for Google Gemini API
    2. ChatPromptTemplate: Structured way to build prompts (system + user messages)
    3. JsonOutputParser: Automatically parses LLM JSON responses
    4. LCEL (LangChain Expression Language): Chains components together with | operator
    
    BENEFITS:
    - Cleaner code: No manual JSON parsing
    - Type safety: Pydantic schemas enforce structure
    - Flexibility: Easy to add more steps (validation, retries, etc.)
    - Standardization: Same pattern works with any LLM provider
    """
    
    def __init__(self):
        """
        Initialize LangChain LLM with Google Gemini.
        
        BEHIND THE SCENES:
        - ChatGoogleGenerativeAI creates a connection to Gemini API
        - temperature=0.1 ensures deterministic, factual output (not creative)
        - model_name can be any Gemini model (gemini-pro, gemini-2.5-flash, etc.)
        """
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model_name,
            temperature=settings.temperature,
            google_api_key=settings.gemini_api_key,
            max_output_tokens=2048,
        )
        
        print(f"[LangChain LLM] Initialized with model: {settings.gemini_model_name}")
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate raw text response from LLM.
        
        WHAT HAPPENS:
        1. Your prompt is sent to Gemini API via LangChain
        2. LangChain handles HTTP requests, retries, error handling
        3. Response text is returned
        
        This is equivalent to the old GeminiService.generate_response()
        but with better error handling built-in.
        
        Args:
            prompt: Complete prompt string
            
        Returns:
            Raw text response
        """
        try:
            # Invoke the LLM with the prompt
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            raise Exception(f"LangChain LLM error: {str(e)}")
    
    def generate_structured_response(
        self, 
        system_prompt: str, 
        user_prompt: str,
        output_schema: Optional[BaseModel] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response using LangChain's chain pattern.
        
        THIS IS THE MAGIC OF LANGCHAIN:
        Instead of manually extracting JSON from text, we build a "chain":
        
        Prompt Template -> LLM -> JSON Parser -> Validated Output
        
        LCEL (LangChain Expression Language) lets us write this as:
        chain = prompt | llm | parser
        
        The | operator means "pipe the output from left to right"
        
        BEHIND THE SCENES:
        1. ChatPromptTemplate formats your prompts into proper messages
        2. LLM generates response
        3. JsonOutputParser extracts and validates JSON
        4. (Optional) Pydantic schema validates the structure
        
        Args:
            system_prompt: Instructions for the AI (its role and rules)
            user_prompt: The actual task/document to process
            output_schema: Optional Pydantic model for validation
            
        Returns:
            Parsed and validated JSON dictionary
        """
        try:
            # Step 1: Create prompt template
            # This is cleaner than string concatenation
            prompt_template = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template("{system_instructions}"),
                HumanMessagePromptTemplate.from_template("{user_input}")
            ])
            
            # Step 2: Create JSON parser
            # This automatically extracts JSON from LLM responses
            # Even if LLM wraps it in markdown or adds extra text
            json_parser = JsonOutputParser()
            
            # Step 3: Build the chain using LCEL
            # Read as: "Format prompt, send to LLM, parse as JSON"
            chain = prompt_template | self.llm | json_parser
            
            # Step 4: Execute the chain
            result = chain.invoke({
                "system_instructions": system_prompt,
                "user_input": user_prompt
            })
            
            # Step 5: (Optional) Validate with Pydantic schema
            if output_schema:
                validated = output_schema(**result)
                return validated.model_dump()
            
            return result
            
        except Exception as e:
            raise ValueError(f"Structured response generation failed: {str(e)}")
    
    def create_custom_chain(self, prompt_template: ChatPromptTemplate, parser=None):
        """
        Create a reusable chain for specific tasks.
        
        ADVANCED PATTERN:
        Instead of calling generate_structured_response each time,
        you can create a chain once and reuse it many times.
        
        This is more efficient and follows LangChain best practices.
        
        Example usage:
        ```python
        template = ChatPromptTemplate.from_messages([...])
        qa_chain = llm_service.create_custom_chain(template, JsonOutputParser())
        
        # Use the chain multiple times
        answer1 = qa_chain.invoke({"question": "What is RAG?"})
        answer2 = qa_chain.invoke({"question": "What is embedding?"})
        ```
        
        Args:
            prompt_template: LangChain prompt template
            parser: Optional output parser (JsonOutputParser, StrOutputParser, etc.)
            
        Returns:
            Executable LangChain chain
        """
        if parser:
            return prompt_template | self.llm | parser
        else:
            return prompt_template | self.llm


# Singleton instance for reuse
_langchain_llm_service = None


def get_langchain_llm_service() -> LangChainLLMService:
    """
    Get singleton instance of LangChainLLMService.
    
    WHY SINGLETON?
    Creating LLM connections is expensive (API setup, model loading).
    By reusing one instance, we save time and resources.
    
    This is the same pattern used in the original llm.py
    """
    global _langchain_llm_service
    if _langchain_llm_service is None:
        _langchain_llm_service = LangChainLLMService()
    return _langchain_llm_service
