"""
Pydantic schemas for request/response validation.

This module defines the strict data contracts between:
- Frontend and API (request/response)
- AI Agent and validation layer (output schema)

Key principle: Treat LLM output as untrusted until validated.
"""

from typing import Literal, List
from pydantic import BaseModel, Field, validator


class AnalysisResult(BaseModel):
    """
    Strict schema for AI analysis output.
    
    The AI must return JSON matching this exact structure.
    No hallucination allowed - agent can say "unknown" when uncertain.
    """
    summary: str = Field(
        ..., 
        description="Brief summary of the document (2-3 sentences max)",
        min_length=10,
        max_length=500
    )
    
    completeness_status: Literal["complete", "partial", "unknown"] = Field(
        ...,
        description="Assessment of document completeness"
    )
    
    missing_points: List[str] = Field(
        default_factory=list,
        description="List of missing sections or information. Empty if complete or unknown."
    )
    
    evidence: List[str] = Field(
        ...,
        description="Direct quotes or references from document supporting the analysis",
        min_items=1
    )
    
    confidence: float = Field(
        ...,
        description="Confidence score between 0.0 and 1.0",
        ge=0.0,
        le=1.0
    )
    
    @validator('missing_points')
    def validate_missing_points_with_status(cls, v, values):
        """
        Ensure missing_points is consistent with completeness_status.
        If status is 'complete', missing_points should be empty.
        """
        if 'completeness_status' in values:
            if values['completeness_status'] == 'complete' and len(v) > 0:
                raise ValueError("Cannot have missing_points when status is 'complete'")
        return v


class AnalyzeRequest(BaseModel):
    """
    Request model for document analysis endpoint.
    """
    document_text: str = Field(
        ...,
        description="The document text to analyze",
        min_length=20,
        max_length=10000  # Reasonable limit for demo purposes
    )


class AnalyzeResponse(BaseModel):
    """
    Response model for document analysis endpoint.
    
    Wraps AnalysisResult with additional metadata.
    """
    success: bool = Field(..., description="Whether analysis succeeded")
    result: AnalysisResult | None = Field(None, description="Analysis result if successful")
    error: str | None = Field(None, description="Error message if failed")
    
    @validator('result')
    def validate_result_with_success(cls, v, values):
        """Ensure result exists when success is True."""
        if values.get('success') and v is None:
            raise ValueError("Result must be provided when success is True")
        return v
