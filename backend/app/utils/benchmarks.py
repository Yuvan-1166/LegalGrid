"""
Retrieval quality benchmarks
Measures Precision@K and NDCG@K
"""

from typing import List, Dict
import numpy as np
from sklearn.metrics import ndcg_score

class RetrievalBenchmark:
    """Benchmark retrieval quality"""
    
    def __init__(self, test_queries: List[Dict]):
        """
        Initialize benchmark
        
        Args:
            test_queries: List of test queries with format:
                {
                    "query": "search query",
                    "collection": "statutes",
                    "relevant_docs": ["doc_id1", "doc_id2"],
                    "relevance_scores": {"doc_id1": 5, "doc_id2": 3}
                }
        """
        self.test_queries = test_queries
    
    def precision_at_k(self, retriever, k: int = 5) -> float:
        """
        Calculate Precision@K
        
        Precision@K = (# relevant docs in top-K) / K
        
        Args:
            retriever: Retriever instance
            k: Number of top results to consider
            
        Returns:
            Average precision across all queries
        """
        precisions = []
        
        for query_item in self.test_queries:
            query = query_item["query"]
            collection = query_item.get("collection", "statutes")
            relevant_docs = set(query_item["relevant_docs"])
            
            # Retrieve documents
            results = retriever.retrieve(
                query=query,
                collection=collection,
                top_k=k
            )
            
            # Get retrieved doc IDs
            retrieved_ids = {doc.get("doc_id", doc.get("id")) for doc in results}
            
            # Calculate precision
            relevant_retrieved = relevant_docs & retrieved_ids
            precision = len(relevant_retrieved) / k if k > 0 else 0
            
            precisions.append(precision)
        
        return np.mean(precisions) if precisions else 0.0
    
    def ndcg_at_k(self, retriever, k: int = 5) -> float:
        """
        Calculate NDCG@K (Normalized Discounted Cumulative Gain)
        
        NDCG accounts for ranking order - perfect ranking = 1.0
        
        Args:
            retriever: Retriever instance
            k: Number of top results to consider
            
        Returns:
            Average NDCG across all queries
        """
        ndcg_scores = []
        
        for query_item in self.test_queries:
            query = query_item["query"]
            collection = query_item.get("collection", "statutes")
            relevance_scores = query_item.get("relevance_scores", {})
            
            # Retrieve documents
            results = retriever.retrieve(
                query=query,
                collection=collection,
                top_k=k
            )
            
            # Build relevance arrays
            y_true = []
            y_score = []
            
            for doc in results:
                doc_id = doc.get("doc_id", doc.get("id"))
                y_true.append(relevance_scores.get(doc_id, 0))
                y_score.append(doc.get("fusion_score", doc.get("score", 0)))
            
            # Pad to k if needed
            while len(y_true) < k:
                y_true.append(0)
                y_score.append(0)
            
            # Calculate NDCG
            try:
                ndcg = ndcg_score([y_true], [y_score], k=k)
                ndcg_scores.append(ndcg)
            except:
                # If all zeros, skip
                pass
        
        return np.mean(ndcg_scores) if ndcg_scores else 0.0
    
    def run_full_benchmark(self, retriever) -> Dict:
        """Run complete benchmark suite"""
        print("Running retrieval benchmarks...")
        
        precision_5 = self.precision_at_k(retriever, k=5)
        ndcg_5 = self.ndcg_at_k(retriever, k=5)
        
        results = {
            "precision_at_5": round(precision_5, 3),
            "ndcg_at_5": round(ndcg_5, 3),
            "total_queries": len(self.test_queries),
            "target_precision": 0.80,
            "target_ndcg": 0.75,
            "precision_met": precision_5 >= 0.80,
            "ndcg_met": ndcg_5 >= 0.75
        }
        
        return results

# Sample test queries for benchmarking
SAMPLE_TEST_QUERIES = [
    {
        "query": "murder and homicide laws in India",
        "collection": "statutes",
        "relevant_docs": ["IPC_302", "IPC_304", "IPC_299", "IPC_300"],
        "relevance_scores": {"IPC_302": 5, "IPC_304": 4, "IPC_299": 4, "IPC_300": 5}
    },
    {
        "query": "fundamental rights and equality",
        "collection": "statutes",
        "relevant_docs": ["CONST_ART_14", "CONST_ART_15", "CONST_ART_19", "CONST_ART_21"],
        "relevance_scores": {"CONST_ART_14": 5, "CONST_ART_15": 5, "CONST_ART_19": 4, "CONST_ART_21": 4}
    },
    {
        "query": "contract enforceability and consideration",
        "collection": "statutes",
        "relevant_docs": ["ICA_10", "ICA_23", "ICA_2"],
        "relevance_scores": {"ICA_10": 5, "ICA_23": 5, "ICA_2": 3}
    },
    {
        "query": "sexual harassment at workplace",
        "collection": "cases",
        "relevant_docs": ["CASE_VISHAKA"],
        "relevance_scores": {"CASE_VISHAKA": 5}
    },
    {
        "query": "right to privacy and data protection",
        "collection": "cases",
        "relevant_docs": ["CASE_PUTTASWAMY"],
        "relevance_scores": {"CASE_PUTTASWAMY": 5}
    }
]
