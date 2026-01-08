"""
API routes for the document analysis application.

Exposes:
- GET / : Serve HTML frontend
- POST /analyze : Analyze document endpoint
- POST /upload : Upload document to vector DB
- GET /documents : List uploaded documents
- DELETE /documents/{document_id} : Delete document
- POST /ask : Ask question about documents
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.models.schemas import (
    AnalyzeRequest, AnalyzeResponse, AnalysisResult,
    DocumentUploadResponse, DocumentListResponse, 
    QuestionRequest, QuestionResponse
)
from app.agent import get_document_analysis_agent
from app.agent.qa_agent import get_qa_agent
from app.services.vector_db import get_vector_db_service

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


@router.get("/advanced", response_class=HTMLResponse)
async def advanced_ui(request: Request):
    """
    Serve the advanced UI with document upload and Q&A.
    """
    return templates.TemplateResponse("advanced.html", {"request": request})


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
        # Log incoming request for debugging
        print(f"[DEBUG] Received request with document length: {len(request.document_text)}")
        
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
    return {"status": "healthy", "service": "AI Agent Document Analyzer"}


# New endpoints for document upload and Q&A

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to the vector database.
    
    Supports: .txt, .md, .pdf (text-based)
    """
    try:
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        if len(text) < 50:
            return DocumentUploadResponse(
                success=False,
                message="Document too short (minimum 50 characters)",
                error="Document must contain at least 50 characters"
            )
        
        # Get vector DB service
        vector_db = get_vector_db_service()
        
        # Add document with metadata
        metadata = {
            "filename": file.filename,
            "upload_date": datetime.now().isoformat(),
            "file_size": len(text)
        }
        
        vector_db.add_document(document_id, text, metadata)
        
        return DocumentUploadResponse(
            success=True,
            document_id=document_id,
            filename=file.filename,
            message=f"Document '{file.filename}' uploaded successfully"
        )
    
    except UnicodeDecodeError:
        return DocumentUploadResponse(
            success=False,
            message="Failed to read file",
            error="File must be in UTF-8 text format"
        )
    except Exception as e:
        return DocumentUploadResponse(
            success=False,
            message="Upload failed",
            error=str(e)
        )


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """List all uploaded documents."""
    try:
        vector_db = get_vector_db_service()
        documents = vector_db.list_documents()
        
        return DocumentListResponse(
            success=True,
            documents=documents,
            total_count=len(documents)
        )
    except Exception as e:
        return DocumentListResponse(
            success=False,
            error=str(e)
        )


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document from the vector database."""
    try:
        vector_db = get_vector_db_service()
        deleted = vector_db.delete_document(document_id)
        
        if deleted:
            return {"success": True, "message": "Document deleted"}
        else:
            return {"success": False, "message": "Document not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about uploaded documents.
    
    Uses RAG to retrieve relevant context and generate answer.
    """
    try:
        # Get Q&A agent
        qa_agent = get_qa_agent()
        
        # Get answer
        result = qa_agent.answer_question(
            question=request.question,
            document_id=request.document_id
        )
        
        return QuestionResponse(
            success=True,
            answer=result["answer"],
            sources=result["sources"]
        )
    
    except ValueError as e:
        return QuestionResponse(
            success=False,
            error=str(e)
        )
    except Exception as e:
        return QuestionResponse(
            success=False,
            error=f"Failed to answer question: {str(e)}"
        )
