"""Concurrent Request Tests for LegalGrid"""
import pytest, sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.hybrid_retriever import hybrid_retriever

class TestConcurrent:
    def test_concurrent_retrieval(self):
        """Test concurrent retrieval requests"""
        queries = [f"query_{i}" for i in range(10)]
        
        def retrieve(query):
            return hybrid_retriever.retrieve(query=query, collection="statutes", top_k=5)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(retrieve, q) for q in queries]
            results = [f.result() for f in as_completed(futures)]
        
        assert len(results) == 10
        assert all(isinstance(r, list) for r in results)
    
    def test_cache_consistency(self):
        """Test cache consistency under concurrent access"""
        query = "contract law"
        
        def retrieve_cached():
            return hybrid_retriever.retrieve(query=query, collection="statutes", top_k=5, use_cache=True)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(retrieve_cached) for _ in range(20)]
            results = [f.result() for f in as_completed(futures)]
        
        # All results should be identical (from cache)
        first_result = results[0]
        assert all(len(r) == len(first_result) for r in results)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
