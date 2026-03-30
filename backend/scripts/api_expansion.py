#!/usr/bin/env python3
"""
API-based corpus expansion
Uses the running backend API to add documents
"""

import requests
import json

API_BASE = "http://localhost:8000/api/v1"

def add_document_via_api(doc):
    """Add document using the Qdrant API endpoint"""
    try:
        response = requests.post(
            f"{API_BASE}/qdrant/add",
            json=doc,
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Sample of documents to add (abbreviated for demonstration)
DOCUMENTS = [
    {
        "doc_id": "CONST_ART_13",
        "title": "Constitution - Article 13",
        "content": "Laws inconsistent with fundamental rights shall be void...",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {"article": 13, "year": 1950}
    },
    # Add more documents here
]

def main():
    print("Adding documents via API...")
    success = 0
    for doc in DOCUMENTS:
        if add_document_via_api(doc):
            print(f"✓ {doc['doc_id']}")
            success += 1
        else:
            print(f"✗ {doc['doc_id']}")
    
    print(f"\nAdded {success}/{len(DOCUMENTS)} documents")

if __name__ == "__main__":
    main()
