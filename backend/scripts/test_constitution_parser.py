#!/usr/bin/env python3
"""Test constitution parser without ingesting to Qdrant"""

import sys
import os
from pathlib import Path
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import PyPDF2
except ImportError:
    print("Installing PyPDF2...")
    os.system("pip install PyPDF2")
    import PyPDF2

# Import parsing functions from ingest_constitution
from ingest_constitution import extract_text_from_pdf, parse_constitution_articles

def main():
    print("\n🧪 Testing Constitution Parser (No Ingestion)\n")
    
    pdf_path = "data/IndianConstitution.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ Error: {pdf_path} not found!")
        return
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    
    # Parse articles
    documents = parse_constitution_articles(text)
    
    if not documents:
        print("❌ No articles found!")
        return
    
    # Save to JSON
    output_path = "data/constitution_parsed.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Parsed {len(documents)} articles")
    print(f"💾 Saved to: {output_path}\n")
    
    # Show sample articles
    print("📋 Sample Articles:\n")
    print("=" * 70)
    
    for i, doc in enumerate(documents[:5], 1):
        print(f"\n{i}. Article {doc['article_number']}: {doc['title']}")
        print(f"   Part: {doc['part']} - {doc['part_title']}")
        print(f"   Content length: {len(doc['content'])} chars")
        if doc.get('clauses'):
            print(f"   Clauses: {len(doc['clauses'])}")
        print(f"   Preview: {doc['content'][:150]}...")
    
    print("\n" + "=" * 70)
    print(f"\n✅ Test complete! Review full output in: {output_path}\n")

if __name__ == "__main__":
    main()
