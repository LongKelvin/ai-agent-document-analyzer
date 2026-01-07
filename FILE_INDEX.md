# 📑 Project File Index

Complete reference of all files in the AI Agent Demo project.

---

## 📖 Documentation Files

| File | Purpose | For |
|------|---------|-----|
| **README.md** | Complete project documentation with setup, architecture, and usage | Everyone |
| **QUICKSTART.md** | 5-minute quick start guide | New users |
| **PROJECT_SUMMARY.md** | Comprehensive educational overview with concepts explained | Learners |
| **FILE_INDEX.md** | This file - index of all project files | Reference |

---

## ⚙️ Configuration Files

| File | Purpose | Edit? |
|------|---------|-------|
| **requirements.txt** | Python package dependencies | No (unless adding packages) |
| **.env.example** | Template for environment variables | No (copy to .env) |
| **.env** | Actual environment configuration (not in git) | **YES - Add your API key** |
| **.gitignore** | Files to exclude from git | Rarely |

---

## 🚀 Setup & Utility Scripts

| File | Purpose | When to Use |
|------|---------|-------------|
| **setup.ps1** | Automated setup wizard (PowerShell) | First time setup on Windows |
| **check_setup.py** | Verify installation and configuration | After setup, before running |

---

## 🏗️ Application Code

### Root Application Files

| File | Purpose | Key Concepts |
|------|---------|--------------|
| **app/__init__.py** | Makes `app` a Python package | Package initialization |
| **app/main.py** | FastAPI application entry point | Application lifecycle, CORS |
| **app/config.py** | Configuration management | Pydantic Settings, env vars |

### API Layer (`app/api/`)

| File | Purpose | Key Concepts |
|------|---------|--------------|
| **app/api/__init__.py** | Package initialization | Router export |
| **app/api/routes.py** | FastAPI endpoints and route handlers | REST API, error handling |

**Endpoints:**
- `GET /` - Serve HTML frontend
- `POST /analyze` - Document analysis endpoint
- `GET /health` - Health check

### Agent Layer (`app/agent/`)

| File | Purpose | Key Concepts |
|------|---------|--------------|
| **app/agent/__init__.py** | Package initialization | Agent exports |
| **app/agent/agent.py** | AI Agent orchestration logic | RAG workflow, validation |
| **app/agent/prompts.py** | System and user prompt templates | Prompt engineering, contracts |

**Key Functions:**
- `analyze_document()` - Main agent workflow
- `build_complete_prompt()` - Assemble final prompt
- `build_system_prompt()` - Create system instructions

### Data Models (`app/models/`)

| File | Purpose | Key Concepts |
|------|---------|--------------|
| **app/models/__init__.py** | Package initialization | Schema exports |
| **app/models/schemas.py** | Pydantic data models | Validation, type safety |

**Schemas:**
- `AnalysisResult` - LLM output structure
- `AnalyzeRequest` - API request validation
- `AnalyzeResponse` - API response structure

### Services Layer (`app/services/`)

| File | Purpose | Key Concepts |
|------|---------|--------------|
| **app/services/__init__.py** | Package initialization | Service exports |
| **app/services/llm.py** | Google Gemini API wrapper | LLM integration, JSON parsing |
| **app/services/embeddings.py** | Embeddings and vector search | RAG, semantic similarity |

**Key Classes:**
- `GeminiService` - LLM interaction
- `EmbeddingService` - Vector search and retrieval

### Frontend (`app/templates/`)

| File | Purpose | Key Concepts |
|------|---------|--------------|
| **app/templates/index.html** | Web UI for document analysis | HTML form, JavaScript fetch API |

**Features:**
- Document input textarea
- Submit button
- Results display with formatting
- Loading states
- Error handling

---

## 📊 File Statistics

```
Total Files: 24
├── Documentation: 4 files
├── Configuration: 4 files
├── Scripts: 2 files
└── Application Code: 14 files
    ├── Core: 3 files
    ├── API: 2 files
    ├── Agent: 3 files
    ├── Models: 2 files
    ├── Services: 3 files
    └── Frontend: 1 file
```

---

## 🎯 Files by Learning Priority

### 1. **Start Here** (Understanding the app)
1. `README.md` - Overview and setup
2. `QUICKSTART.md` - Get it running
3. `app/main.py` - Application entry point
4. `app/templates/index.html` - See the UI

### 2. **Core Concepts** (Key architecture)
5. `app/models/schemas.py` - Data validation
6. `app/agent/prompts.py` - Prompt engineering
7. `app/agent/agent.py` - Agent workflow
8. `app/services/llm.py` - LLM interaction

### 3. **Advanced Topics** (Deep dive)
9. `app/services/embeddings.py` - RAG implementation
10. `app/config.py` - Configuration patterns
11. `app/api/routes.py` - API design
12. `PROJECT_SUMMARY.md` - Comprehensive concepts

---

## 🔍 Find Files by Concept

### Want to understand **Pydantic Validation**?
Read: `app/models/schemas.py`

### Want to understand **Prompt Engineering**?
Read: `app/agent/prompts.py`

### Want to understand **RAG**?
Read: `app/services/embeddings.py`

### Want to understand **LLM Integration**?
Read: `app/services/llm.py`

### Want to understand **FastAPI**?
Read: `app/main.py`, `app/api/routes.py`

### Want to understand **Agent Orchestration**?
Read: `app/agent/agent.py`

### Want to understand **Configuration**?
Read: `app/config.py`, `.env.example`

---

## 📝 File Dependencies

```
app/main.py
  ├── app/config.py
  └── app/api/routes.py
      ├── app/models/schemas.py
      └── app/agent/agent.py
          ├── app/agent/prompts.py
          ├── app/services/llm.py
          │   └── app/config.py
          └── app/services/embeddings.py
              └── app/config.py
```

---

## 🛠️ Files You Should Modify

### **Definitely Edit:**
- `.env` - Add your API key
- `app/agent/prompts.py` - Experiment with prompts
- `app/services/embeddings.py` - Try different guidelines

### **Might Edit:**
- `app/models/schemas.py` - Add new fields
- `app/templates/index.html` - Customize UI
- `app/config.py` - Add new settings

### **Rarely Edit:**
- `app/main.py` - Core app setup
- `app/api/routes.py` - Endpoint logic
- `requirements.txt` - Dependencies

### **Don't Edit:**
- `.env.example` - Template for others
- `README.md` - Keep original docs
- `.gitignore` - Standard ignores

---

## 📦 File Sizes (Approximate)

```
Large Files (>5KB):
├── app/templates/index.html      ~12 KB (HTML + CSS + JS)
├── app/services/embeddings.py    ~6 KB (RAG logic)
├── PROJECT_SUMMARY.md            ~15 KB (comprehensive docs)
└── README.md                     ~12 KB (full documentation)

Medium Files (2-5KB):
├── app/models/schemas.py         ~3 KB (Pydantic models)
├── app/services/llm.py           ~4 KB (LLM wrapper)
├── app/agent/prompts.py          ~4 KB (Prompt templates)
├── app/agent/agent.py            ~3 KB (Agent logic)
└── QUICKSTART.md                 ~5 KB (Quick guide)

Small Files (<2KB):
├── app/api/routes.py             ~2 KB (API endpoints)
├── app/config.py                 ~1 KB (Settings)
├── app/main.py                   ~2 KB (App entry)
├── check_setup.py                ~2 KB (Verification)
├── setup.ps1                     ~2 KB (Setup script)
├── requirements.txt              <1 KB (Dependencies)
├── .env.example                  <1 KB (Env template)
└── All __init__.py files         <1 KB each
```

---

## 🚀 Quick Navigation

**To run the app:**
```powershell
python -m app.main
```

**To verify setup:**
```powershell
python check_setup.py
```

**To install everything:**
```powershell
.\setup.ps1
```

**To modify AI behavior:**
Edit: `app/agent/prompts.py`

**To change output structure:**
Edit: `app/models/schemas.py`

**To add new guidelines:**
Edit: `app/services/embeddings.py` (ANALYSIS_GUIDELINES)

---

## 📚 Related Reading

Each file contains extensive comments explaining:
- **Why** the code is structured this way
- **What** each function/class does
- **How** to extend or modify it

Look for comments starting with:
- `# Why:` - Explains design decisions
- `# Note:` - Important details
- `# Example:` - Usage examples
- `# TODO:` - Extension ideas

---

## ✅ Checklist: Files You've Read

Track your learning progress:

- [ ] README.md
- [ ] QUICKSTART.md
- [ ] app/main.py
- [ ] app/models/schemas.py
- [ ] app/agent/prompts.py
- [ ] app/agent/agent.py
- [ ] app/services/llm.py
- [ ] app/services/embeddings.py
- [ ] app/api/routes.py
- [ ] app/config.py
- [ ] app/templates/index.html
- [ ] PROJECT_SUMMARY.md

**Pro tip:** Read files in the order listed above for best learning flow!

---

**Last Updated:** January 7, 2026  
**Project Version:** 1.0.0
