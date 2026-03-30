"""
Caching layer for improved performance
Implements LRU cache for retrieval results
"""

from functools import lru_cache
from typing import List, Dict, Optional
import hashlib
import json

class RetrievalCache:
    """Simple in-memory cache for retrieval results"""
    
    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, List[Dict]] = {}
        self.max_size = max_size
        self.access_count: Dict[str, int] = {}
    
    def _generate_key(self, query: str, collection: str, jurisdiction: str, top_k: int) -> str:
        """Generate cache key from query parameters"""
        key_data = f"{query}:{collection}:{jurisdiction}:{top_k}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, query: str, collection: str, jurisdiction: str, top_k: int) -> Optional[List[Dict]]:
        """Get cached results if available"""
        key = self._generate_key(query, collection, jurisdiction, top_k)
        
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        
        return None
    
    def set(self, query: str, collection: str, jurisdiction: str, top_k: int, results: List[Dict]):
        """Cache retrieval results"""
        key = self._generate_key(query, collection, jurisdiction, top_k)
        
        # Evict least recently used if cache is full
        if len(self.cache) >= self.max_size:
            lru_key = min(self.access_count, key=self.access_count.get)
            del self.cache[lru_key]
            del self.access_count[lru_key]
        
        self.cache[key] = results
        self.access_count[key] = 1
    
    def clear(self):
        """Clear all cached results"""
        self.cache.clear()
        self.access_count.clear()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "total_accesses": sum(self.access_count.values()),
            "unique_queries": len(self.cache)
        }

# Global cache instance
retrieval_cache = RetrievalCache(max_size=100)
