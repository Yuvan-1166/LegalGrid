"""BM25 search implementation using Whoosh for keyword-based retrieval"""

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import scoring
import os
from typing import List, Dict, Optional

class BM25Searcher:
    def __init__(self, index_dir: str = "whoosh_index"):
        self.index_dir = index_dir
        # Simplified schema - store everything in STORED fields
        self.schema = Schema(
            doc_id=ID(stored=True, unique=True),
            title=TEXT(stored=True),
            content=TEXT(stored=True),
            collection=KEYWORD(stored=True),
            jurisdiction=KEYWORD(stored=True),
            # Store all other metadata as a single field
            metadata=STORED()
        )
        self._initialize_index()
    
    def _initialize_index(self):
        """Create or open Whoosh index"""
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
        
        if not exists_in(self.index_dir):
            self.ix = create_in(self.index_dir, self.schema)
        else:
            self.ix = open_dir(self.index_dir)
    
    def add_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        collection: str,
        jurisdiction: str = "All-India",
        **metadata
    ):
        """Add document to BM25 index"""
        writer = self.ix.writer()
        writer.add_document(
            doc_id=doc_id,
            title=title,
            content=content,
            collection=collection,
            jurisdiction=jurisdiction,
            metadata=metadata  # Store all extra metadata here
        )
        writer.commit()
    
    def search(
        self,
        query: str,
        collection: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Search using BM25 algorithm
        
        Args:
            query: Search query
            collection: Filter by collection
            jurisdiction: Filter by jurisdiction
            top_k: Number of results to return
            
        Returns:
            List of matching documents with scores
        """
        with self.ix.searcher(weighting=scoring.BM25F()) as searcher:
            # Parse query across multiple fields
            parser = MultifieldParser(
                ["title", "content"],
                schema=self.ix.schema
            )
            
            # Build query with filters
            query_obj = parser.parse(query)
            
            # Apply filters
            filter_terms = []
            if collection:
                filter_terms.append(f"collection:{collection}")
            if jurisdiction and jurisdiction != "All":
                filter_terms.append(f"jurisdiction:{jurisdiction}")
            
            if filter_terms:
                filter_query = " AND ".join(filter_terms)
                filter_obj = parser.parse(filter_query)
                results = searcher.search(query_obj, filter=filter_obj, limit=top_k)
            else:
                results = searcher.search(query_obj, limit=top_k)
            
            # Format results
            formatted_results = []
            for hit in results:
                result = {
                    "doc_id": hit["doc_id"],
                    "title": hit["title"],
                    "content": hit["content"],
                    "score": hit.score,
                    "collection": hit["collection"],
                    "jurisdiction": hit["jurisdiction"],
                    "rank": hit.rank + 1,
                    "metadata": hit.get("metadata", {})
                }
                formatted_results.append(result)
            
            return formatted_results
    
    def clear_index(self):
        """Clear all documents from index"""
        writer = self.ix.writer()
        writer.commit(mergetype=self.ix.writer.CLEAR)

# Global BM25 searcher instance
bm25_searcher = BM25Searcher()
