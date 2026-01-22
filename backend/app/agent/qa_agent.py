"""
Q&A Agent for answering questions about uploaded documents.

This agent uses RAG to retrieve relevant context and answer questions.
"""

from typing import List, Dict, Any
from app.services.llm import get_gemini_service
from app.services.vector_db import get_vector_db_service


class QAAgent:
    """
    Question-Answering Agent using RAG.
    
    This agent:
    1. Retrieves relevant document chunks using semantic search
    2. Constructs a prompt with context
    3. Gets answer from LLM
    4. Returns answer with source citations
    """
    
    def __init__(self):
        """Initialize agent with required services."""
        self.llm_service = get_gemini_service()
        self.vector_db = get_vector_db_service()
    
    def answer_question(
        self, 
        question: str, 
        document_id: str = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Answer a question about documents using RAG.
        
        Args:
            question: User's question
            document_id: Optional specific document to query
            top_k: Number of relevant chunks to retrieve
            
        Returns:
            Dict with 'answer' and 'sources' keys
        """
        # Step 1: Retrieve relevant context
        print(f"      → Sub-step 2.1: Retrieving relevant context from Vector DB...")
        print(f"      • Query: {question[:60]}...")
        print(f"      • Top K: {top_k}")
        search_results = self.vector_db.search(
            query=question,
            top_k=top_k,
            document_id=document_id
        )
        
        if not search_results:
            print(f"      ⚠ No documents found in database")
            return {
                "answer": "I don't have any documents to answer this question. Please upload documents first.",
                "sources": []
            }
        
        print(f"      • Found {len(search_results)} relevant chunks:")
        for idx, result in enumerate(search_results, 1):
            chunk_idx = result['metadata'].get('chunk_index', 0)
            total_chunks = result['metadata'].get('total_chunks', 1)
            filename = result['metadata'].get('filename', 'Unknown')
            print(f"        [{idx}] {filename} - Chunk {chunk_idx+1}/{total_chunks} ({len(result['text'])} chars)")
        print(f"      ✓ Context retrieved")
        
        # Step 2: Build context from search results
        print(f"    → Sub-step 2.2: Assembling context from search results...")
        context_parts = []
        sources = []
        
        for i, result in enumerate(search_results, 1):
            # Full text for LLM context (no truncation)
            context_parts.append(f"[Source {i}]: {result['text']}")
            
            # For user display: show full chunk (no truncation)
            # Since chunks are now 1000 chars with sentence boundaries,
            # showing the full chunk gives complete context
            text = result['text']
            chunk_info = f"(Chunk {result['metadata'].get('chunk_index', 0)+1}/{result['metadata'].get('total_chunks', 1)})"
            
            sources.append({
                "source_number": i,  # Return as int, not str
                "text": text,  # Show full chunk text, no truncation
                "document": result['metadata'].get('filename', 'Unknown') + " " + chunk_info,
                "document_id": result['metadata'].get('document_id', 'Unknown')
            })
        
        context = "\n\n".join(context_parts)
        print(f"      • Total context: {len(context)} characters")
        print(f"      ✓ Context assembled")
        
        # Step 3: Build prompt
        print(f"    → Sub-step 2.3: Building Q&A prompt...")
        prompt = self._build_qa_prompt(question, context)
        print(f"      • Prompt length: {len(prompt)} characters")
        print(f"      ✓ Prompt ready")
        
        # Step 4: Get LLM response
        print(f"    → Sub-step 2.4: Calling LLM for answer...")
        try:
            answer = self.llm_service.generate_response(prompt)
            print(f"      • Answer length: {len(answer)} characters")
            print(f"      ✓ LLM response received")
            
            return {
                "answer": answer.strip(),
                "sources": sources
            }
        except Exception as e:
            print(f"      LLM call failed: {str(e)}")
            raise ValueError(f"Failed to generate answer: {str(e)}")
    
    def _build_qa_prompt(self, question: str, context: str) -> str:
        """
        Build prompt for Q&A.
        
        Args:
            question: User's question
            context: Retrieved context from documents
            
        Returns:
            Complete prompt string
        """
        system_instructions = """You are a helpful assistant that answers questions based ONLY on the provided context.

Rules:
1. Answer the question using ONLY information from the context provided
2. If the context doesn't contain enough information, say "I don't have enough information to answer that question."
3. Be concise and direct in your answer
4. Cite source numbers when referencing specific information (e.g., "According to Source 1...")
5. Do not make assumptions or add information not in the context
6. If multiple sources provide the same information, mention all relevant sources"""

        user_prompt = f"""Context from documents:

{context}

Question: {question}

Answer:"""

        return f"{system_instructions}\n\n{user_prompt}"


# Singleton instance
_qa_agent = None

def get_qa_agent() -> QAAgent:
    """Get or create singleton QAAgent instance."""
    global _qa_agent
    if _qa_agent is None:
        _qa_agent = QAAgent()
    return _qa_agent
