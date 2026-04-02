#!/usr/bin/env python3
"""Ingest all documents from corpus.jsonl into Qdrant and BM25"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retriever import retriever
from app.rag.bm25_search import bm25_searcher

def load_corpus(corpus_path: str = "data/corpus.jsonl"):
    """Load all documents from corpus.jsonl"""
    documents = []
    corpus_file = Path(corpus_path)
    
    if not corpus_file.exists():
        print(f"❌ Error: {corpus_path} not found!")
        return documents
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                doc = json.loads(line)
                documents.append(doc)
            except json.JSONDecodeError as e:
                print(f"⚠️  Warning: Skipping line {line_num} - Invalid JSON: {e}")
    
    return documents

def ingest_documents(documents):
    """Ingest all documents into both Qdrant and BM25 index"""
    print("=" * 70)
    print("Corpus Data Ingestion")
    print("=" * 70)
    print(f"\nIngesting {len(documents)} documents...\n")
    
    success_count = 0
    error_count = 0
    
    for i, doc in enumerate(documents, 1):
        try:
            # Add to Qdrant (vector database)
            retriever.add_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc.get("jurisdiction", "All-India"),
                metadata=doc.get("metadata", {})
            )
            
            # Add to BM25 index
            bm25_searcher.add_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc.get("jurisdiction", "All-India"),
                **doc.get("metadata", {})
            )
            
            if i % 50 == 0:
                print(f"✓ Progress: {i}/{len(documents)} documents ingested...")
            
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error adding {doc.get('doc_id', 'unknown')}: {e}")
            error_count += 1
    
    print(f"\n{'=' * 70}")
    print(f"Ingestion Complete")
    print(f"{'=' * 70}")
    print(f"✓ Successfully added: {success_count} documents")
    if error_count > 0:
        print(f"✗ Errors: {error_count} documents")
    
    return success_count, error_count

def test_retrieval():
    """Test retrieval with sample queries"""
    print(f"\n{'=' * 70}")
    print("Testing Retrieval")
    print(f"{'=' * 70}\n")
    
    test_queries = [
        ("Indian Penal Code murder", "statutes"),
        ("Constitution fundamental rights", "statutes"),
        ("contract law", "statutes"),
    ]
    
    for query, collection in test_queries:
        print(f"\nQuery: '{query}' in {collection}")
        print("-" * 70)
        
        try:
            results = retriever.retrieve(
                query=query,
                collection=collection,
                top_k=3
            )
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['title']}")
                    print(f"   Score: {result.get('score', 0):.3f}")
            else:
                print("   No results found")
        except Exception as e:
            print(f"   Error: {e}")

def main():
    print("\n🚀 Starting corpus ingestion from corpus.jsonl...\n")
    
    # Load documents from corpus.jsonl
    documents = load_corpus("data/corpus.jsonl")
    
    if not documents:
        print("❌ No documents found to ingest!")
        return
    
    print(f"📄 Loaded {len(documents)} documents from corpus.jsonl\n")
    
    # Initialize collections
    print("Initializing Qdrant collections...")
    try:
        retriever.initialize_collections()
        print("✓ Collections initialized\n")
    except Exception as e:
        print(f"⚠️  Warning: {e}\n")
    
    # Ingest documents
    success, errors = ingest_documents(documents)
    
    # Test retrieval if successful
    if success > 0:
        test_retrieval()
    
    print(f"\n✅ Ingestion complete! {success} documents added.\n")

if __name__ == "__main__":
    main()
