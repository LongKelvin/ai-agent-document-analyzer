# LangChain Integration - Educational Guide

## Overview

This document explains how we refactored the AI Agent Demo to use LangChain, replacing custom implementations with standardized LangChain components.

**Goal:** Make the code more maintainable, educational, and demonstrate industry-standard AI development patterns.

---

## What is LangChain?

**LangChain** is a framework for building applications with Large Language Models (LLMs). It provides:

1. **Standardized interfaces** for LLMs, vector databases, and retrievers
2. **Pre-built chains** for common patterns (RAG, Q&A, summarization)
3. **LCEL (LangChain Expression Language)** for building custom pipelines
4. **Easy switching** between different LLMs and vector DBs

**Analogy:** LangChain is like React for AI applications - it gives you reusable components instead of building everything from scratch.

---

## What Changed?

### Before (Custom Implementation)
```
User Question
    ↓
1. Manual ChromaDB query
2. Manual embedding generation
3. Manual prompt string concatenation
4. Manual API call to Gemini
5. Manual JSON parsing with regex
6. Manual Pydantic validation
    ↓
Answer
```

### After (LangChain)
```
User Question
    ↓
1. LangChain Retriever (handles embedding + search)
2. LangChain Prompt Template (structured prompts)
3. LangChain LLM Wrapper (handles API calls)
4. LangChain Output Parser (handles parsing)
5. LangChain Chain (orchestrates 1-4 automatically)
    ↓
Answer
```

---

## File-by-File Breakdown

### 1. `app/services/llm_langchain.py` (New)

**Replaces:** `app/services/llm.py`

**Key Changes:**
- Uses `ChatGoogleGenerativeAI` instead of `google.generativeai` directly
- Uses `ChatPromptTemplate` for structured prompts (system + user messages)
- Uses `JsonOutputParser` to extract JSON (no more regex!)
- Supports LCEL chains with `|` operator

**Educational Value:**
- Shows how LangChain wraps LLM APIs
- Demonstrates prompt templates (cleaner than string concatenation)
- Introduces LCEL (LangChain Expression Language) for chaining

**Example:**
```python
# OLD WAY (Custom)
response = genai.generate_content(system_prompt + user_prompt)
json_str = re.search(r'{.*}', response.text).group(0)
result = json.loads(json_str)

# NEW WAY (LangChain)
chain = prompt_template | llm | json_parser
result = chain.invoke({"system": system_prompt, "user": user_prompt})
```

---

### 2. `app/services/vector_db_langchain.py` (New)

**Replaces:** `app/services/vector_db.py`

**Key Changes:**
- Uses `Chroma` (LangChain wrapper) instead of `chromadb.PersistentClient`
- Uses `HuggingFaceEmbeddings` (LangChain wrapper) for embeddings
- Uses `RecursiveCharacterTextSplitter` for intelligent chunking
- Provides `as_retriever()` method for chain integration
- Uses `Document` objects (LangChain's standard format)

**Educational Value:**
- Shows how LangChain standardizes vector DB access
- Demonstrates intelligent text splitting (respects sentence boundaries)
- Introduces Retriever interface (used in chains)

**Example:**
```python
# OLD WAY (Custom)
chunks = manual_chunk_text(text, 500, 50)
embeddings = embedding_model.encode(chunks)
collection.add(ids=ids, embeddings=embeddings, documents=chunks)

# NEW WAY (LangChain)
docs = [Document(page_content=text, metadata=metadata)]
chunks = text_splitter.split_documents(docs)
vector_store.add_documents(chunks)  # Handles embedding automatically
```

---

### 3. `app/agent/qa_agent_langchain.py` (New)

**Replaces:** `app/agent/qa_agent.py`

**Key Changes:**
- Offers two approaches:
  1. **RetrievalQA** (pre-built chain, less control)
  2. **Custom LCEL chain** (full control, more educational)
- Uses `Retriever` from vector store
- Uses `PromptTemplate` for custom prompts
- Uses LCEL `|` operator to chain components

**Educational Value:**
- Shows both simple and advanced LangChain patterns
- Demonstrates RAG pipeline step by step
- Introduces LCEL for custom chains

**Example (Custom LCEL Chain):**
```python
# This chain:
# 1. Retrieves relevant docs
# 2. Formats them into context string
# 3. Injects into prompt template
# 4. Sends to LLM
# 5. Parses output

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

answer = chain.invoke(question)
```

---

## Key LangChain Concepts Explained

### 1. Document
```python
from langchain_core.documents import Document

doc = Document(
    page_content="Text content here",
    metadata={"source": "file.txt", "page": 1}
)
```
**What it is:** LangChain's standard format for text + metadata.  
**Why use it:** Works with all LangChain tools (splitters, retrievers, chains).

---

### 2. Embeddings
```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```
**What it is:** Wrapper for embedding models (HuggingFace, OpenAI, etc.).  
**Why use it:** Easy to switch models without changing your code.

---

### 3. VectorStore
```python
from langchain_chroma import Chroma

vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```
**What it is:** Wrapper for vector databases (Chroma, Pinecone, FAISS, etc.).  
**Why use it:** Easy to switch databases without changing your code.

---

### 4. Retriever
```python
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
docs = retriever.invoke("What is RAG?")
```
**What it is:** Interface for fetching relevant documents.  
**Why use it:** Plugs into chains, supports filtering and ranking.

---

### 5. PromptTemplate
```python
from langchain_core.prompts import PromptTemplate

template = "Answer this question: {question}\nContext: {context}"
prompt = PromptTemplate.from_template(template)
formatted = prompt.invoke({"question": "...", "context": "..."})
```
**What it is:** Structured way to build prompts with variables.  
**Why use it:** Cleaner than string concatenation, supports validation.

---

### 6. LLM Wrappers
```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
response = llm.invoke("Hello!")
```
**What it is:** Wrapper for LLM APIs (Google, OpenAI, Anthropic, etc.).  
**Why use it:** Standardized interface, easy to switch models.

---

### 7. LCEL (LangChain Expression Language)
```python
chain = prompt | llm | output_parser
result = chain.invoke(input_data)
```
**What it is:** Way to connect components using `|` operator.  
**Why use it:** Readable, composable, easy to debug.

**How it works:** Each component receives input, processes it, passes output to next component.

---

## How to Use the LangChain Version

### Option 1: Keep Using Original Implementation
The original files (`llm.py`, `vector_db.py`, `qa_agent.py`) still work. No changes needed.

### Option 2: Switch to LangChain
Update your imports to use the new `_langchain` versions:

```python
# OLD
from app.services.llm import get_gemini_service
from app.services.vector_db import get_vector_db_service
from app.agent.qa_agent import get_qa_agent

# NEW
from app.services.llm_langchain import get_langchain_llm_service
from app.services.vector_db_langchain import get_langchain_vector_db_service
from app.agent.qa_agent_langchain import get_langchain_qa_agent
```

---

## Benefits of LangChain

### 1. **Easier to Switch Components**
Want to use OpenAI instead of Gemini?
```python
# Just change one line:
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4")
```

Want to use Pinecone instead of ChromaDB?
```python
# Just change one line:
from langchain_pinecone import Pinecone
vector_store = Pinecone(...)
```

### 2. **Less Code to Maintain**
- No manual JSON parsing with regex
- No manual embedding generation
- No manual prompt string concatenation
- Built-in error handling

### 3. **Industry Standard**
- LangChain is widely used in production
- Lots of documentation and examples
- Active community support

### 4. **Pre-built Chains**
- RetrievalQA for RAG Q&A
- ConversationalRetrievalChain for chat
- Summarization chains
- And many more...

---

## Learning Path

### Beginner
1. Read `llm_langchain.py` - understand LLM wrappers
2. Read `vector_db_langchain.py` - understand vector stores and retrievers
3. Try `answer_question_simple()` in `qa_agent_langchain.py` - see RetrievalQA in action

### Intermediate
1. Read `answer_question_custom()` - understand LCEL chains
2. Modify the prompt template - see how it affects answers
3. Try different embedding models or chunk sizes

### Advanced
1. Build your own custom chain using LCEL
2. Add conversation memory (ConversationalRetrievalChain)
3. Implement multi-query retrieval or re-ranking
4. Add tool calling or function execution

---

## Common Questions

### Q: Should I use the original or LangChain version?
**A:** Both work! Use original for learning fundamentals, use LangChain for production projects.

### Q: Is LangChain faster?
**A:** Performance is similar. LangChain adds small overhead but provides better error handling.

### Q: Can I mix original and LangChain?
**A:** Yes! You can use LangChain for some parts and original for others.

### Q: What if I want to use a different LLM?
**A:** With LangChain, just change the LLM wrapper. With original, you'd need to rewrite `llm.py`.

---

## Next Steps

1. **Test the LangChain version:** Run the app and compare outputs
2. **Experiment:** Try different prompts, models, or chunk sizes
3. **Build something new:** Use LangChain to add conversation memory or multi-step reasoning
4. **Read official docs:** https://python.langchain.com/docs/

---

## Summary

**What we did:**
- Replaced custom LLM calls with LangChain's `ChatGoogleGenerativeAI`
- Replaced manual ChromaDB with LangChain's `Chroma` wrapper
- Replaced manual RAG logic with LangChain's `Retriever` and chains
- Added LCEL chains for flexibility

**Why it matters:**
- More maintainable code
- Industry-standard patterns
- Easier to extend and modify
- Better educational value (students learn real-world tools)

**The power of LangChain:**
Instead of reinventing the wheel, we use battle-tested components that thousands of developers rely on in production.
