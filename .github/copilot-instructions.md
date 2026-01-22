# AI Agent Document Analyzer - Copilot Instructions

## Architecture Overview

This is an **educational AI Agent demo** showcasing clean architecture patterns with FastAPI, Google Gemini, LangChain-style orchestration, and RAG (Retrieval-Augmented Generation).

The project now consists of **two main parts**:
1. **Backend AI Agent API** (FastAPI)
2. **Frontend Angular UI** (separate project, consuming the API)

**Core Philosophy**: Treat LLM outputs as untrusted. All responses must be validated with Pydantic schemas before being used or returned to clients.

---

## High-Level Architecture

```
root/
├── backend/                    # FastAPI AI Agent service
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── api/
│       ├── agent/
│       ├── services/
│       ├── models/
│       └── templates/
│
└── frontend/
    └── angular-ui/              # Angular UI project
        ├── src/
        │   ├── app/
        │   │   ├── core/        # API clients, interceptors, config
        │   │   ├── features/    # Feature modules (analyze, history, health)
        │   │   ├── shared/      # Reusable UI components
        │   │   └── app.config.ts
        │   └── environments/
        └── angular.json
```

The backend remains **API-first**. The Angular UI is a consumer, not part of core agent logic.

---

## Backend Component Structure

```
app/
├── main.py              # FastAPI entry point with startup/shutdown hooks
├── config.py            # Pydantic Settings (singleton pattern)
├── api/routes.py        # REST endpoints: GET /, POST /analyze, GET /health
├── agent/
│   ├── agent.py         # DocumentAnalysisAgent orchestrates the full pipeline
│   └── prompts.py       # Prompt templates (system + user prompts)
├── services/
│   ├── llm.py           # GeminiService singleton wraps google-generativeai
│   └── embeddings.py    # EmbeddingService with in-memory RAG (no vector DB)
├── models/schemas.py    # Pydantic models for validation
└── templates/index.html # Legacy minimal HTML UI (optional / demo only)
```

---

## Angular UI Architecture

The Angular UI is responsible only for **presentation and interaction**.

**Key responsibilities**:
- Upload or paste documents
- Call backend `/analyze` API
- Render structured analysis results
- Display validation or API errors
- Show backend health status

**Explicit non-responsibilities**:
- No prompt logic
- No schema validation
- No LLM interaction
- No business rules

All intelligence lives in the backend.

### Angular Core Patterns

```
app/
├── core/
│   ├── api/
│   │   └── document-analyzer.api.ts   # Typed HTTP client
│   ├── models/                        # TypeScript mirrors of Pydantic schemas
│   ├── interceptors/                  # Error handling, logging
│   └── config/                        # Environment-based API URLs
│
├── features/
│   ├── analyze/                       # Analyze document flow
│   ├── health/                        # Health check UI
│   └── home/
│
└── shared/
    ├── components/
    └── ui/
```

Angular should use **typed interfaces** that mirror backend Pydantic models exactly.

---

## Critical Backend Patterns

### 1. Singleton Services
All backend services use a singleton pattern via module-level functions:

```python
# services/llm.py
_gemini_service = None

def get_gemini_service() -> GeminiService:
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
```

Never instantiate services directly. Always use `get_*_service()`.

---

### 2. RAG with In-Memory Vectors

`app/services/embeddings.py` contains a hardcoded `ANALYSIS_GUIDELINES` list embedded at startup using `sentence-transformers`.

- Semantic search via cosine similarity
- No external vector database
- Entirely in-memory

---

### 3. Structured LLM Outputs

Agent workflow (`app/agent/agent.py`):
1. Retrieve guidelines via `embedding_service.retrieve_relevant_guidelines()`
2. Build prompt using `build_complete_prompt()`
3. Call `llm_service.generate_structured_response()`
4. Validate response with `AnalysisResult` (Pydantic)
5. Return validated JSON or raise an error

Raw LLM output must never be returned directly.

---

### 4. Environment Configuration

All backend configuration is loaded from `.env` via `app/config.py`.

Key variables:
- `GEMINI_API_KEY` (required)
- `GEMINI_MODEL_NAME` (default: gemini-pro)
- `TEMPERATURE` (default: 0.1)
- `EMBEDDING_MODEL_NAME` (default: all-MiniLM-L6-v2)

Access via:
```python
from app.config import settings
```

Angular configuration uses `environment.ts` files only and must not duplicate backend secrets.

---

## Developer Workflows

### Backend: Running the Application

```powershell
.\venv\Scripts\Activate.ps1
python -m app.main
```

Do not use `--reload` on Windows.

---

### Frontend: Running Angular UI

```powershell
cd frontend/angular-ui
npm install
npm start
```

The Angular app should proxy API calls to the FastAPI backend during development.

---

## API Contract Rules (Backend to Frontend)

- API responses are always validated JSON
- Schema changes require:
  1. Updating Pydantic models
  2. Updating system prompt JSON examples
  3. Updating Angular TypeScript interfaces

Backend schema is the single source of truth.

---

## Project-Specific Conventions

### 1. Low Temperature (0.1)

Required for deterministic JSON output. Do not increase unless schema validation is removed.

---

### 2. Evidence-Based Analysis

The agent must:
- Cite only text from the input document
- Provide direct quotes
- Use confidence scores
- Never hallucinate

---

### 3. Prompt Engineering Contract

The system prompt defines the JSON contract.

Any schema change must be reflected in:
- `app/models/schemas.py`
- `app/agent/prompts.py`
- Angular TypeScript models

---

### 4. No Business Logic in Angular

Angular is strictly a UI layer:
- No AI logic
- No validation rules beyond UX
- No prompt awareness

This keeps the demo clean, testable, and educational.

---

## Integration Points

### FastAPI
- CORS enabled for development
- REST-only communication
- No authentication

### Google Gemini
- Wrapped by `GeminiService`
- No retries
- Strict JSON extraction

### Sentence Transformers
- Local inference only
- In-memory embeddings

---

## Common Pitfalls

1. Using `--reload` on Windows
2. Changing schema without updating Angular models
3. Letting frontend interpret LLM output
4. Increasing temperature and breaking validation
5. Forgetting first-run embedding model download delay

---

## Extension Patterns

To extend analysis capabilities:
1. Update `ANALYSIS_GUIDELINES`
2. Modify `AnalysisResult` schema
3. Update system prompt JSON example
4. Update Angular models and UI rendering

The agent orchestration usually does not need changes.

