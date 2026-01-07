"""
API routes for the document analysis application.

Exposes:
- GET / : Serve HTML frontend
- POST /analyze : Analyze document endpoint
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.models.schemas import AnalyzeRequest, AnalyzeResponse, AnalysisResult
from app.agent import get_document_analysis_agent

# Initialize router
router = APIRouter()

# Initialize templates
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Serve the main HTML page with document analysis form.
    
    This is a simple HTML frontend - no JavaScript frameworks needed.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(request: AnalyzeRequest):
    """
    Analyze a document for completeness and clarity.
    
    This endpoint:
    1. Validates the request (Pydantic does this automatically)
    2. Calls the AI agent
    3. Validates the AI output
    4. Returns structured response
    
    Args:
        request: AnalyzeRequest with document_text
        
    Returns:
        AnalyzeResponse with result or error
        
    Error handling:
    - 400: Invalid request (e.g., text too short)
    - 422: Validation error from Pydantic
    - 500: LLM API error or other internal error
    """
    try:
        # Get agent instance
        agent = get_document_analysis_agent()
        
        # Perform analysis
        # This may raise ValidationError if LLM output is invalid
        result = agent.analyze_document(request.document_text)
        
        # Return success response
        return AnalyzeResponse(
            success=True,
            result=result,
            error=None
        )
    
    except ValidationError as e:
        # LLM output didn't match schema
        # This shouldn't happen often if prompts are well-designed
        error_message = f"AI output validation failed: {str(e)}"
        return AnalyzeResponse(
            success=False,
            result=None,
            error=error_message
        )
    
    except ValueError as e:
        # JSON parsing error from LLM response
        error_message = f"Failed to parse AI response: {str(e)}"
        return AnalyzeResponse(
            success=False,
            result=None,
            error=error_message
        )
    
    except Exception as e:
        # Catch-all for other errors (LLM API, etc.)
        error_message = f"Analysis failed: {str(e)}"
        return AnalyzeResponse(
            success=False,
            result=None,
            error=error_message
        )


@router.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    
    Useful for:
    - Deployment readiness checks
    - Monitoring
    - Testing
    """
    return {"status": "healthy"}
