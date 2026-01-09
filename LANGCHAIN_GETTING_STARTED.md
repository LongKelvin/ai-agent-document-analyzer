# LangChain Implementation - Getting Started

## What You'll Find Here

This project now includes **two parallel implementations**:

1. **Custom Implementation** (original) - Shows you how things work under the hood
2. **LangChain Implementation** (new) - Shows you industry-standard tools

Both implementations do the same thing, but LangChain makes it easier to build production-ready applications.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs both the original dependencies and the new LangChain packages:
- `langchain==0.3.13`
- `langchain-google-genai==2.0.5`
- `langchain-community==0.3.13`
- `langchain-chroma==0.1.4`

### 2. Choose Your Implementation

The app currently uses the **custom implementation** by default. Both versions work side-by-side.

---

## File Mapping

| Component | Custom (Original) | LangChain (New) |
|-----------|-------------------|-----------------|
| LLM Service | `services/llm.py` | `services/llm_langchain.py` |
| Vector DB | `services/vector_db.py` | `services/vector_db_langchain.py` |
| Q&A Agent | `agent/qa_agent.py` | `agent/qa_agent_langchain.py` |

---

## Learning Path

### Step 1: Understand the Custom Implementation
Start with the original files to understand fundamentals:

1. **Read `services/llm.py`** - How to call an LLM API
2. **Read `services/vector_db.py`** - How vector databases work
3. **Read `agent/qa_agent.py`** - How RAG pipelines work

### Step 2: Compare with LangChain
Now read the LangChain versions to see the difference:

1. **Read `services/llm_langchain.py`** - See how LangChain wraps LLMs
2. **Read `services/vector_db_langchain.py`** - See how LangChain simplifies vector DBs
3. **Read `agent/qa_agent_langchain.py`** - See LCEL chains in action

### Step 3: Read the Documentation
- **`LANGCHAIN_EXPLAINED.md`** - Complete guide to LangChain concepts
- **`LANGCHAIN_COMPARISON.md`** - Side-by-side code comparisons

---

## Key Concepts

### What is LCEL?
**LCEL (LangChain Expression Language)** lets you chain components with the `|` operator:

```python
# Instead of this (custom):
embeddings = embedding_model.encode(query)
results = vector_db.query(embeddings)
context = format_context(results)
prompt = build_prompt(context, question)
response = llm.generate(prompt)
answer = parse_response(response)

# You write this (LangChain):
chain = retriever | format_docs | prompt | llm | parser
answer = chain.invoke(question)
```

### What is a Retriever?
A **Retriever** is LangChain's standard interface for fetching relevant documents:

```python
# Get a retriever from any vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Use it in chains
chain = retriever | format_docs | prompt | llm
```

Retrievers work the same way for ChromaDB, Pinecone, FAISS, Weaviate, etc.

### What are Chains?
**Chains** are pre-built or custom pipelines:

```python
# Pre-built chain (simple, less control)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
answer = qa_chain.invoke({"query": "What is RAG?"})

# Custom LCEL chain (more control)
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)
answer = chain.invoke("What is RAG?")
```

---

## Testing the LangChain Version

### Option 1: Python Script
```python
from app.services.llm_langchain import get_langchain_llm_service
from app.services.vector_db_langchain import get_langchain_vector_db_service
from app.agent.qa_agent_langchain import get_langchain_qa_agent

# Test LLM
llm_service = get_langchain_llm_service()
response = llm_service.generate_response("Hello!")
print(response)

# Test Vector DB
vector_db = get_langchain_vector_db_service()
vector_db.add_document(
    document_id="test_doc",
    text="LangChain is a framework for building LLM applications.",
    metadata={"filename": "test.txt"}
)
results = vector_db.search("What is LangChain?", top_k=1)
print(results)

# Test Q&A Agent
qa_agent = get_langchain_qa_agent()
answer = qa_agent.answer_question("What is LangChain?")
print(answer)
```

### Option 2: Update Routes
To use LangChain in the web app, update `app/api/routes.py`:

```python
# Change this:
from app.services.vector_db import get_vector_db_service
from app.agent.qa_agent import get_qa_agent

# To this:
from app.services.vector_db_langchain import get_langchain_vector_db_service as get_vector_db_service
from app.agent.qa_agent_langchain import get_langchain_qa_agent as get_qa_agent
```

---

## Benefits of LangChain

### 1. Easy to Switch LLMs
```python
# Want to use OpenAI instead of Gemini? Just change one line:
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4")
```

### 2. Easy to Switch Vector DBs
```python
# Want to use Pinecone instead of ChromaDB? Just change one line:
from langchain_pinecone import Pinecone
vector_store = Pinecone(...)
```

### 3. Pre-built Chains
```python
# RAG Q&A in one line:
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Conversational Q&A with memory:
from langchain.chains import ConversationalRetrievalChain
qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
```

### 4. Less Code
- No manual JSON parsing
- No manual embedding generation
- No manual prompt concatenation
- Built-in error handling

---

## Common Questions

### Q: Which version should I use?
**A:** Both! Use custom for learning, use LangChain for building real applications.

### Q: Can I mix custom and LangChain?
**A:** Yes! They don't interfere with each other. Use what makes sense for each component.

### Q: Is LangChain faster?
**A:** Performance is similar. LangChain adds small overhead but provides better features.

### Q: Do I need to learn LCEL?
**A:** Not required, but it makes chains more readable and composable. Start with pre-built chains (RetrievalQA) first.

---

## Next Steps

1. **Read the documentation:**
   - `LANGCHAIN_EXPLAINED.md` - Complete guide
   - `LANGCHAIN_COMPARISON.md` - Side-by-side comparison

2. **Try the code:**
   - Run the test script above
   - Modify prompts and see how answers change
   - Try different embedding models or chunk sizes

3. **Build something new:**
   - Add conversation memory (ConversationalRetrievalChain)
   - Add multi-query retrieval
   - Add re-ranking or filtering

4. **Explore LangChain:**
   - Official docs: https://python.langchain.com/docs/
   - LangChain cookbook: https://github.com/langchain-ai/langchain/tree/master/cookbook

---

## Summary

- ✅ Both implementations (custom + LangChain) are fully functional
- ✅ LangChain version is in separate files (`*_langchain.py`)
- ✅ Extensive comments explain every concept
- ✅ Documentation shows side-by-side comparisons
- ✅ Easy to switch between implementations

**Learn with custom, build with LangChain!**
