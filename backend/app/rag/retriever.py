from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import hashlib
from app.core.config import settings

class HybridRetriever:
    def __init__(self, qdrant_url: str = None):
        self.qdrant_url = qdrant_url or settings.QDRANT_URL
        self.client = QdrantClient(url=self.qdrant_url)
        self.encoder = SentenceTransformer("all-mpnet-base-v2")
        self.cache: Dict[str, list] = {}
        self.embedding_dim = 768  # all-mpnet-base-v2 dimension
    
    def initialize_collections(self):
        """Create Qdrant collections for different document types"""
        collections = {
            "statutes": "Indian statutes (IPC, CPC, Constitution)",
            "cases": "Supreme Court & High Court judgments",
            "regulations": "MCA, RBI, SEBI notifications",
            "contracts": "Sample contracts (user uploads)",
        }
        
        for collection_name, description in collections.items():
            try:
                self.client.get_collection(collection_name)
                print(f"✓ Collection '{collection_name}' already exists")
            except Exception:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,
                        distance=Distance.COSINE
                    )
                )
                print(f"✓ Created collection: {collection_name}")
    
    def add_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        collection: str,
        jurisdiction: str = "All-India",
        metadata: Optional[dict] = None
    ):
        """Add document to vector database"""
        embedding = self.encoder.encode(content, convert_to_tensor=False)
        
        payload = {
            "title": title,
            "content": content[:2000],  # Store first 2k chars
            "collection": collection,
            "jurisdiction": jurisdiction,
            "doc_id": doc_id,
            **(metadata or {})
        }
        
        self.client.upsert(
            collection_name=collection,
            points=[
                PointStruct(
                    id=abs(hash(doc_id)) % (10**9),
                    vector=embedding.tolist(),
                    payload=payload
                )
            ]
        )
    
    def retrieve(
        self,
        query: str,
        collection: str,
        jurisdiction: str = "All-India",
        top_k: int = 5
    ) -> List[Dict]:
        """Retrieve relevant documents using semantic search"""
        # Check cache
        cache_key = self._hash_query(query, collection, jurisdiction)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Encode query
        query_embedding = self.encoder.encode(query, convert_to_tensor=False).tolist()
        
        # Search with jurisdiction filter
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="jurisdiction",
                    match=MatchValue(value=jurisdiction)
                )
            ]
        ) if jurisdiction != "All" else None
        
        results = self.client.search(
            collection_name=collection,
            query_vector=query_embedding,
            query_filter=search_filter,
            limit=top_k,
            with_payload=True
        )
        
        # Format results
        formatted_results = []
        for hit in results:
            formatted_results.append({
                "doc_id": hit.payload.get("doc_id"),
                "title": hit.payload.get("title"),
                "content": hit.payload.get("content"),
                "score": hit.score,
                "metadata": {k: v for k, v in hit.payload.items() 
                           if k not in ["doc_id", "title", "content"]}
            })
        
        # Cache results
        self.cache[cache_key] = formatted_results
        return formatted_results
    
    def _hash_query(self, query: str, collection: str, jurisdiction: str) -> str:
        """Create cache key"""
        key = f"{query}:{collection}:{jurisdiction}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def clear_cache(self):
        """Clear retrieval cache"""
        self.cache.clear()

# Global retriever instance
retriever = HybridRetriever()
