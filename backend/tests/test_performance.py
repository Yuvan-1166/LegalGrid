"""Performance Tests for LegalGrid"""
import pytest, time, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.hybrid_retriever import hybrid_retriever

class TestPerformance:
    def test_retrieval_response_time(self):
        """Test retrieval completes within 2 seconds"""
        start = time.time()
        result = hybrid_retriever.retrieve(query="contract law", collection="statutes", top_k=5)
        elapsed = time.time() - start
        assert elapsed < 2.0, f"Retrieval took {elapsed:.2f}s (target: <2s)"
    
    def test_cache_effectiveness(self):
        """Test cache improves performance"""
        query = "employment termination"
        
        # First call (no cache)
        start1 = time.time()
        hybrid_retriever.retrieve(query=query, collection="statutes", top_k=5, use_cache=True)
        time1 = time.time() - start1
        
        # Second call (cached)
        start2 = time.time()
        hybrid_retriever.retrieve(query=query, collection="statutes", top_k=5, use_cache=True)
        time2 = time.time() - start2
        
        assert time2 < time1 * 0.5, "Cache should improve performance by 50%+"
    
    def test_batch_retrieval(self):
        """Test batch retrieval performance"""
        queries = ["contract", "employment", "property", "tax", "compliance"]
        start = time.time()
        for q in queries:
            hybrid_retriever.retrieve(query=q, collection="statutes", top_k=5)
        elapsed = time.time() - start
        assert elapsed < 10.0, f"Batch retrieval took {elapsed:.2f}s (target: <10s)"
    
    def test_large_top_k(self):
        """Test retrieval with large top_k"""
        start = time.time()
        result = hybrid_retriever.retrieve(query="legal", collection="statutes", top_k=100)
        elapsed = time.time() - start
        assert elapsed < 5.0, f"Large top_k took {elapsed:.2f}s (target: <5s)"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
