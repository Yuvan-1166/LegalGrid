"""Edge Case Tests for LegalGrid"""
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.hybrid_retriever import hybrid_retriever
from app.agents.contract_agent import contract_agent

class TestEdgeCases:
    def test_empty_query(self):
        """Test handling of empty query"""
        result = hybrid_retriever.retrieve(query="", collection="statutes", top_k=5)
        assert isinstance(result, list)
    
    def test_very_long_query(self):
        """Test handling of very long query"""
        long_query = "contract " * 1000
        result = hybrid_retriever.retrieve(query=long_query, collection="statutes", top_k=5)
        assert isinstance(result, list)
    
    def test_special_characters(self):
        """Test handling of special characters"""
        result = hybrid_retriever.retrieve(query="@#$%^&*()", collection="statutes", top_k=5)
        assert isinstance(result, list)
    
    def test_unicode_query(self):
        """Test handling of unicode characters"""
        result = hybrid_retriever.retrieve(query="अनुबंध समझौता", collection="statutes", top_k=5)
        assert isinstance(result, list)
    
    def test_malformed_contract(self):
        """Test contract analysis with malformed input"""
        result = contract_agent.analyze(contract_text="", jurisdiction="All-India")
        assert result is not None
    
    def test_invalid_jurisdiction(self):
        """Test invalid jurisdiction handling"""
        result = hybrid_retriever.retrieve(query="test", collection="statutes", jurisdiction="InvalidPlace")
        assert isinstance(result, list)
    
    def test_zero_top_k(self):
        """Test retrieval with top_k=0"""
        result = hybrid_retriever.retrieve(query="contract", collection="statutes", top_k=0)
        assert len(result) == 0
    
    def test_negative_top_k(self):
        """Test retrieval with negative top_k"""
        result = hybrid_retriever.retrieve(query="contract", collection="statutes", top_k=-5)
        assert isinstance(result, list)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
