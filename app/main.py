"""
FastAPI application entry point.

This is the main file that:
- Creates the FastAPI app
- Registers routes
- Configures middleware
- Starts the server
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api import router

# Create FastAPI application
app = FastAPI(
    title="AI Agent Document Analysis Demo",
    description="Educational demo showing AI Agent principles with Gemini, LangChain, and RAG",
    version="1.0.0",
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


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    
    This is where we can:
    - Initialize database connections (not needed for demo)
    - Load ML models (handled lazily in singletons)
    - Set up logging
    """
    print("AI Agent Demo Application Starting...")
    print("Initializing services...")
    
    # Services are initialized lazily on first use
    # This keeps startup fast
    
    print("Application ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown.
    
    Clean up resources if needed.
    """
    print("Shutting down AI Agent Demo Application...")


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # For development: auto-reload on code changes
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload for development
        log_level="info"
    )
