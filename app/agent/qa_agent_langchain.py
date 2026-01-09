"""
Q&A Agent using LangChain Chains - Educational Version

WHAT IS THIS FILE?
This replaces the custom QAAgent (qa_agent.py) with LangChain's chain-based approach.

WHY USE LANGCHAIN CHAINS?
- Pre-built patterns: RetrievalQA, ConversationalRetrievalChain, etc.
- LCEL (LangChain Expression Language): Build custom chains with | operator
- Automatic prompt formatting: No manual string templates needed
- Built-in source tracking: Chains can return source documents automatically

WHAT CHANGED?
Before: We manually retrieved context, built prompts, called LLM, formatted output
After: LangChain chains do all of this automatically
"""

from typing import Dict, Any, Optional
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.services.llm_langchain import get_langchain_llm_service
from app.services.vector_db_langchain import get_langchain_vector_db_service


class LangChainQAAgent:
    """
    Q&A Agent using LangChain's RetrievalQA pattern.
    
    KEY LANGCHAIN CONCEPTS:
    1. Retriever: Fetches relevant documents (already implemented in vector_db)
    2. RetrievalQA Chain: Pre-built chain for RAG question-answering
    3. LCEL Chain: Custom chain using | operator for flexibility
    
    TWO APPROACHES SHOWN:
    - Method 1: RetrievalQA (simpler, less control)
    - Method 2: Custom LCEL chain (more control, more educational)
    """
    
    def __init__(self):
        """
        Initialize agent with LangChain services.
        
        BEHIND THE SCENES:
        - llm_service provides the LLM (Gemini via LangChain)
        - vector_db provides the Retriever (ChromaDB via LangChain)
        """
        self.llm_service = get_langchain_llm_service()
        self.vector_db = get_langchain_vector_db_service()
        self.llm = self.llm_service.llm  # Get the actual ChatGoogleGenerativeAI instance
        
        print("[LangChain QA Agent] Initialized")
    
    def answer_question_simple(
        self, 
        question: str, 
        document_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Answer questions using LangChain's RetrievalQA chain.
        
        THIS IS THE SIMPLEST WAY:
        RetrievalQA is a pre-built chain that:
        1. Takes your question
        2. Uses the retriever to find relevant docs
        3. Builds a prompt automatically
        4. Calls the LLM
        5. Returns the answer + source documents
        
        WHAT LANGCHAIN DOES FOR YOU:
        - Automatic prompt construction
        - Source document tracking
        - Error handling
        
        LIMITATION:
        Less control over the prompt format. For full control, use answer_question_custom().
        
        Args:
            question: User's question
            document_id: Optional document filter
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict with answer and sources
        """
        # Get retriever from vector store
        # Retriever is a LangChain abstraction that knows how to fetch relevant docs
        if document_id:
            retriever = self.vector_db.as_retriever(
                search_kwargs={"k": top_k, "filter": {"document_id": document_id}}
            )
        else:
            retriever = self.vector_db.as_retriever(search_kwargs={"k": top_k})
        
        # Create RetrievalQA chain
        # This is a pre-built chain that handles everything
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # "stuff" means "stuff all docs into one prompt"
            retriever=retriever,
            return_source_documents=True  # Include sources in response
        )
        
        # Run the chain
        # LangChain automatically: retrieves, prompts, calls LLM, formats output
        result = qa_chain.invoke({"query": question})
        
        # Format sources
        sources = []
        for i, doc in enumerate(result['source_documents'], 1):
            sources.append({
                "source_number": str(i),
                "text": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "document": doc.metadata.get('filename', 'Unknown'),
                "document_id": doc.metadata.get('document_id', 'Unknown')
            })
        
        return {
            "answer": result['result'],
            "sources": sources
        }
    
    def answer_question_custom(
        self, 
        question: str, 
        document_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Answer questions using custom LCEL chain for full control.
        
        THIS IS THE EDUCATIONAL APPROACH:
        LCEL (LangChain Expression Language) lets you build chains step by step:
        
        retriever | format_docs | prompt | llm | parser
        
        Each | means "pass output to the next step"
        
        WHY USE THIS?
        - Full control over prompts
        - Add custom processing steps
        - Easier to debug and modify
        - More educational (you see exactly what's happening)
        
        THE CHAIN BREAKDOWN:
        1. retriever: Fetch relevant chunks from vector DB
        2. format_docs: Convert docs to readable context string
        3. prompt: Inject context and question into template
        4. llm: Generate answer from Gemini
        5. parser: Extract clean text from LLM response
        
        Args:
            question: User's question
            document_id: Optional document filter
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict with answer and sources
        """
        # Step 1: Get retriever
        if document_id:
            retriever = self.vector_db.as_retriever(
                search_kwargs={"k": top_k, "filter": {"document_id": document_id}}
            )
        else:
            retriever = self.vector_db.as_retriever(search_kwargs={"k": top_k})
        
        # Step 2: Define custom prompt template
        # This gives us full control over what the AI sees
        template = """You are a helpful assistant that answers questions based ONLY on the provided context.

Rules:
1. Answer the question using ONLY information from the context provided
2. If the context doesn't contain enough information, say "I don't have enough information to answer that question."
3. Be concise and direct in your answer
4. Cite source numbers when referencing specific information (e.g., "According to Source 1...")
5. Do not make assumptions or add information not in the context
6. If multiple sources provide the same information, mention all relevant sources

Context from documents:
{context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate.from_template(template)
        
        # Step 3: Helper function to format retrieved docs
        def format_docs(docs):
            """Convert list of Document objects to formatted string."""
            formatted = []
            for i, doc in enumerate(docs, 1):
                formatted.append(f"[Source {i}]: {doc.page_content}")
            return "\n\n".join(formatted)
        
        # Step 4: Build the LCEL chain
        # Read this chain left to right:
        # "Get context and question, format them, send to LLM, parse output"
        chain = (
            {
                "context": retriever | format_docs,  # Retrieve docs and format them
                "question": RunnablePassthrough()  # Pass question through unchanged
            }
            | prompt  # Inject into prompt template
            | self.llm  # Send to Gemini
            | StrOutputParser()  # Extract text from response
        )
        
        # Step 5: Execute the chain
        # LangChain automatically manages the data flow
        answer = chain.invoke(question)
        
        # Step 6: Get source documents for citation
        # We need to retrieve again to get the actual docs
        # (In a production app, you'd optimize this)
        source_docs = retriever.invoke(question)
        
        sources = []
        for i, doc in enumerate(source_docs, 1):
            sources.append({
                "source_number": str(i),
                "text": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "document": doc.metadata.get('filename', 'Unknown'),
                "document_id": doc.metadata.get('document_id', 'Unknown')
            })
        
        return {
            "answer": answer.strip(),
            "sources": sources
        }
    
    def answer_question(
        self, 
        question: str, 
        document_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Main Q&A method (uses custom LCEL chain for educational purposes).
        
        WHICH METHOD TO USE?
        - answer_question_simple(): Easier, less code, less control
        - answer_question_custom(): More educational, full control, easier to modify
        
        For this educational project, we use the custom method so students can see
        exactly how the RAG pipeline works.
        
        Args:
            question: User's question
            document_id: Optional document filter
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict with answer and sources
        """
        # Use custom method for educational transparency
        return self.answer_question_custom(question, document_id, top_k)


# Singleton instance
_langchain_qa_agent = None


def get_langchain_qa_agent() -> LangChainQAAgent:
    """
    Get singleton instance of LangChainQAAgent.
    
    WHY SINGLETON?
    - Reuses LLM and vector DB connections
    - Faster response times
    - Less memory usage
    """
    global _langchain_qa_agent
    if _langchain_qa_agent is None:
        _langchain_qa_agent = LangChainQAAgent()
    return _langchain_qa_agent
