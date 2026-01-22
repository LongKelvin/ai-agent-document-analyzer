# AI Agent Document Analyzer

[![Powered by Claude Sonnet 4.5](https://img.shields.io/badge/AI-Claude%20Sonnet%204.5-blue)](https://www.anthropic.com/claude)
[![Built with Gemini 2.0](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-orange)](https://deepmind.google/technologies/gemini/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Angular 18](https://img.shields.io/badge/Angular-18-red.svg)](https://angular.io/)
[![License: MIT](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

> **Educational AI Agent Demo** - Learn to build production-grade AI agents with RAG, prompt engineering, structured validation, and modern web interfaces.

---

## Built With AI

**This entire project was architected and developed by Claude Sonnet 4.5** (Anthropic), demonstrating AI-assisted software engineering at its finest. Every line of code, documentation, and architectural decision showcases what's possible when human vision meets AI capability.

**Runtime powered by Google Gemini 2.0 Flash** - The latest and fastest Gemini model for production AI applications.

---

## What You'll Learn

This project demonstrates professional AI Agent development:
- **AI Agent Architecture** - Treating LLMs as untrusted components
- **RAG (Retrieval-Augmented Generation)** - Semantic search with ChromaDB vector store
- **Prompt Engineering** - Prompts as strict contracts
- **Structured Output** - Pydantic validation for LLM responses
- **Evidence-Based AI** - No hallucination, only facts with citations
- **Clean Architecture** - Separation of concerns (Backend API + Frontend UI)
- **Modern Web Stack** - FastAPI + Angular 18 with TypeScript
- **Document Q&A** - Interactive question answering over uploaded documents

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Google Gemini API key ([Get free key](https://makersuite.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/LongKelvin/ai-agent-document-analyzer.git
cd ai-agent-document-analyzer

# Backend Setup (Windows PowerShell)
cd backend
.\setup.ps1  # Automated: creates venv, installs deps, configures .env

# Or manual backend setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Frontend Setup
cd ../frontend/angular-ui
npm install
```

### Run Application

**Terminal 1 - Backend:**
```bash
cd backend
.\run.ps1  # Or: python -m app.main
```
Backend runs on http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend/angular-ui
npm start
```
Frontend runs on http://localhost:4200

Open http://localhost:4200 in your browser

---

## Project Structure

```
ai-agent-document-analyzer/
├── backend/                      # FastAPI AI Agent Service
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration management
│   │   ├── api/
│   │   │   └── routes.py        # REST endpoints
│   │   ├── agent/
│   │   │   ├── agent.py         # Document analysis orchestration
│   │   │   ├── qa_agent.py      # Q&A agent with RAG
│   │   │   └── prompts.py       # Prompt engineering
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic validation schemas
│   │   ├── services/
│   │   │   ├── llm.py           # Gemini 2.0 Flash integration
│   │   │   ├── embeddings.py    # Sentence transformers
│   │   │   └── vector_db.py     # ChromaDB vector store
│   │   ├── utils/
│   │   │   └── file_parser.py   # Document parsing (PDF, TXT, MD)
│   │   └── templates/
│   │       └── index.html       # Legacy demo UI
│   ├── requirements.txt
│   ├── setup.ps1                # Automated setup script
│   └── run.ps1                  # Quick run script
│
└── frontend/
    └── angular-ui/               # Angular 18 UI
        ├── src/
        │   ├── app/
        │   │   ├── core/         # API clients, models, config
        │   │   ├── features/     # Feature modules
        │   │   │   ├── analyze/  # Document analysis
        │   │   │   ├── documents/ # Upload, Q&A, management
        │   │   │   └── health/   # Health check
        │   │   └── shared/       # Reusable UI components
        │   └── environments/
        ├── proxy.conf.json       # Dev proxy to backend
        ├── package.json
        └── angular.json
```

---

## Architecture

### Backend (FastAPI + AI)
- **REST API** with CORS enabled for development
- **AI Agent** orchestrates document analysis with RAG
- **Q&A Agent** answers questions using vector similarity search
- **Pydantic Validation** ensures LLM output integrity
- **ChromaDB** for persistent vector storage
- **Singleton Services** for efficient resource management

### Frontend (Angular 18)
- **Standalone Components** (no NgModules)
- **Typed API Client** mirrors backend Pydantic schemas
- **RxJS Observables** for async operations
- **TailwindCSS** for styling
- **Three Main Features:**
  - Document Analysis (upload & analyze)
  - Document Management (upload, Q&A, delete)
  - Health Check

### Integration
- Frontend proxies `/api/*` to `http://localhost:8000`
- TypeScript interfaces mirror Pydantic models exactly
- No business logic in frontend (presentation only)
- Backend is single source of truth

---

## Key Features

✅ **Document Analysis** - Analyzes completeness, extracts evidence, provides confidence scores  
✅ **Document Q&A** - Ask questions about uploaded documents with source citations  
✅ **Multi-Format Support** - PDF, TXT, Markdown with proper parsing  
✅ **Vector Search** - ChromaDB for semantic similarity matching  
✅ **RAG Pipeline** - Retrieval-Augmented Generation for accurate answers  
✅ **Structured Output** - Pydantic ensures type safety and validation  
✅ **Evidence-Based** - All answers include source text and document references  
✅ **Modern UI** - Clean Angular interface with real-time feedback  
✅ **API-First Design** - Backend can be consumed by any client  

---

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.10+
- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB 0.4.22
- **Validation**: Pydantic v2
- **Document Parsing**: PyPDF2, python-docx

### Frontend
- **Framework**: Angular 18
- **Language**: TypeScript 5+
- **Styling**: TailwindCSS 3
- **HTTP**: Angular HttpClient
- **Build**: Angular CLI with Vite

---

## API Endpoints

### Document Analysis
**`POST /api/analyze`**
Analyzes document completeness and quality

**Request:**
```json
{
  "document_text": "Your document content here..."
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "summary": "Brief summary",
    "completeness_status": "complete|partial|insufficient",
    "missing_points": ["Section A", "Section B"],
    "evidence": ["Quote 1", "Quote 2"],
    "confidence": 0.85
  }
}
```

### Document Upload & Management
**`POST /api/upload`** - Upload document to vector store  
**`GET /api/documents`** - List all uploaded documents  
**`DELETE /api/documents/{id}`** - Delete document  

### Question & Answer
**`POST /api/ask`** - Ask questions about uploaded documents

**Request:**
```json
{
  "question": "What is the main purpose of this document?"
}
```

**Response:**
```json
{
  "success": true,
  "answer": "The document describes...",
  "sources": [
    {
      "source_number": 1,
      "text": "Relevant excerpt from document",
      "document": "filename.pdf",
      "document_id": "abc-123"
    }
  ]
}
```

### Health Check
**`GET /api/health`** - Service status and configuration

---

## How It Works

### Document Analysis Flow
1. User submits document via Angular UI
2. Frontend sends POST to `/api/analyze`
3. Backend RAG retrieves relevant guidelines using embeddings
4. Prompt construction injects guidelines + document
5. Gemini 2.0 Flash generates structured JSON analysis
6. Pydantic validates output matches `AnalysisResult` schema
7. Frontend displays results with evidence and confidence

### Q&A Flow
1. User uploads documents to vector store
2. Documents are chunked and embedded using sentence-transformers
3. Embeddings stored in ChromaDB with metadata
4. User asks question via Angular UI
5. Question is embedded and ChromaDB finds similar chunks
6. Retrieved context + question sent to Gemini
7. LLM generates answer with source citations
8. Pydantic validates `QuestionResponse` schema
9. Frontend displays answer with clickable source references

---

## Documentation

### Backend Docs (in `backend/`)
- **[START_HERE.md](backend/START_HERE.md)** - Documentation master index
- **[GETTING_STARTED.md](backend/GETTING_STARTED.md)** - Quick visual guide
- **[QUICKSTART.md](backend/QUICKSTART.md)** - 5-minute setup
- **[PROJECT_SUMMARY.md](backend/PROJECT_SUMMARY.md)** - Deep educational dive
- **[FILE_INDEX.md](backend/FILE_INDEX.md)** - Complete file reference
- **[PDF_SUPPORT_GUIDE.md](backend/PDF_SUPPORT_GUIDE.md)** - PDF parsing guide

### Frontend Docs (in `frontend/angular-ui/`)
- **[README.md](frontend/angular-ui/README.md)** - Angular CLI reference
- **[README_UI.md](frontend/angular-ui/README_UI.md)** - UI architecture guide

### Integration Docs (in root)
- **[INTEGRATION_VERIFICATION.md](INTEGRATION_VERIFICATION.md)** - Backend-frontend integration details
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - AI agent development guidelines

---

## Learning Path

### Beginner (1 hour)
1. Run backend and frontend
2. Upload a document and analyze it
3. Try the Q&A feature
4. Read QUICKSTART.md

### Intermediate (3 hours)
4. Study backend/app/agent/prompts.py
5. Explore RAG in backend/app/services/vector_db.py
6. Review Angular API client structure
7. Modify prompts and test changes

### Advanced (Full day)
8. Add new analysis types to backend
9. Create new Angular components
10. Implement conversation history
11. Add authentication
12. Deploy to production (Docker + cloud)

---

## Customization

### Easy Modifications
- **Prompts**: Edit `backend/app/agent/prompts.py`
- **UI Styling**: Modify `frontend/angular-ui/src/app/**/*.css`
- **Output Schema**: Update `backend/app/models/schemas.py` + TypeScript models
- **LLM Settings**: Change temperature/model in `backend/app/config.py`

### Extension Ideas
- Add sentiment analysis
- Implement conversation memory
- Try different LLM models (Claude, GPT-4)
- Add real-time collaboration
- Implement user authentication
- Deploy with Docker Compose
- Add more document formats (DOCX, XLSX)
- Implement document comparison

---

## Development Tips

### Backend Development
```bash
# Check dependencies
python check_setup.py

# Test PDF support
python test_pdf_support.py

# Reindex all documents
python reindex_documents.py --clear
```

### Frontend Development
```bash
# Run dev server with proxy
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Common Issues
- **CORS errors**: Ensure backend CORS allows `http://localhost:4200`
- **Observable not completing**: Removed `withFetch()` from HttpClient config
- **UI not updating**: Added `ChangeDetectorRef.detectChanges()` after async ops
- **Schema validation errors**: Ensure TypeScript models match Pydantic exactly

---

## Testing

### Backend Testing
```bash
# Test API connection
cd backend
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

### Frontend Testing
```bash
# Test with PowerShell scripts
.\test-api-connection.ps1
.\test-integration.ps1
.\test-upload-response.ps1
```

---

## Contributing

This is an educational project. Feel free to:
- Fork and experiment
- Suggest improvements via issues
- Share your learnings
- Build upon it for your own projects

---

## License

Educational use - Free to learn, modify, and extend.

---

## Acknowledgments

- **Claude Sonnet 4.5** (Anthropic) - Project architecture and development
- **Google Gemini 2.0 Flash** - Runtime AI model
- **FastAPI** - Backend web framework
- **Angular Team** - Frontend framework
- **ChromaDB** - Vector database
- **Pydantic** - Data validation
- **sentence-transformers** - Embedding models

---

## Support

- **Documentation**: See backend/START_HERE.md and frontend README files
- **Issues**: Use GitHub issues for bug reports
- **Learning**: Read backend/PROJECT_SUMMARY.md for deep dive

---

## Star History

If this project helped you learn AI Agent development, consider giving it a star! ⭐

---

**Built with AI by Claude Sonnet 4.5**

*Demonstrating the future of AI-assisted software development*
