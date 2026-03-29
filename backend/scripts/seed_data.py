#!/usr/bin/env python3
"""Seed initial legal documents into Qdrant"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retriever import retriever

# Sample Indian legal documents
SAMPLE_DOCUMENTS = [
    {
        "doc_id": "IPC_420",
        "title": "IPC Section 420 - Cheating and dishonestly inducing delivery of property",
        "content": """Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or anything which is signed or sealed, and which is capable of being converted into a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Penal Code",
            "section": 420,
            "year": 1860,
            "tags": ["fraud", "criminal", "cheating"]
        }
    },
    {
        "doc_id": "IPC_406",
        "title": "IPC Section 406 - Punishment for criminal breach of trust",
        "content": """Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Penal Code",
            "section": 406,
            "year": 1860,
            "tags": ["breach of trust", "criminal"]
        }
    },
    {
        "doc_id": "CONSTITUTION_14",
        "title": "Constitution of India - Article 14: Equality before law",
        "content": """The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "doc_type": "constitution",
            "article": 14,
            "year": 1950,
            "tags": ["fundamental rights", "equality"]
        }
    },
    {
        "doc_id": "CONSTITUTION_21",
        "title": "Constitution of India - Article 21: Protection of life and personal liberty",
        "content": """No person shall be deprived of his life or personal liberty except according to procedure established by law.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "doc_type": "constitution",
            "article": 21,
            "year": 1950,
            "tags": ["fundamental rights", "life", "liberty"]
        }
    },
    {
        "doc_id": "ICA_10",
        "title": "Indian Contract Act Section 10 - What agreements are contracts",
        "content": """All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Contract Act",
            "section": 10,
            "year": 1872,
            "tags": ["contract", "agreement", "consideration"]
        }
    }
]

def main():
    print("Initializing Qdrant collections...")
    retriever.initialize_collections()
    
    print("\nSeeding sample documents...")
    for doc in SAMPLE_DOCUMENTS:
        retriever.add_document(
            doc_id=doc["doc_id"],
            title=doc["title"],
            content=doc["content"],
            collection=doc["collection"],
            jurisdiction=doc["jurisdiction"],
            metadata=doc["metadata"]
        )
        print(f"✓ Added: {doc['title']}")
    
    print(f"\n✓ Successfully seeded {len(SAMPLE_DOCUMENTS)} documents")
    
    # Test retrieval
    print("\nTesting retrieval...")
    results = retriever.retrieve(
        query="contract enforceability and consideration",
        collection="statutes",
        top_k=3
    )
    
    print(f"\nFound {len(results)} relevant documents:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']} (score: {result['score']:.3f})")

if __name__ == "__main__":
    main()
