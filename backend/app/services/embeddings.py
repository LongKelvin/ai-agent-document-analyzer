"""
Embeddings and Retrieval Service - Educational RAG implementation.

This module demonstrates:
- Document embedding generation
- In-memory vector storage
- Semantic similarity search
- Context retrieval for prompt augmentation

This is educational code, not production-ready. No external vector DB needed.
"""

from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import settings


# Hardcoded guidelines for document analysis (educational purposes)
# In production, these would come from a database or configuration
ANALYSIS_GUIDELINES = [
    """
    A complete document should include:
    - Clear title or heading
    - Introduction or overview section
    - Main content with logical structure
    - Conclusion or summary
    - References or citations (if applicable)
    """,
    """
    When assessing document completeness:
    - Check for logical flow between sections
    - Verify that claims are supported by evidence
    - Look for missing context or unexplained terms
    - Identify gaps in reasoning or argumentation
    """,
    """
    Evidence-based analysis principles:
    - Only cite information present in the document
    - Use direct quotes when possible
    - Do not make assumptions about missing information
    - Mark uncertain assessments with lower confidence scores
    """,
    """
    Common completeness issues to check:
    - Missing introduction or background
    - Undefined abbreviations or acronyms
    - Unsupported claims without evidence
    - Abrupt ending without conclusion
    - Missing references for cited facts
    """
]


class EmbeddingService:
    """
    Service for generating embeddings and performing semantic search.
    
    Uses sentence-transformers for lightweight, local embeddings.
    No API calls required after model download.
    """
    
    def __init__(self):
        """
        Initialize embedding model and encode guidelines.
        
        The model is loaded once and reused for efficiency.
        Guidelines are embedded at initialization for quick retrieval.
        """
        # Load sentence transformer model
        # This model is small (~80MB) and runs locally
        self.model = SentenceTransformer(settings.embedding_model_name)
        
        # Precompute guideline embeddings
        # This is a one-time cost at startup
        self.guidelines = ANALYSIS_GUIDELINES
        self.guideline_embeddings = self._embed_texts(self.guidelines)
    
    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            NumPy array of shape (len(texts), embedding_dim)
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Cosine similarity measures the angle between vectors.
        Range: -1 (opposite) to 1 (identical)
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score between -1 and 1
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def retrieve_relevant_guidelines(self, query: str, top_k: int = 2) -> List[str]:
        """
        Retrieve the most relevant guidelines for a query.
        
        This is the "retrieval" part of RAG (Retrieval-Augmented Generation).
        
        Process:
        1. Embed the query
        2. Calculate similarity with all guideline embeddings
        3. Return top-k most similar guidelines
        
        Args:
            query: The search query (e.g., document text or analysis goal)
            top_k: Number of guidelines to retrieve
            
        Returns:
            List of most relevant guideline texts
        """
        # Embed the query
        query_embedding = self._embed_texts([query])[0]
        
        # Calculate similarities with all guidelines
        similarities = []
        for i, guideline_embedding in enumerate(self.guideline_embeddings):
            similarity = self._cosine_similarity(query_embedding, guideline_embedding)
            similarities.append((i, similarity))
        
        # Sort by similarity (descending) and get top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in similarities[:top_k]]
        
        # Return corresponding guideline texts
        return [self.guidelines[idx] for idx in top_indices]
    
    def embed_document(self, document: str) -> np.ndarray:
        """
        Generate embedding for a document.
        
        Useful for:
        - Document similarity search
        - Clustering
        - Classification
        
        Args:
            document: Text to embed
            
        Returns:
            Embedding vector
        """
        return self._embed_texts([document])[0]


# Singleton instance
_embedding_service_instance = None


def get_embedding_service() -> EmbeddingService:
    """
    Get singleton instance of EmbeddingService.
    
    Model loading is expensive, so we only do it once.
    """
    global _embedding_service_instance
    if _embedding_service_instance is None:
        _embedding_service_instance = EmbeddingService()
    return _embedding_service_instance
