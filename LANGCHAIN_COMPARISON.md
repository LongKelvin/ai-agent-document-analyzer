# LangChain vs Custom Implementation - Side-by-Side Comparison

This document shows the exact differences between the original custom implementation and the new LangChain version.

---

## 1. LLM Service Comparison

### Custom Implementation (`llm.py`)
```python
import google.generativeai as genai
import json
import re

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model_name,
            generation_config={"temperature": settings.temperature}
        )
    
    def generate_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
    
    def extract_json_from_response(self, response_text: str) -> Dict:
        # Manual regex to find JSON in response
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r'\{.*\}', response_text)
            json_str = json_match.group(0) if json_match else response_text
        
        return json.loads(json_str)
```

### LangChain Implementation (`llm_langchain.py`)
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class LangChainLLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model_name,
            temperature=settings.temperature,
            google_api_key=settings.gemini_api_key
        )
    
    def generate_response(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content
    
    def generate_structured_response(self, system_prompt: str, user_prompt: str):
        # LangChain handles prompt formatting and JSON extraction
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "{system_instructions}"),
            ("human", "{user_input}")
        ])
        
        json_parser = JsonOutputParser()
        
        # LCEL chain: prompt -> LLM -> parse JSON
        chain = prompt_template | self.llm | json_parser
        
        return chain.invoke({
            "system_instructions": system_prompt,
            "user_input": user_prompt
        })
```

**Key Differences:**
- ✅ LangChain: No manual regex, no try/catch for JSON parsing
- ✅ LangChain: Structured prompts with ChatPromptTemplate
- ✅ LangChain: LCEL chains (`|` operator) for readable pipelines

---

## 2. Vector DB Service Comparison

### Custom Implementation (`vector_db.py`)
```python
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class VectorDBService:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(name="documents")
        self.embedding_model = SentenceTransformer(settings.embedding_model_name)
    
    def add_document(self, document_id: str, text: str, metadata: Dict):
        # Manual chunking
        chunks = self._chunk_text(text, chunk_size=500, overlap=50)
        
        # Manual embedding generation
        embeddings = self.embedding_model.encode(chunks).tolist()
        
        # Manual ID generation
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Add to ChromaDB
        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=[{**metadata, "document_id": document_id, "chunk_index": i} 
                       for i in range(len(chunks))]
        )
    
    def search(self, query: str, top_k: int = 5):
        # Manual query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Manual search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Manual result formatting
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i]
            })
        return formatted_results
```

### LangChain Implementation (`vector_db_langchain.py`)
```python
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class LangChainVectorDBService:
    def __init__(self, persist_directory: str = "./chroma_db"):
        # LangChain wraps embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name,
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # LangChain wraps ChromaDB
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embedding_model,
            persist_directory=persist_directory
        )
        
        # Intelligent text splitter (respects sentence boundaries)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def add_document(self, document_id: str, text: str, metadata: Dict):
        # Create LangChain Document
        doc = Document(
            page_content=text,
            metadata={**metadata, "document_id": document_id}
        )
        
        # Split using intelligent splitter
        chunks = self.text_splitter.split_documents([doc])
        
        # Add metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)
        
        # LangChain handles: embedding generation, ID generation, storage
        self.vector_store.add_documents(chunks)
    
    def search(self, query: str, top_k: int = 5):
        # LangChain handles: query embedding, search, result formatting
        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=top_k
        )
        
        # Format to match old interface
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "text": doc.page_content,
                "metadata": doc.metadata,
                "distance": score
            })
        return formatted_results
    
    def as_retriever(self, search_kwargs=None):
        # NEW: Return LangChain Retriever for use in chains
        if search_kwargs is None:
            search_kwargs = {"k": 5}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
```

**Key Differences:**
- ✅ LangChain: Automatic embedding generation (no manual encode)
- ✅ LangChain: Intelligent text splitting (respects sentence boundaries)
- ✅ LangChain: `as_retriever()` method for chain integration
- ✅ LangChain: Standardized `Document` format

---

## 3. Q&A Agent Comparison

### Custom Implementation (`qa_agent.py`)
```python
class QAAgent:
    def __init__(self):
        self.llm_service = get_gemini_service()
        self.vector_db = get_vector_db_service()
    
    def answer_question(self, question: str, top_k: int = 5):
        # Step 1: Manual retrieval
        search_results = self.vector_db.search(query=question, top_k=top_k)
        
        # Step 2: Manual context formatting
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"[Source {i}]: {result['text']}")
        context = "\n\n".join(context_parts)
        
        # Step 3: Manual prompt building
        prompt = self._build_qa_prompt(question, context)
        
        # Step 4: Manual LLM call
        answer = self.llm_service.generate_response(prompt)
        
        # Step 5: Manual response formatting
        return {
            "answer": answer.strip(),
            "sources": [...]
        }
    
    def _build_qa_prompt(self, question: str, context: str) -> str:
        # Manual string concatenation
        system_instructions = """You are a helpful assistant..."""
        user_prompt = f"""Context from documents:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"""
        return f"{system_instructions}\n\n{user_prompt}"
```

### LangChain Implementation (`qa_agent_langchain.py`)
```python
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class LangChainQAAgent:
    def __init__(self):
        self.llm_service = get_langchain_llm_service()
        self.vector_db = get_langchain_vector_db_service()
        self.llm = self.llm_service.llm
    
    # METHOD 1: Pre-built RetrievalQA chain
    def answer_question_simple(self, question: str, top_k: int = 5):
        retriever = self.vector_db.as_retriever(search_kwargs={"k": top_k})
        
        # One-liner RAG chain!
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True
        )
        
        return qa_chain.invoke({"query": question})
    
    # METHOD 2: Custom LCEL chain (more control)
    def answer_question_custom(self, question: str, top_k: int = 5):
        retriever = self.vector_db.as_retriever(search_kwargs={"k": top_k})
        
        # Define prompt template
        template = """You are a helpful assistant...

Context: {context}
Question: {question}
Answer:"""
        prompt = PromptTemplate.from_template(template)
        
        # Helper function to format docs
        def format_docs(docs):
            return "\n\n".join([f"[Source {i}]: {doc.page_content}" 
                               for i, doc in enumerate(docs, 1)])
        
        # LCEL chain: retriever -> format -> prompt -> LLM -> parse
        chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return {"answer": chain.invoke(question), "sources": [...]}
```

**Key Differences:**
- ✅ LangChain: Pre-built `RetrievalQA` chain (one-liner!)
- ✅ LangChain: LCEL custom chains for full control
- ✅ LangChain: No manual prompt concatenation
- ✅ LangChain: Automatic source tracking
- ✅ LangChain: `Retriever` abstraction (works with any vector DB)

---

## 4. Code Length Comparison

### Custom Implementation (Total Lines)
- `llm.py`: ~140 lines
- `vector_db.py`: ~227 lines
- `qa_agent.py`: ~120 lines
- **Total: ~487 lines**

### LangChain Implementation (Total Lines)
- `llm_langchain.py`: ~180 lines (with extensive educational comments)
- `vector_db_langchain.py`: ~225 lines (with extensive educational comments)
- `qa_agent_langchain.py`: ~240 lines (with extensive educational comments)
- **Total: ~645 lines**

**Note:** LangChain version has more lines because of educational comments. The actual code is shorter!

**Without comments:**
- Custom: ~350 lines
- LangChain: ~200 lines

---

## 5. Feature Comparison

| Feature | Custom | LangChain |
|---------|--------|-----------|
| LLM API calls | ✅ Manual | ✅ Wrapped |
| JSON parsing | ⚠️ Regex | ✅ Built-in parser |
| Prompt templates | ⚠️ String concat | ✅ PromptTemplate |
| Vector DB | ✅ ChromaDB | ✅ Chroma (wrapped) |
| Embeddings | ✅ SentenceTransformer | ✅ HuggingFaceEmbeddings |
| Text chunking | ⚠️ Manual | ✅ RecursiveCharacterTextSplitter |
| RAG chains | ⚠️ Manual | ✅ RetrievalQA + LCEL |
| Retrievers | ❌ None | ✅ Built-in |
| Switch LLMs | ❌ Rewrite code | ✅ Change one line |
| Switch vector DB | ❌ Rewrite code | ✅ Change one line |
| Error handling | ⚠️ Manual | ✅ Built-in |
| Conversation memory | ❌ Not implemented | ✅ Easy to add |

---

## 6. When to Use Which?

### Use Custom Implementation When:
- Learning fundamentals (how embeddings, RAG, prompts work)
- Building a minimal prototype
- You need 100% control over every detail
- You want to avoid external dependencies

### Use LangChain When:
- Building production applications
- You need to switch between LLMs/vector DBs
- You want pre-built chains (RetrievalQA, ConversationalRetrievalChain)
- You want industry-standard patterns
- You need conversation memory, tool calling, or agents

---

## 7. Migration Guide

To switch from custom to LangChain:

1. **Install dependencies:**
   ```bash
   pip install langchain-chroma==0.1.4
   ```

2. **Update imports in your code:**
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

3. **Update method calls (if needed):**
   Most methods have the same signature, but check the documentation for any differences.

4. **Test thoroughly:**
   Both versions should produce similar results, but prompts may need tweaking.

---

## Summary

**Custom Implementation:**
- ✅ Great for learning fundamentals
- ✅ No extra dependencies
- ❌ More code to maintain
- ❌ Hard to switch components

**LangChain Implementation:**
- ✅ Industry standard
- ✅ Less code (without comments)
- ✅ Easy to switch LLMs/vector DBs
- ✅ Pre-built chains and patterns
- ❌ Extra dependency (LangChain)
- ❌ Learning curve for LCEL

**Recommendation:** Learn with custom, build with LangChain!
