# 🤖 AI Agent Document Analysis Demo

[![Powered by Claude Sonnet 4.5](https://img.shields.io/badge/AI-Claude%20Sonnet%204.5-blue)](https://www.anthropic.com/claude)
[![Built with Gemini 2.0](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-orange)](https://deepmind.google/technologies/gemini/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

> 🎓 **Educational AI Agent Demo** - Learn to build production-grade AI agents with RAG, prompt engineering, and structured validation.

---

## 🌟 Built With AI

**This entire project was architected and developed by Claude Sonnet 4.5** (Anthropic), demonstrating AI-assisted software engineering at its finest. Every line of code, documentation, and architectural decision showcases what's possible when human vision meets AI capability.

**Runtime powered by Google Gemini 2.0 Flash** - The latest and fastest Gemini model for production AI applications.

---

## 🎯 What You'll Learn

This project demonstrates professional AI Agent development:
- **AI Agent Architecture** - Treating LLMs as untrusted components
- **RAG (Retrieval-Augmented Generation)** - Semantic search with embeddings
- **Prompt Engineering** - Prompts as strict contracts
- **Structured Output** - Pydantic validation for LLM responses
- **Evidence-Based AI** - No hallucination, only facts
- **Clean Architecture** - Production-ready code organization

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key ([Get free key](https://makersuite.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-agent-document-analyzer.git
cd ai-agent-document-analyzer

# Automated setup (Windows)
.\setup.ps1

# Or manual setup
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Run

```bash
python -m app.main
```

Open http://localhost:8000 in your browser 🎉

---

## 📚 Documentation

- **[START_HERE.md](START_HERE.md)** - Documentation master index
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick visual guide
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Deep educational dive
- **[FILE_INDEX.md](FILE_INDEX.md)** - Complete file reference

---

## 🏗️ Architecture

```
app/
├── main.py              # FastAPI entry point
├── config.py            # Configuration management
├── api/
│   └── routes.py        # REST endpoints
├── agent/
│   ├── agent.py         # AI orchestration
│   └── prompts.py       # Prompt engineering
├── models/
│   └── schemas.py       # Pydantic validation
├── services/
│   ├── llm.py           # Gemini 2.0 Flash integration
│   └── embeddings.py    # RAG implementation
└── templates/
    └── index.html       # Web interface
```

---

## 🎯 Key Features

✅ **AI Agent with RAG** - Retrieves relevant context before analysis  
✅ **Structured Output** - Pydantic ensures type safety  
✅ **Evidence-Based** - Only references document content  
✅ **No Hallucination** - Agent can say "unknown"  
✅ **Clean Code** - Extensive comments explaining WHY  
✅ **Educational** - Built for learning and teaching  

---

## 🔧 Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **AI/ML**: Google Gemini 2.0 Flash, LangChain, sentence-transformers
- **Validation**: Pydantic v2
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Vector Search**: In-memory with NumPy (educational)

---

## 📖 How It Works

1. **User submits document** via web interface
2. **RAG retrieval** finds relevant analysis guidelines using embeddings
3. **Prompt construction** injects guidelines + document into template
4. **Gemini 2.0 Flash** generates structured JSON analysis
5. **Pydantic validation** ensures output matches schema
6. **Results displayed** with summary, status, evidence, and confidence

---

## 🎓 Learning Path

### Beginner (20 minutes)
1. Run the application
2. Try sample documents
3. Read QUICKSTART.md

### Intermediate (2 hours)
4. Read PROJECT_SUMMARY.md
5. Study `app/agent/prompts.py`
6. Modify prompts and test

### Advanced (Full day)
7. Study RAG in `app/services/embeddings.py`
8. Add new analysis types
9. Implement tool calling
10. Deploy to production

---

## 🛠️ Customization

### Easy Modifications
- **Prompts**: Edit `app/agent/prompts.py`
- **Guidelines**: Modify `app/services/embeddings.py`
- **Output Schema**: Update `app/models/schemas.py`
- **UI**: Customize `app/templates/index.html`

### Extension Ideas
- Add sentiment analysis
- Implement conversation history
- Try different LLM models
- Add real vector database (Pinecone, Weaviate)
- Deploy with Docker

---

## 📊 API Endpoints

### `GET /`
Serves web interface

### `POST /analyze`
Analyzes document

**Request:**
```json
{
  "document_text": "Your document here..."
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "summary": "Brief summary",
    "completeness_status": "partial",
    "missing_points": ["Section A", "Section B"],
    "evidence": ["Quote 1", "Quote 2"],
    "confidence": 0.85
  }
}
```

### `GET /health`
Health check endpoint

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Fork and experiment
- Suggest improvements
- Share your learnings
- Build upon it

---

## 📝 License

Educational use - Free to learn, modify, and extend.

---

## 🙏 Acknowledgments

- **Claude Sonnet 4.5** (Anthropic) - Project architecture and development
- **Google Gemini 2.0 Flash** - Runtime AI model
- **FastAPI** - Web framework
- **LangChain** - Agent orchestration
- **Pydantic** - Data validation

---

## 📧 Support

- **Documentation**: See [START_HERE.md](START_HERE.md)
- **Issues**: Check troubleshooting guides in docs
- **Learning**: Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🌟 Star History

If this project helped you learn AI Agent development, consider giving it a star! ⭐

---

**Built with 🤖 by Claude Sonnet 4.5 | Powered by ⚡ Gemini 2.0 Flash**

*Demonstrating the future of AI-assisted software development*
