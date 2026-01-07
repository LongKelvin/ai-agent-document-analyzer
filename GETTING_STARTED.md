# Getting Started - Visual Guide

## Choose Your Path

```
┌─────────────────────────────────────────────────────────────┐
│ │
│ I want to get started FAST (5 minutes) │
│ -> Run: .\setup.ps1 │
│ -> Follow the wizard │
│ │
├─────────────────────────────────────────────────────────────┤
│ │
│ I want to understand before running │
│ -> Read: QUICKSTART.md │
│ -> Then: Manual setup below │
│ │
├─────────────────────────────────────────────────────────────┤
│ │
│ I want deep understanding │
│ -> Start: PROJECT_SUMMARY.md │
│ -> Then: Explore code files │
│ │
└─────────────────────────────────────────────────────────────┘
```

---

## Fast Track (Automated Setup)

### Step 1: Run Setup Script
```powershell
.\setup.ps1
```

The script will:
- [OK] Check Python installation
- [OK] Create virtual environment
- [OK] Install all dependencies
- [OK] Create .env file
- [OK] Verify installation

### Step 2: Add API Key
When prompted, add your Gemini API key to `.env`

Get your key: https://makersuite.google.com/app/apikey

### Step 3: Start Application
```powershell
python -m app.main
```

### Step 4: Open Browser
Navigate to: http://localhost:8000

**Done!**

---

## Manual Setup (Step-by-Step)

### 1. Create Virtual Environment
```powershell
python -m venv venv
```

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your prompt.

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

This takes 2-3 minutes.

### 4. Create Environment File
```powershell
Copy-Item .env.example .env
```

### 5. Add Your API Key
```powershell
notepad .env
```

Replace `your_api_key_here` with your actual Gemini API key.

Get key from: https://makersuite.google.com/app/apikey

### 6. Verify Setup (Optional)
```powershell
python check_setup.py
```

Should show all green checkmarks

### 7. Run Application
```powershell
python -m app.main
```

### 8. Open in Browser
http://localhost:8000

**Success!**

---

## Visual Project Map

```
 ai-agent-demo/
│
├── START HERE
│ ├── README.md ← Full documentation
│ ├── QUICKSTART.md ← 5-minute guide
│ ├── GETTING_STARTED.md ← This file
│ └── PROJECT_SUMMARY.md ← Deep dive
│
├── CONFIGURATION
│ ├── requirements.txt ← Dependencies
│ ├── .env.example ← Template
│ ├── .env ← YOUR API KEY HERE [WARN]
│ └── .gitignore ← Git rules
│
├── SETUP TOOLS
│ ├── setup.ps1 ← Automated setup
│ └── check_setup.py ← Verify installation
│
└── APPLICATION CODE
 └── app/
 ├── main.py ← Entry point
 ├── config.py ← Settings
 │
 ├── api/ ← REST API
 │ └── routes.py ← Endpoints
 │
 ├── agent/ ← AI AGENT
 │ ├── agent.py ← Orchestration
 │ └── prompts.py ← Prompt templates
 │
 ├── models/ ← DATA VALIDATION
 │ └── schemas.py ← Pydantic schemas
 │
 ├── services/ ← BUSINESS LOGIC
 │ ├── llm.py ← Gemini API
 │ └── embeddings.py ← RAG implementation
 │
 └── templates/ ← FRONTEND
 └── index.html ← Web UI
```

---

## First Time User Journey

```
You are here (1) Read this file (GETTING_STARTED.md)
 |
 2. Run setup.ps1 OR follow manual steps
 |
 3. Add Gemini API key to .env
 |
 4. Run: python check_setup.py
 |
 5. Run: python -m app.main
 |
 6. Open: http://localhost:8000
 |
 7. Paste sample document
 |
 8. Click "Analyze Document"
 |
 9. See AI analysis!
 |
 10. Read PROJECT_SUMMARY.md to understand
 |
 11. Explore code files
 |
 12. Modify and experiment!
```

---

## Quick Commands Reference

### Setup Commands
```powershell
# Automated setup
.\setup.ps1

# Manual setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

### Run Commands
```powershell
# Start application
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload

# Verify setup
python check_setup.py
```

### Development Commands
```powershell
# Activate venv (always do this first)
.\venv\Scripts\Activate.ps1

# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Deactivate venv
deactivate
```

---

## Troubleshooting Quick Fixes

### [FAIL] "Module not found"
```powershell
# Make sure venv is activated (see "venv" in prompt)
.\venv\Scripts\Activate.ps1

# Reinstall packages
pip install -r requirements.txt
```

### [FAIL] "Execution policy" error
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### [FAIL] "Port 8000 already in use"
```powershell
# Use different port
uvicorn app.main:app --reload --port 8001
```

### [FAIL] "API key not configured"
```powershell
# Check .env file exists
ls .env

# Edit and add your key
notepad .env
```

### [FAIL] "Import errors in IDE"
- Make sure you selected the venv Python interpreter
- In VS Code: Ctrl+Shift+P -> "Python: Select Interpreter" -> Choose venv

---

## What You'll See

### Terminal Output (Success)
```
 AI Agent Demo Application Starting...
 Initializing services...
[OK] Application ready!
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO: Started reloader process
INFO: Started server process
INFO: Waiting for application startup.
INFO: Application startup complete.
```

### Browser Interface
```
┌─────────────────────────────────────────────────────────┐
│ AI Agent Document Analysis Demo │
│ Educational demo using FastAPI, Gemini, and RAG │
├─────────────────────────────────────────────────────────┤
│ │
│ Input Document │ Analysis Result │
│ ┌──────────────────┐ │ ┌──────────────────┐ │
│ │ [Text area] │ │ │ [Results here] │ │
│ │ │ │ │ │ │
│ └──────────────────┘ │ └──────────────────┘ │
│ [ Analyze Document] │ │
│ │
└─────────────────────────────────────────────────────────┘
```

---

## Learning Path

### Beginner Path
1. [OK] Get it running (this guide)
2. [OK] Try sample documents
3. [OK] Read QUICKSTART.md
4. [OK] Read README.md
5. [OK] Understand PROJECT_SUMMARY.md

### Intermediate Path
6. [OK] Read `app/models/schemas.py`
7. [OK] Read `app/agent/prompts.py`
8. [OK] Modify prompts and see changes
9. [OK] Add new fields to schema

### Advanced Path
10. [OK] Read `app/services/embeddings.py`
11. [OK] Read `app/agent/agent.py`
12. [OK] Add new analysis types
13. [OK] Implement tool calling
14. [OK] Deploy to production

---

## Sample Documents to Try

### 1. Incomplete Document (will find issues)
```
Project Proposal: Build a Mobile App

We need a mobile app for our business.

Features:
- User login
- Push notifications
```

### 2. Complete Document (will pass)
```
Technical Specification: User Authentication System

Introduction:
This document outlines the authentication system for our web platform.

Requirements:
- Email/password login
- JWT token-based sessions
- Password reset via email
- Two-factor authentication (optional)

Technical Details:
- Backend: Python/FastAPI
- Database: PostgreSQL
- Tokens: 24-hour expiry
- Security: Bcrypt password hashing

Implementation Plan:
Phase 1: Basic email/password (Week 1-2)
Phase 2: Password reset (Week 3)
Phase 3: 2FA (Week 4)

Conclusion:
This system will provide secure authentication for all users.

References:
- OWASP Authentication Guidelines
- JWT Best Practices RFC 8725
```

---

## Success Checklist

After setup, you should be able to:

- [ ] Run `python -m app.main` without errors
- [ ] See "Application ready!" in terminal
- [ ] Open http://localhost:8000 in browser
- [ ] See the web interface load
- [ ] Paste text in the textarea
- [ ] Click "Analyze Document"
- [ ] See analysis results appear

If all checked, **you're ready to learn!**

---

## Next Steps After Setup

1. **Try It Out**
 - Test with sample documents
 - See how it analyzes different texts

2. **Understand It**
 - Read PROJECT_SUMMARY.md
 - Explore code files
 - Follow FILE_INDEX.md

3. **Modify It**
 - Change prompts
 - Add new fields
 - Experiment!

4. **Extend It**
 - Add new features
 - Try different models
 - Build something new

---

## Need Help?

### Check These Files:
- **Setup issues:** QUICKSTART.md
- **Understanding concepts:** PROJECT_SUMMARY.md
- **File purposes:** FILE_INDEX.md
- **Full documentation:** README.md

### Common Issues:
- Python not installed -> Install from python.org
- API key missing -> Get from makersuite.google.com
- Import errors -> Activate venv and reinstall
- Port in use -> Use different port

---

## Ready to Start?

Choose your method:

**Fast (Automated):**
```powershell
.\setup.ps1
```

**Manual (Step-by-step):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env # Add API key
python -m app.main
```

**Then open:** http://localhost:8000

---

**Let's build some AI!**
