"""Cross-Encoder Reranker for improved retrieval accuracy"""
from sentence_transformers import CrossEncoder
from typing import List, Dict
import numpy as np

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """Initialize cross-encoder reranker"""
        self.model = CrossEncoder(model_name)
        self.model_name = model_name
    
    def rerank(self, query: str, documents: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        Rerank documents using cross-encoder
        
        Args:
            query: Search query
            documents: List of retrieved documents
            top_k: Number of top results to return
            
        Returns:
            Reranked documents with cross-encoder scores
        """
        if not documents:
            return []
        
        # Prepare query-document pairs
        pairs = [[query, doc.get("content", "")] for doc in documents]
        
        # Get cross-encoder scores
        scores = self.model.predict(pairs)
        
        # Add scores to documents
        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)
            doc["original_score"] = doc.get("fusion_score", doc.get("score", 0))
        
        # Sort by rerank score
        reranked = sorted(documents, key=lambda x: x["rerank_score"], reverse=True)
        
        return reranked[:top_k]
    
    def explain_reranking(self, doc: Dict) -> str:
        """Explain reranking decision"""
        original = doc.get("original_score", 0)
        rerank = doc.get("rerank_score", 0)
        change = rerank - original
        
        if change > 0.1:
            return f"Promoted by reranker (score: {rerank:.3f}, was: {original:.3f})"
        elif change < -0.1:
            return f"Demoted by reranker (score: {rerank:.3f}, was: {original:.3f})"
        else:
            return f"Position maintained (score: {rerank:.3f})"

# Global reranker instance
reranker = CrossEncoderReranker()
