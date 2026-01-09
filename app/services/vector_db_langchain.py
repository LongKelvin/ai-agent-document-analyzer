"""
Vector Database Service using LangChain + ChromaDB - Educational Version

WHAT IS THIS FILE?
This replaces the custom ChromaDB implementation (vector_db.py) with LangChain's Chroma wrapper.

WHY USE LANGCHAIN'S VECTOR STORE?
- Standardized interface: Works the same way for any vector DB (Pinecone, Weaviate, FAISS, etc.)
- Built-in document processing: Automatic chunking, metadata handling
- Easy integration: Works seamlessly with LangChain retrievers and chains
- Less boilerplate: No need to manually manage embeddings, IDs, metadata

WHAT CHANGED?
Before: We manually called ChromaDB's add(), query(), delete() methods
After: LangChain's Chroma class handles all the complexity
"""

import os
import warnings
from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import settings

# Suppress ChromaDB telemetry warnings
warnings.filterwarnings('ignore', category=UserWarning, module='chromadb')


class LangChainVectorDBService:
    """
    LangChain-based vector database service using ChromaDB.
    
    KEY LANGCHAIN CONCEPTS:
    1. Document: LangChain's standard format for text + metadata
    2. Embeddings: Interface for any embedding model (HuggingFace, OpenAI, etc.)
    3. VectorStore: Interface for any vector database
    4. TextSplitter: Smart chunking with overlap and separators
    
    BENEFITS:
    - Switch vector DBs easily (just change Chroma -> Pinecone)
    - Switch embedding models easily (just change HuggingFaceEmbeddings -> OpenAIEmbeddings)
    - Built-in RAG methods: similarity_search(), as_retriever()
    - Better document management with metadata filtering
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize LangChain vector store.
        
        BEHIND THE SCENES:
        1. HuggingFaceEmbeddings wraps sentence-transformers models
        2. Chroma creates/connects to ChromaDB with persistence
        3. TextSplitter prepares to chunk documents intelligently
        
        WHY RecursiveCharacterTextSplitter?
        - Tries to split at sentence boundaries first (. ! ?)
        - Falls back to paragraphs, then words if needed
        - Maintains context with overlap between chunks
        """
        os.makedirs(persist_directory, exist_ok=True)
        
        # Disable telemetry
        os.environ['ANONYMIZED_TELEMETRY'] = 'False'
        
        # Initialize embedding model (same as before, but wrapped in LangChain)
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name,
            model_kwargs={'device': 'cpu'},  # Use CPU for compatibility
            encode_kwargs={'normalize_embeddings': True}  # Better similarity search
        )
        
        # Initialize LangChain's Chroma vector store
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embedding_model,
            persist_directory=persist_directory
        )
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Target chunk size in characters
            chunk_overlap=50,  # Overlap to maintain context
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # Priority order for splitting
        )
        
        doc_count = len(self.vector_store.get()['ids']) if self.vector_store else 0
        print(f"[LangChain VectorDB] Initialized with {doc_count} documents")
    
    def add_document(self, document_id: str, text: str, metadata: Dict[str, Any]) -> None:
        """
        Add a document to the vector store using LangChain.
        
        LANGCHAIN APPROACH:
        1. Create Document objects (text + metadata)
        2. Use TextSplitter to chunk intelligently
        3. VectorStore handles embedding and storage automatically
        
        WHAT'S DIFFERENT?
        Before: We manually chunked, embedded, and stored with IDs
        After: LangChain does all of this with .add_documents()
        
        IMPORTANT:
        LangChain generates its own chunk IDs internally.
        We store document_id in metadata to track which document each chunk belongs to.
        
        Args:
            document_id: Unique identifier for this document
            text: Full text content
            metadata: Additional info (filename, upload_date, etc.)
        """
        # Step 1: Create a LangChain Document
        # Document is just a container for text + metadata
        doc = Document(
            page_content=text,
            metadata={**metadata, "document_id": document_id}
        )
        
        # Step 2: Split into chunks using intelligent text splitter
        # This respects sentence boundaries and maintains context with overlap
        chunks = self.text_splitter.split_documents([doc])
        
        # Step 3: Add chunk metadata (which chunk this is)
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)
        
        # Step 4: Add to vector store
        # LangChain automatically:
        # - Generates embeddings using self.embedding_model
        # - Stores in ChromaDB with proper IDs
        # - Persists to disk
        self.vector_store.add_documents(chunks)
        
        print(f"[LangChain VectorDB] Added document {document_id} with {len(chunks)} chunks")
    
    def search(self, query: str, top_k: int = 5, document_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Semantic search using LangChain's similarity_search.
        
        LANGCHAIN MAGIC:
        - Automatically embeds your query
        - Performs similarity search in ChromaDB
        - Returns results sorted by relevance
        - Supports metadata filtering
        
        WHAT'S DIFFERENT?
        Before: We manually encoded query, called ChromaDB query(), formatted results
        After: One method call does everything
        
        Args:
            query: Search query
            top_k: Number of results
            document_id: Optional filter for specific document
            
        Returns:
            List of results with text, metadata, and scores
        """
        # Build metadata filter if document_id provided
        filter_dict = {"document_id": document_id} if document_id else None
        
        # Perform similarity search
        # LangChain handles: embedding query, searching, scoring
        if filter_dict:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=top_k,
                filter=filter_dict
            )
        else:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=top_k
            )
        
        # Format results to match the old interface
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "text": doc.page_content,
                "metadata": doc.metadata,
                "distance": score  # Lower score = more similar
            })
        
        return formatted_results
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all unique documents in the vector store.
        
        LANGCHAIN METHOD:
        - Use get() to retrieve all documents
        - Extract unique document_ids from metadata
        
        This is similar to the old implementation but uses LangChain's API.
        """
        # Get all documents from the collection
        all_data = self.vector_store.get()
        
        # Extract unique documents
        documents = {}
        if all_data['metadatas']:
            for metadata in all_data['metadatas']:
                doc_id = metadata.get('document_id')
                if doc_id and doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "filename": metadata.get('filename', 'Unknown'),
                        "upload_date": metadata.get('upload_date', 'Unknown'),
                        "file_size": metadata.get('file_size', 0)
                    }
        
        return list(documents.values())
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document and all its chunks.
        
        LANGCHAIN METHOD:
        1. Get all chunk IDs with this document_id in metadata
        2. Delete by IDs using vector_store.delete()
        
        NOTE: LangChain's delete() requires explicit IDs,
        so we still need to query first to get them.
        
        Args:
            document_id: ID of document to delete
            
        Returns:
            True if deleted, False if not found
        """
        # Get all chunks for this document
        all_data = self.vector_store.get(
            where={"document_id": document_id}
        )
        
        if all_data['ids']:
            # Delete all chunks
            self.vector_store.delete(ids=all_data['ids'])
            print(f"[LangChain VectorDB] Deleted document {document_id} ({len(all_data['ids'])} chunks)")
            return True
        
        return False
    
    def get_document_count(self) -> int:
        """Get total number of unique documents."""
        return len(self.list_documents())
    
    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Convert vector store to LangChain Retriever.
        
        THIS IS THE POWER OF LANGCHAIN:
        A Retriever is a standardized interface for fetching relevant documents.
        Once you have a retriever, you can plug it into any LangChain chain.
        
        Example usage:
        ```python
        retriever = vector_db.as_retriever(search_kwargs={"k": 5})
        
        # Use in a RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever
        )
        ```
        
        This is how we'll refactor the QA agent in the next step!
        
        Args:
            search_kwargs: Parameters for search (k, filter, etc.)
            
        Returns:
            LangChain Retriever object
        """
        if search_kwargs is None:
            search_kwargs = {"k": 5}
        
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)


# Singleton instance
_langchain_vector_db_service = None


def get_langchain_vector_db_service() -> LangChainVectorDBService:
    """
    Get singleton instance of LangChainVectorDBService.
    
    WHY SINGLETON?
    - ChromaDB connection is expensive to create
    - Embedding model loads once and stays in memory
    - Reuse across all requests for efficiency
    """
    global _langchain_vector_db_service
    if _langchain_vector_db_service is None:
        _langchain_vector_db_service = LangChainVectorDBService()
    return _langchain_vector_db_service
