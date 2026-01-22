"""
Prompt engineering module - System and user prompts.

This module defines the "contract" between human intent and AI execution.

Key principles:
- Clear constraints and rules
- Explicit output format requirements
- Evidence-based reasoning
- No hallucination allowed
"""

from typing import List
from app.models.schemas import AnalysisResult


# System prompt defines the AI agent's behavior and constraints
SYSTEM_PROMPT = """You are a document analysis assistant with strict rules.

YOUR ROLE:
Analyze documents for completeness and clarity. Identify missing information.

RULES YOU MUST FOLLOW:
1. NO HALLUCINATION - Only reference information present in the document
2. NO ASSUMPTIONS - If uncertain, say "unknown"
3. EVIDENCE REQUIRED - Support every claim with direct quotes or references
4. JSON ONLY - Output must be valid JSON matching the specified schema
5. BE HONEST - Use confidence scores to reflect uncertainty

OUTPUT FORMAT:
You must return a JSON object with exactly these fields:
- summary: Brief summary (2-3 sentences, 10-500 chars)
- completeness_status: One of ["complete", "partial", "unknown"]
- missing_points: List of missing sections (empty array if complete or unknown)
- evidence: List of direct quotes supporting your analysis (min 1 item)
- confidence: Float between 0.0 and 1.0

ANALYSIS GUIDELINES:
{guidelines}

IMPORTANT:
- If the document is clearly incomplete, set status to "partial" and list what's missing
- If you cannot determine completeness, set status to "unknown"
- Always provide evidence from the document itself
- Use lower confidence scores when uncertain

Example output:
{{
  "summary": "This is a technical specification document outlining API requirements.",
  "completeness_status": "partial",
  "missing_points": ["Authentication details", "Error handling specifications"],
  "evidence": ["Document states 'API endpoints are defined below'", "No mention of security protocols"],
  "confidence": 0.7
}}
"""


USER_PROMPT_TEMPLATE = """DOCUMENT TO ANALYZE:

{document_text}

---

Analyze the above document and return JSON only.
"""


def build_system_prompt(retrieved_guidelines: List[str]) -> str:
    """
    Build system prompt with retrieved guidelines injected.
    
    This is where RAG happens - we inject relevant context
    retrieved from our knowledge base into the prompt.
    
    Args:
        retrieved_guidelines: List of relevant guideline texts
        
    Returns:
        Complete system prompt with guidelines
    """
    # Format guidelines as numbered list
    guidelines_text = "\n".join([
        f"{i+1}. {guideline.strip()}"
        for i, guideline in enumerate(retrieved_guidelines)
    ])
    
    return SYSTEM_PROMPT.format(guidelines=guidelines_text)


def build_user_prompt(document_text: str) -> str:
    """
    Build user prompt with document text.
    
    Args:
        document_text: The document to analyze
        
    Returns:
        Complete user prompt
    """
    return USER_PROMPT_TEMPLATE.format(document_text=document_text)


def build_complete_prompt(document_text: str, retrieved_guidelines: List[str]) -> str:
    """
    Build complete prompt combining system and user prompts.
    
    This creates the final prompt sent to the LLM.
    
    Args:
        document_text: The document to analyze
        retrieved_guidelines: Relevant guidelines from RAG
        
    Returns:
        Complete prompt ready for LLM
    """
    system_prompt = build_system_prompt(retrieved_guidelines)
    user_prompt = build_user_prompt(document_text)
    
    # Combine system and user prompts
    # For Gemini, we concatenate them directly
    return f"{system_prompt}\n\n{user_prompt}"
