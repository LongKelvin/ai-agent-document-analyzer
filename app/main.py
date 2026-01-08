"""
FastAPI application entry point.

This is the main file that:
- Creates the FastAPI app
- Registers routes
- Configures middleware
- Starts the server
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.
    
    Replaces deprecated @app.on_event decorators.
    """
    # Startup
    print("AI Agent Demo Application Starting...")
    print("Initializing services...")
    print("Application ready!")
    
    yield
    
    # Shutdown
    print("Shutting down AI Agent Demo Application...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.
    
    Replaces deprecated @app.on_event decorators.
    """
    # Startup
    print("AI Agent Demo Application Starting...")
    print("Initializing services...")
    print("Application ready!")
    
    yield
    
    # Shutdown
    print("Shutting down AI Agent Demo Application...")


# Create FastAPI application
app = FastAPI(
    title="AI Agent Document Analysis Demo",
    description="Educational demo showing AI Agent principles with Gemini, LangChain, and RAG",
    version="1.0.0",
    lifespan=lifespan
)

# Add exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log and return detailed validation errors."""
    print(f"[ERROR] Validation failed for {request.url}")
    print(f"[ERROR] Details: {exc.errors()}")
    print(f"[ERROR] Body: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "result": None,
            "error": f"Validation error: {exc.errors()}"
        }
    )

# Configure CORS (for development)
# In production, specify allowed origins explicitly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # Note: reload=False to avoid Windows multiprocessing issues with torch/sentence-transformers
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disabled for Windows compatibility
        log_level="info"
    )
