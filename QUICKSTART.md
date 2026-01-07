# Quick Start Guide

## Get Started in 5 Minutes

### Step 1: Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

⏳ This may take 2-3 minutes. First install will download:
- FastAPI and dependencies
- Google Generative AI SDK
- Sentence transformers model (~80MB)

### Step 3: Configure API Key

1. Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

2. Get your Gemini API key:
 - Go to https://makersuite.google.com/app/apikey
 - Click "Create API Key"
 - Copy the key

3. Edit `.env` and paste your key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Verify Setup (Optional)

```powershell
python check_setup.py
```

This will check:
- [OK] All packages installed
- [OK] API key configured
- [OK] Project structure correct

### Step 5: Run the Application

```powershell
python -m app.main
```

You should see:
```
AI Agent Demo Application Starting...
Initializing services...
Application ready!
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Open in Browser

Navigate to: **http://localhost:8000**

---

## Try It Out

1. **Paste a document** in the text area
2. **Click "Analyze Document"**
3. **View the AI analysis** with:
 - Summary
 - Completeness status
 - Missing points (if any)
 - Evidence from document
 - Confidence score

---

## Sample Documents to Test

### Test 1: Incomplete Document
```
Project Proposal: AI Task Manager

We want to build an AI-powered task manager.

Features:
- Task creation
- Priority suggestions
```

**Expected Result:** Status = "partial", will identify missing sections

### Test 2: Complete Document
```
Technical Specification: User Authentication API

Introduction:
This document specifies the authentication endpoints for our web application.

Requirements:
1. User registration with email verification
2. Login with JWT token generation
3. Password reset functionality
4. Rate limiting on auth endpoints

Endpoints:
POST /auth/register - Create new user account
POST /auth/login - Authenticate and get token
POST /auth/reset-password - Reset password via email

Security Considerations:
- Passwords hashed with bcrypt
- JWT tokens expire after 24 hours
- Rate limit: 5 attempts per minute per IP

Conclusion:
This specification covers all authentication requirements for the MVP release.

References:
- OAuth 2.0 RFC 6749
- JWT RFC 7519
```

**Expected Result:** Status = "complete", high confidence

---

## Troubleshooting

### "Module not found" errors
```powershell
# Make sure venv is activated (you should see (venv) in prompt)
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### "API key not configured"
```powershell
# Check if .env exists
ls .env

# If not, copy from example
Copy-Item .env.example .env

# Edit .env and add your key
notepad .env
```

### Port 8000 already in use
```powershell
# Use a different port
uvicorn app.main:app --reload --port 8001
```

---

## Learning Path

After getting it running, explore:

1. **`app/models/schemas.py`** - See how Pydantic validates LLM output
2. **`app/agent/prompts.py`** - Study the prompt engineering
3. **`app/services/embeddings.py`** - Understand RAG implementation
4. **`app/agent/agent.py`** - See how everything orchestrates

---

## Making Changes

The app runs with auto-reload enabled. Edit any `.py` file and the server will automatically restart.

Try modifying:
- System prompt in `app/agent/prompts.py`
- Analysis guidelines in `app/services/embeddings.py`
- Pydantic schema in `app/models/schemas.py`

---

## Next Steps

- Add more analysis types (sentiment, readability, etc.)
- Implement tool calling with LangChain
- Add conversation history
- Try different LLM models
- Experiment with prompt variations

---

**Need Help?** Check the full README.md for detailed documentation.
