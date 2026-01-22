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
    DocumentUploadResponse, DocumentListResponse, DocumentDeleteResponse,
    QuestionRequest, QuestionResponse
)
from app.agent.agent import get_document_analysis_agent
from app.agent.qa_agent import get_qa_agent
from app.services.vector_db import get_vector_db_service
from app.utils.file_parser import FileParser

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
    request_id = str(uuid.uuid4())[:8]
    try:
        print(f"\n{'='*70}")
        print(f"[ANALYZE REQUEST {request_id}] NEW DOCUMENT ANALYSIS")
        print(f"{'='*70}")
        print(f"[{request_id}] Document length: {len(request.document_text)} characters")
        print(f"[{request_id}] Document preview: {request.document_text[:100]}...")
        
        # Get agent instance
        print(f"[{request_id}] Step 1/5: Initializing AI Agent...")
        agent = get_document_analysis_agent()
        print(f"[{request_id}] ✓ Agent initialized")
        
        # Perform analysis
        # This may raise ValidationError if LLM output is invalid
        print(f"[{request_id}] Step 2/5: Starting document analysis pipeline...")
        result = agent.analyze_document(request.document_text, request_id)
        print(f"[{request_id}] ✓ Analysis complete")
        
        # Return success response
        print(f"[{request_id}] Step 5/5: Preparing response...")
        print(f"[{request_id}] Results: {result.completeness_status.upper()} | Confidence: {result.confidence:.2f}")
        print(f"[{request_id}] REQUEST COMPLETED SUCCESSFULLY")
        print(f"{'='*70}\n")
        return AnalyzeResponse(
            success=True,
            result=result,
            error=None
        )
    
    except ValidationError as e:
        # LLM output didn't match schema
        # This shouldn't happen often if prompts are well-designed
        print(f"[{request_id}] VALIDATION ERROR: LLM output doesn't match schema")
        print(f"[{request_id}] Error details: {str(e)}")
        print(f"{'='*70}\n")
        error_message = f"AI output validation failed: {str(e)}"
        return AnalyzeResponse(
            success=False,
            result=None,
            error=error_message
        )
    
    except ValueError as e:
        # JSON parsing error from LLM response
        print(f"[{request_id}] JSON PARSING ERROR")
        print(f"[{request_id}] Error details: {str(e)}")
        print(f"{'='*70}\n")
        error_message = f"Failed to parse AI response: {str(e)}"
        return AnalyzeResponse(
            success=False,
            result=None,
            error=error_message
        )
    
    except Exception as e:
        # Catch-all for other errors (LLM API, etc.)
        print(f"[{request_id}] UNEXPECTED ERROR: {type(e).__name__}")
        print(f"[{request_id}] Error details: {str(e)}")
        print(f"{'='*70}\n")
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
    
    Supports: .txt, .md, .pdf
    """
    upload_id = str(uuid.uuid4())[:8]
    try:
        print(f"\n{'='*70}")
        print(f"📤 [UPLOAD {upload_id}] NEW DOCUMENT UPLOAD")
        print(f"{'='*70}")
        print(f"[{upload_id}] Filename: {file.filename}")
        
        # Check if file format is supported
        if not FileParser.is_supported(file.filename):
            file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else 'unknown'
            print(f"[{upload_id}] ❌ Unsupported format: .{file_ext}")
            print(f"{'='*70}\n")
            return DocumentUploadResponse(
                success=False,
                message=f"Unsupported file format: .{file_ext}",
                error=f"Supported formats: {', '.join('.' + ext for ext in FileParser.get_supported_extensions())}"
            )
        
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        print(f"[{upload_id}] Assigned document ID: {document_id[:12]}...")
        
        # Read file content
        print(f"[{upload_id}] Step 1/4: Reading file content...")
        content = await file.read()
        file_ext = file.filename.lower().split('.')[-1]
        print(f"[{upload_id}]   • File type: .{file_ext}")
        print(f"[{upload_id}]   • File size: {len(content):,} bytes")
        
        # Parse file based on format (DO NOT decode as UTF-8 first!)
        print(f"[{upload_id}] Step 2/4: Extracting text from {file_ext.upper()}...")
        try:
            text = FileParser.parse_text(content, file.filename)
            print(f"[{upload_id}]   ✓ Text extracted - {len(text):,} characters")
        except ValueError as e:
            print(f"[{upload_id}]   ❌ Parsing failed: {str(e)}")
            print(f"{'='*70}\n")
            return DocumentUploadResponse(
                success=False,
                message="Failed to parse file",
                error=str(e)
            )
        
        if len(text) < 50:
            print(f"[{upload_id}] ❌ Document too short: {len(text)} < 50 characters")
            print(f"{'='*70}\n")
            return DocumentUploadResponse(
                success=False,
                message="Document too short (minimum 50 characters)",
                error="Document must contain at least 50 characters"
            )
        
        # Get vector DB service
        print(f"[{upload_id}] Step 3/4: Initializing Vector DB service...")
        vector_db = get_vector_db_service()
        print(f"[{upload_id}]   ✓ Vector DB ready")
        
        # Add document with metadata
        print(f"[{upload_id}] Step 4/4: Generating embeddings and storing in Vector DB...")
        metadata = {
            "filename": file.filename,
            "upload_date": datetime.now().isoformat(),
            "file_size": len(text),
            "file_type": file_ext
        }
        
        vector_db.add_document(document_id, text, metadata)
        print(f"[{upload_id}]   ✓ Document stored in vector database")
        
        print(f"[{upload_id}] ✅ DOCUMENT UPLOADED SUCCESSFULLY")
        print(f"{'='*70}\n")
        
        return DocumentUploadResponse(
            success=True,
            document_id=document_id,
            filename=file.filename,
            message=f"Document '{file.filename}' uploaded successfully"
        )
    
    except UnicodeDecodeError as e:
        print(f"[{upload_id}] ❌ ENCODING ERROR: File not in UTF-8 format")
        print(f"[{upload_id}] Error details: {str(e)}")
        print(f"{'='*70}\n")
        return DocumentUploadResponse(
            success=False,
            message="Failed to read file",
            error="Text file must be in UTF-8 format"
        )
    except Exception as e:
        print(f"[{upload_id}] ❌ UPLOAD FAILED: {type(e).__name__}")
        print(f"[{upload_id}] Error details: {str(e)}")
        print(f"{'='*70}\n")
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


@router.delete("/documents/{document_id}", response_model=DocumentDeleteResponse)
async def delete_document(document_id: str):
    """Delete a document from the vector database."""
    try:
        vector_db = get_vector_db_service()
        deleted = vector_db.delete_document(document_id)
        
        if deleted:
            return DocumentDeleteResponse(
                success=True,
                message="Document deleted successfully"
            )
        else:
            return DocumentDeleteResponse(
                success=False,
                message="Document not found",
                error="The specified document ID does not exist"
            )
    except Exception as e:
        return DocumentDeleteResponse(
            success=False,
            message="Failed to delete document",
            error=str(e)
        )


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about uploaded documents.
    
    Uses RAG to retrieve relevant context and generate answer.
    """
    question_id = str(uuid.uuid4())[:8]
    try:
        print(f"\n{'='*70}")
        print(f"❓ [Q&A {question_id}] NEW QUESTION")
        print(f"{'='*70}")
        print(f"[{question_id}] Question: {request.question}")
        if request.document_id:
            print(f"[{question_id}] Target document: {request.document_id[:12]}...")
        else:
            print(f"[{question_id}] Searching all documents")
        
        # Get Q&A agent
        print(f"[{question_id}] Step 1/3: Initializing Q&A Agent...")
        qa_agent = get_qa_agent()
        print(f"[{question_id}] ✓ Agent ready")
        
        # Get answer
        print(f"[{question_id}] Step 2/3: Processing question with RAG pipeline...")
        result = qa_agent.answer_question(
            question=request.question,
            document_id=request.document_id
        )
        print(f"[{question_id}] ✓ Answer generated")
        
        print(f"[{question_id}] Step 3/3: Preparing response...")
        print(f"[{question_id}] Sources: {len(result['sources'])} document chunks")
        print(f"[{question_id}] QUESTION ANSWERED SUCCESSFULLY")
        print(f"{'='*70}\n")
        
        return QuestionResponse(
            success=True,
            answer=result["answer"],
            sources=result["sources"]
        )
    
    except ValueError as e:
        print(f"[{question_id}] VALIDATION ERROR: {str(e)}")
        print(f"{'='*70}\n")
        return QuestionResponse(
            success=False,
            error=str(e)
        )
    except Exception as e:
        print(f"[{question_id}] ERROR: {type(e).__name__}")
        print(f"[{question_id}] Error details: {str(e)}")
        print(f"{'='*70}\n")
        return QuestionResponse(
            success=False,
            error=f"Failed to answer question: {str(e)}"
        )
