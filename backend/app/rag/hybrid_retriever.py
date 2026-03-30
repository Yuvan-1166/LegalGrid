"""Enhanced hybrid retriever combining semantic search and BM25"""

from typing import List, Dict, Optional
from app.rag.retriever import retriever
from app.rag.bm25_search import bm25_searcher
from app.core.cache import retrieval_cache
import numpy as np

class HybridRetriever:
    def __init__(self, semantic_weight: float = 0.6, bm25_weight: float = 0.4):
        """
        Initialize hybrid retriever
        
        Args:
            semantic_weight: Weight for semantic search (0-1)
            bm25_weight: Weight for BM25 search (0-1)
        """
        self.semantic_weight = semantic_weight
        self.bm25_weight = bm25_weight
        self.semantic_retriever = retriever
        self.bm25_retriever = bm25_searcher
        self.cache = retrieval_cache
    
    def reciprocal_rank_fusion(
        self,
        semantic_results: List[Dict],
        bm25_results: List[Dict],
        k: int = 60
    ) -> List[Dict]:
        """
        Combine results using Reciprocal Rank Fusion (RRF)
        
        RRF formula: score = 1 / (k + rank)
        
        Args:
            semantic_results: Results from semantic search
            bm25_results: Results from BM25 search
            k: Constant for RRF (default: 60)
            
        Returns:
            Fused and ranked results
        """
        # Create score dictionaries
        doc_scores = {}
        doc_data = {}
        
        # Add semantic scores
        for rank, doc in enumerate(semantic_results, 1):
            doc_id = doc["doc_id"]
            rrf_score = 1.0 / (k + rank)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + (rrf_score * self.semantic_weight)
            doc_data[doc_id] = doc
            doc_data[doc_id]["semantic_rank"] = rank
            doc_data[doc_id]["semantic_score"] = doc.get("score", 0)
        
        # Add BM25 scores
        for rank, doc in enumerate(bm25_results, 1):
            doc_id = doc["doc_id"]
            rrf_score = 1.0 / (k + rank)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + (rrf_score * self.bm25_weight)
            
            if doc_id not in doc_data:
                doc_data[doc_id] = doc
            
            doc_data[doc_id]["bm25_rank"] = rank
            doc_data[doc_id]["bm25_score"] = doc.get("score", 0)
        
        # Sort by fused score
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Format results
        results = []
        for doc_id, fusion_score in sorted_docs:
            doc = doc_data[doc_id]
            doc["fusion_score"] = fusion_score
            doc["retrieval_method"] = self._get_retrieval_method(doc)
            results.append(doc)
        
        return results
    
    def _get_retrieval_method(self, doc: Dict) -> str:
        """Determine which method retrieved the document"""
        has_semantic = "semantic_rank" in doc
        has_bm25 = "bm25_rank" in doc
        
        if has_semantic and has_bm25:
            return "hybrid"
        elif has_semantic:
            return "semantic"
        elif has_bm25:
            return "bm25"
        return "unknown"
    
    def retrieve(
        self,
        query: str,
        collection: str,
        jurisdiction: str = "All-India",
        top_k: int = 5,
        use_hybrid: bool = True,
        use_cache: bool = True
    ) -> List[Dict]:
        """
        Retrieve documents using hybrid search with caching
        
        Args:
            query: Search query
            collection: Collection to search in
            jurisdiction: Jurisdiction filter
            top_k: Number of results to return
            use_hybrid: If False, use only semantic search
            use_cache: If True, use cached results when available
            
        Returns:
            List of retrieved documents with scores
        """
        # Check cache first
        if use_cache:
            cached_results = self.cache.get(query, collection, jurisdiction, top_k)
            if cached_results is not None:
                return cached_results
        
        if not use_hybrid:
            # Semantic only
            results = self.semantic_retriever.retrieve(
                query=query,
                collection=collection,
                jurisdiction=jurisdiction,
                top_k=top_k
            )
        else:
            # Get results from both retrievers
            semantic_results = self.semantic_retriever.retrieve(
                query=query,
                collection=collection,
                jurisdiction=jurisdiction,
                top_k=top_k * 2  # Get more for fusion
            )
            
            bm25_results = self.bm25_retriever.search(
                query=query,
                collection=collection,
                jurisdiction=jurisdiction if jurisdiction != "All-India" else None,
                top_k=top_k * 2
            )
            
            # Fuse results
            fused_results = self.reciprocal_rank_fusion(
                semantic_results,
                bm25_results
            )
            
            # Return top-k
            results = fused_results[:top_k]
        
        # Cache results
        if use_cache:
            self.cache.set(query, collection, jurisdiction, top_k, results)
        
        return results
    
    def explain_retrieval(self, doc: Dict) -> str:
        """Generate explanation for why document was retrieved"""
        method = doc.get("retrieval_method", "unknown")
        
        if method == "hybrid":
            return (
                f"Retrieved via hybrid search (semantic rank: {doc.get('semantic_rank', 'N/A')}, "
                f"BM25 rank: {doc.get('bm25_rank', 'N/A')}). "
                f"Fusion score: {doc.get('fusion_score', 0):.3f}"
            )
        elif method == "semantic":
            return (
                f"Retrieved via semantic similarity. "
                f"Score: {doc.get('semantic_score', 0):.3f}"
            )
        elif method == "bm25":
            return (
                f"Retrieved via keyword matching (BM25). "
                f"Score: {doc.get('bm25_score', 0):.3f}"
            )
        return "Retrieval method unknown"

# Global hybrid retriever instance
hybrid_retriever = HybridRetriever()
