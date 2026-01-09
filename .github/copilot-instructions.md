# AI Agent Document Analyzer - Copilot Instructions

## Architecture Overview

This is an **educational AI Agent demo** showcasing clean architecture patterns with FastAPI, Google Gemini, LangChain, and RAG (Retrieval-Augmented Generation).

**Core Philosophy**: Treat LLM outputs as untrusted - all responses are validated with Pydantic schemas before use.

**Two Implementations Available**:
1. **Custom Implementation** (`llm.py`, `vector_db.py`, `qa_agent.py`) - Educational, shows fundamentals
2. **LangChain Implementation** (`*_langchain.py` files) - Production-ready, industry standard

See `LANGCHAIN_EXPLAINED.md` and `LANGCHAIN_COMPARISON.md` for detailed comparison.

### Component Structure
```
app/
├── main.py              # FastAPI entry point with lifespan context manager
├── config.py            # Pydantic Settings (singleton pattern)
├── api/routes.py        # REST endpoints: GET /, POST /analyze, POST /upload, POST /ask
├── agent/
│   ├── agent.py         # DocumentAnalysisAgent (custom implementation)
│   ├── qa_agent.py      # QAAgent (custom implementation)
│   ├── qa_agent_langchain.py  # QAAgent using LangChain chains (NEW)
│   └── prompts.py       # Prompt templates (system + user prompts)
├── services/
│   ├── llm.py           # GeminiService (custom implementation)
│   ├── llm_langchain.py # LangChain LLM wrapper (NEW)
│   ├── embeddings.py    # EmbeddingService with in-memory RAG
│   ├── vector_db.py     # VectorDBService with ChromaDB (custom)
│   └── vector_db_langchain.py  # LangChain Chroma wrapper (NEW)
├── models/schemas.py    # Pydantic models for validation
└── templates/           # Web UI (index.html, advanced.html)
```

## Critical Patterns

### 1. Singleton Services
All services use singleton pattern via module-level functions:
```python
# In services/llm.py
_gemini_service = None
def get_gemini_service() -> GeminiService:
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
```
Never instantiate services directly - always use `get_*_service()` functions.

### 2. RAG with In-Memory Vectors AND Persistent Vector DB
- **In-Memory**: `app/services/embeddings.py` contains hardcoded `ANALYSIS_GUIDELINES` for document analysis
- **Persistent**: `app/services/vector_db.py` or `app/services/vector_db_langchain.py` stores user-uploaded documents in ChromaDB

### 3. LangChain Integration (New)
The project now includes LangChain implementations alongside custom code:

**Custom vs LangChain:**
- `llm.py` (custom) vs `llm_langchain.py` (LangChain wrapper for Gemini)
- `vector_db.py` (custom) vs `vector_db_langchain.py` (LangChain Chroma wrapper)
- `qa_agent.py` (custom) vs `qa_agent_langchain.py` (LangChain chains with LCEL)

**Key LangChain Concepts:**
- **LCEL (LangChain Expression Language)**: Chain components with `|` operator
- **Retrievers**: Standardized interface for fetching relevant documents
- **Chains**: Pre-built (RetrievalQA) and custom (LCEL) pipelines
- **Prompt Templates**: Structured prompts (system + user messages)
- **Output Parsers**: Automatic JSON/text extraction

See `LANGCHAIN_EXPLAINED.md` for detailed guide.

### 4. Structured LLM Outputs
Agent workflow in `app/agent/agent.py`:
1. Retrieve guidelines via `embedding_service.retrieve_relevant_guidelines()`
2. Build prompt with `build_complete_prompt()` from `app/agent/prompts.py`
3. Call `llm_service.generate_structured_response()` 
4. Validate response against `AnalysisResult` Pydantic schema
5. Return validated result or raise error

**Never trust raw LLM output** - always validate with Pydantic first.

### 5. Environment Configuration
All config via `.env` file loaded by `app/config.py`. Key variables:
- `GEMINI_API_KEY` (required)
- `GEMINI_MODEL_NAME` (default: gemini-pro, supports gemini-2.0-flash, gemini-2.5-flash)
- `TEMPERATURE` (default: 0.1 for deterministic output)
- `EMBEDDING_MODEL_NAME` (default: all-MiniLM-L6-v2)

Access via `from app.config import settings`.

## Developer Workflows

### Running the Application
```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Run directly (no auto-reload to avoid Windows multiprocessing issues)
python -m app.main

# Or use wrapper script
.\run.ps1
```

**Important**: Do NOT use `--reload` flag on Windows - causes torch/multiprocessing errors with sentence-transformers.

### Setup Verification
```powershell
python check_setup.py
```
Validates: packages installed, API key configured, project structure correct.

### Testing Changes
No formal test suite. Manual testing via:
1. Run application: `python -m app.main`
2. Open browser: http://localhost:8000
3. Submit test documents via web UI
4. Check console logs for errors

### Common Commands
```powershell
# Install dependencies
pip install -r requirements.txt

# Create new .env from template
Copy-Item .env.example .env

# Automated setup
.\setup.ps1
```

## Project-Specific Conventions

### 1. Low Temperature (0.1)
LLM temperature set to 0.1 for **deterministic JSON output**. Do not increase unless you want creative responses (which breaks validation).

### 2. Evidence-Based Analysis
The agent is explicitly instructed (via system prompt) to:
- Only cite text present in the input document
- Provide direct quotes as evidence
- Use confidence scores to reflect uncertainty
- Never hallucinate missing information

### 3. Prompt Engineering
System prompt in `app/agent/prompts.py` acts as a **contract** specifying exact JSON schema. Changes to schema require updating both:
- `app/models/schemas.py` (Pydantic model)
- `app/agent/prompts.py` (system prompt JSON example)

### 4. No External Dependencies for Core Logic
- No vector database (in-memory only)
- No database for persistence
- No authentication/authorization
- Minimal frontend (vanilla HTML/CSS/JS)

This keeps the demo simple and focused on AI Agent patterns.

## Integration Points

### Google Gemini API
- Wrapped in `app/services/llm.py`
- Uses `google.generativeai` library
- Error handling: raises exceptions on API failures (no retries)
- JSON extraction via regex `json\s*(.*?)\s*` pattern

### Sentence Transformers
- Model downloaded on first run (~80MB for all-MiniLM-L6-v2)
- Runs locally (no API calls)
- Embeddings cached in memory at startup

### FastAPI
- CORS enabled for all origins (development only)
- Jinja2 templates for HTML rendering
- Async handlers not required (no DB I/O)

## Common Pitfalls

1. **Windows Reload Issue**: Never use `uvicorn --reload` on Windows - causes multiprocessing errors with torch.
2. **API Key Format**: Ensure no spaces/quotes around API key in `.env` file.
3. **Model Names**: Use exact model names from Google (e.g., `gemini-2.0-flash`, not `gemini-2-flash`).
4. **Pydantic Validation**: If LLM output doesn't match schema, validation fails silently - check logs.
5. **First Run Delay**: Sentence-transformer model downloads on first execution (~1-2 minutes).

## Extension Patterns

To add new analysis capabilities:
1. Update `ANALYSIS_GUIDELINES` in `app/services/embeddings.py`
2. Modify `AnalysisResult` schema in `app/models/schemas.py`
3. Update system prompt in `app/agent/prompts.py` to reflect new schema
4. Agent orchestration (`app/agent/agent.py`) usually needs no changes
