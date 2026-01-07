"""
AI Agent orchestration logic.

This module coordinates:
- RAG retrieval (embeddings)
- Prompt construction
- LLM invocation
- Output validation

The agent treats the LLM as untrusted and validates all output.
"""

from typing import Dict, Any
from pydantic import ValidationError

from app.models.schemas import AnalysisResult
from app.services.llm import get_gemini_service
from app.services.embeddings import get_embedding_service
from app.agent.prompts import build_complete_prompt


class DocumentAnalysisAgent:
    """
    AI Agent for document analysis.
    
    This agent demonstrates the key principles:
    1. Retrieval-Augmented Generation (RAG)
    2. Structured output with Pydantic validation
    3. Treating LLM output as untrusted
    4. Evidence-based reasoning
    """
    
    def __init__(self):
        """
        Initialize agent with required services.
        
        Services are injected via singletons for efficiency.
        """
        self.llm_service = get_gemini_service()
        self.embedding_service = get_embedding_service()
    
    def analyze_document(self, document_text: str) -> AnalysisResult:
        """
        Analyze a document for completeness and clarity.
        
        Process:
        1. Retrieve relevant guidelines using embeddings (RAG)
        2. Build prompt with guidelines and document
        3. Get LLM response as JSON
        4. Validate output with Pydantic
        5. Return validated result
        
        Args:
            document_text: The document to analyze
            
        Returns:
            Validated AnalysisResult
            
        Raises:
            ValidationError: If LLM output doesn't match schema
            ValueError: If JSON parsing fails
            Exception: If LLM API fails
        """
        # Step 1: RAG - Retrieve relevant guidelines
        # This is semantic search using embeddings
        relevant_guidelines = self.embedding_service.retrieve_relevant_guidelines(
            query=document_text,
            top_k=2  # Get 2 most relevant guidelines
        )
        
        # Step 2: Build complete prompt
        # Inject retrieved context and document into prompt template
        prompt = build_complete_prompt(
            document_text=document_text,
            retrieved_guidelines=relevant_guidelines
        )
        
        # Step 3: Get LLM response
        # LLM is instructed to return JSON only
        response_json = self.llm_service.generate_structured_response(prompt)
        
        # Step 4: Validate output with Pydantic
        # This is where we treat LLM output as untrusted
        # If validation fails, Pydantic raises ValidationError
        try:
            result = AnalysisResult(**response_json)
        except ValidationError as e:
            # Add context to validation error
            raise ValidationError(
                f"LLM output validation failed. "
                f"Output: {response_json}. "
                f"Errors: {e.errors()}"
            )
        
        # Step 5: Return validated result
        # At this point, we trust the data because Pydantic validated it
        return result


# Singleton instance
_agent_instance = None


def get_document_analysis_agent() -> DocumentAnalysisAgent:
    """
    Get singleton instance of DocumentAnalysisAgent.
    
    Reuses services across requests for efficiency.
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = DocumentAnalysisAgent()
    return _agent_instance
