# AI Agent Document Analysis Demo

An educational demonstration of building an AI Agent using Python, FastAPI, LangChain, Google Gemini AI, and RAG (Retrieval-Augmented Generation).

## Learning Objectives

This project demonstrates:
- **AI Agent Architecture**: Building agents that treat LLMs as untrusted components
- **Prompt Engineering**: Using prompts as contracts with strict output requirements
- **RAG (Retrieval-Augmented Generation)**: Semantic search with embeddings
- **Structured Output**: Pydantic validation for LLM responses
- **Evidence-Based AI**: No hallucination, only facts from source documents
- **Clean Architecture**: Separation of concerns with clear module boundaries

## Project Structure

```
app/
├── main.py                # FastAPI entry point
├── config.py              # Configuration management
├── api/
│   ├── __init__.py
│   └── routes.py          # API endpoints
├── agent/
│   ├── __init__.py
│   ├── agent.py           # Agent orchestration logic
│   └── prompts.py         # System & user prompts
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models
├── services/
│   ├── __init__.py
│   ├── llm.py             # Gemini LLM wrapper
│   └── embeddings.py      # Embedding + retrieval logic
└── templates/
    └── index.html         # Simple UI
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### 2. Clone and Navigate

```powershell
cd c:\QBrainAI\demo-workspace\ai-agent-demo
```

### 3. Create Virtual Environment

```powershell
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL_NAME=gemini-pro
TEMPERATURE=0.1
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
```

### 7. Run the Application

```powershell
python -m app.main
```

Or using uvicorn directly:
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Open in Browser

Navigate to: [http://localhost:8000](http://localhost:8000)

## How It Works

### 1. User Submits Document
User pastes text into the web interface and clicks "Analyze"

### 2. RAG Retrieval
- Document is embedded using sentence-transformers
- Semantic search finds relevant analysis guidelines
- Top-k guidelines are retrieved from in-memory vector store

### 3. Prompt Construction
- System prompt defines agent behavior and constraints
- Retrieved guidelines are injected into prompt
- User document is added as context
- Complete prompt is built

### 4. LLM Invocation
- Prompt sent to Google Gemini API
- Temperature set to 0.1 for deterministic output
- LLM generates JSON response

### 5. Output Validation
- JSON extracted from LLM response
- Pydantic validates against `AnalysisResult` schema
- If validation fails, error is returned
- If successful, structured result is returned

### 6. Display Results
- Analysis summary
- Completeness status (complete/partial/unknown)
- Missing points (if any)
- Evidence quotes from document
- Confidence score

## Key Concepts Demonstrated

### 1. Treating LLM as Untrusted

```python
# Output must match strict schema
class AnalysisResult(BaseModel):
    summary: str
    completeness_status: Literal["complete", "partial", "unknown"]
    missing_points: List[str]
    evidence: List[str]
    confidence: float
```

### 2. Prompt as Contract

The system prompt explicitly defines:
- What the agent can and cannot do
- Required output format
- Constraints (no hallucination)
- Evidence requirements

### 3. RAG Implementation

```python
# Retrieve relevant context
guidelines = embedding_service.retrieve_relevant_guidelines(
    query=document_text,
    top_k=2
)

# Inject into prompt
prompt = build_complete_prompt(document_text, guidelines)
```

### 4. Evidence-Based Analysis

The agent is instructed to:
- Only cite information present in the document
- Provide direct quotes as evidence
- Say "unknown" when uncertain
- Use confidence scores to reflect certainty

## API Endpoints

### `GET /`
Serves the HTML frontend

### `POST /analyze`
Analyzes a document

**Request:**
```json
{
  "document_text": "Your document text here..."
}
```

**Response (Success):**
```json
{
  "success": true,
  "result": {
    "summary": "Brief summary of the document",
    "completeness_status": "partial",
    "missing_points": ["List", "of", "missing", "sections"],
    "evidence": ["Direct quotes from document"],
    "confidence": 0.85
  },
  "error": null
}
```

**Response (Error):**
```json
{
  "success": false,
  "result": null,
  "error": "Error message here"
}
```

### `GET /health`
Health check endpoint

## Configuration

All configuration is managed through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `GEMINI_MODEL_NAME` | Gemini model to use | `gemini-pro` |
| `TEMPERATURE` | LLM temperature (0.0-2.0) | `0.1` |
| `EMBEDDING_MODEL_NAME` | Sentence transformer model | `all-MiniLM-L6-v2` |

## Testing the Application

Try these sample documents:

### Example 1: Incomplete Document
```
Project Proposal: AI Task Manager

We want to build an AI-powered task manager.

Features:
- Task creation
- Priority suggestions
```

**Expected:** Status = "partial", Missing points identified

### Example 2: Complete Document
```
Project Proposal: AI Task Manager

Introduction:
This document outlines our plan to build a task management application 
with AI-powered priority suggestions.

Background:
Current task managers lack intelligent prioritization.

Proposed Solution:
- Task creation and editing
- AI-powered priority suggestions using machine learning
- Calendar integration for scheduling

Technical Stack:
- Frontend: React
- Backend: Python/FastAPI
- AI: LangChain + OpenAI

Conclusion:
This solution will improve productivity by 30%.

References:
- Industry benchmark study (2024)
```

**Expected:** Status = "complete", High confidence

## Educational Notes

### Why Low Temperature (0.1)?
- More deterministic output
- Better JSON compliance
- Less creativity (which we don't want for structured analysis)

### Why Validate with Pydantic?
- LLMs can make mistakes
- Ensures type safety
- Provides clear error messages
- Acts as a contract enforcement layer

### Why In-Memory Vector Store?
- Sufficient for educational demo
- No external dependencies
- Easy to understand
- Fast for small datasets

### Production Considerations (Not Implemented Here)
- Use proper vector database (Pinecone, Weaviate, etc.)
- Add caching layer
- Implement rate limiting
- Add authentication
- Use async database connections
- Add comprehensive error logging
- Implement retry logic for API calls

## Troubleshooting

### Import Errors
If you see import errors like "Import 'fastapi' could not be resolved":
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt` again
3. Restart your IDE

### API Key Errors
If you see "Gemini API error":
1. Check `.env` file exists and has correct API key
2. Verify API key is valid at [Google AI Studio](https://makersuite.google.com/)
3. Ensure no extra spaces in API key

### Model Download Issues
First run may take time to download sentence-transformer model (~80MB).
Wait for download to complete.

## License

This is educational code. Use freely for learning purposes.

## Contributing

This is a demo project for learning. Feel free to fork and experiment!

## Questions?

This project demonstrates AI Agent principles for educational purposes.
Explore the code, modify it, and learn by doing!

---

**Happy Learning!**
