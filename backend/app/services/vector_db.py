"""
Vector Database Service using ChromaDB for persistent storage.

This replaces the in-memory vector store with a real database.
"""

import os
import warnings
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from app.config import settings

# Suppress ChromaDB telemetry warnings
warnings.filterwarnings('ignore', category=UserWarning, module='chromadb')


class VectorDBService:
    """
    Persistent vector database service using ChromaDB.
    
    Supports:
    - Document upload and storage
    - Semantic search across documents
    - Document management (list, delete)
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB with persistent storage.
        
        Args:
            persist_directory: Directory to store the database
        """
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Disable ChromaDB telemetry to avoid SSL errors
        os.environ['ANONYMIZED_TELEMETRY'] = 'False'
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
                is_persistent=True
            )
        )
        
        # Get or create collection for documents
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"description": "User uploaded documents"}
        )
        
        # Initialize embedding model (same as before)
        self.embedding_model = SentenceTransformer(settings.embedding_model_name)
        
        print(f"[VectorDB] Initialized with {self.collection.count()} documents")
    
    def add_document(self, document_id: str, text: str, metadata: Dict[str, Any]) -> None:
        """
        Add a document to the vector database.
        
        Args:
            document_id: Unique identifier for the document
            text: Full text content of the document
            metadata: Additional metadata (filename, upload_date, etc.)
        """
        print(f"      → Chunking document...")
        # Split document into chunks for better retrieval
        chunks = self._chunk_text(text)
        print(f"        • Created {len(chunks)} chunks")
        
        print(f"      → Generating embeddings with sentence-transformers...")
        # Generate embeddings for each chunk
        embeddings = self.embedding_model.encode(chunks).tolist()
        print(f"        • Generated {len(embeddings)} embeddings")
        
        # Create unique IDs for each chunk
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Add metadata to each chunk
        chunk_metadata = [
            {
                **metadata,
                "document_id": document_id,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]
        
        print(f"      → Storing in ChromaDB...")
        # Add to ChromaDB
        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=chunk_metadata
        )
        
        print(f"        • Total documents in DB: {self.collection.count()}")
        print(f"      ✓ Document stored successfully")
    
    def search(self, query: str, top_k: int = 5, document_id: str = None) -> List[Dict[str, Any]]:
        """
        Semantic search across documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            document_id: Optional filter to search within specific document
            
        Returns:
            List of search results with text, metadata, and similarity scores
        """
        print(f"        • Encoding query with embedding model...")
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Build filter if document_id provided
        where_filter = {"document_id": document_id} if document_id else None
        
        print(f"        • Searching ChromaDB (top_k={top_k})...")
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None,
                    "similarity_score": 1 - results['distances'][0][i] if 'distances' in results else None
                })
        
        print(f"        • Found {len(formatted_results)} results")
        if formatted_results and 'distances' in results:
            avg_distance = sum(results['distances'][0]) / len(results['distances'][0])
            print(f"        • Average similarity: {1 - avg_distance:.2%}")
        return formatted_results
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all unique documents in the database.
        
        Returns:
            List of documents with metadata
        """
        # Get all items
        all_items = self.collection.get()
        
        # Extract unique documents
        documents = {}
        if all_items['metadatas']:
            for metadata in all_items['metadatas']:
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
        
        Args:
            document_id: ID of document to delete
            
        Returns:
            True if deleted, False if not found
        """
        # Get all chunk IDs for this document
        results = self.collection.get(
            where={"document_id": document_id}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            print(f"[VectorDB] Deleted document {document_id} ({len(results['ids'])} chunks)")
            return True
        
        return False
    
    def get_document_count(self) -> int:
        """Get total number of unique documents."""
        return len(self.list_documents())
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks for better retrieval.
        
        Increased from 500 to 1000 chars to preserve more context.
        Overlap ensures important information isn't lost at boundaries.
        
        Args:
            text: Text to chunk
            chunk_size: Target size of each chunk in characters (default: 1000)
            overlap: Overlap between chunks (default: 100)
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary for better context
            if end < len(text):
                # Look for sentence ending (prefer period, then other punctuation)
                for char in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
                    last_sentence = text[start:end].rfind(char)
                    if last_sentence > chunk_size * 0.5:  # At least 50% of chunk_size
                        end = start + last_sentence + len(char)
                        break
            
            chunk = text[start:end].strip()
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)
            start = end - overlap
        
        return chunks
        
        return chunks


# Singleton instance
_vector_db_service = None

def get_vector_db_service() -> VectorDBService:
    """Get or create singleton VectorDBService instance."""
    global _vector_db_service
    if _vector_db_service is None:
        _vector_db_service = VectorDBService()
    return _vector_db_service
