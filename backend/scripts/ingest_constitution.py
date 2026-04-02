#!/usr/bin/env python3
"""Extract and ingest Indian Constitution from PDF"""

import sys
import os
from pathlib import Path
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retriever import retriever
from app.rag.bm25_search import bm25_searcher

try:
    import PyPDF2
except ImportError:
    print("Installing PyPDF2...")
    os.system("pip install PyPDF2")
    import PyPDF2

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from PDF"""
    print(f"📖 Reading PDF: {pdf_path}")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        print(f"   Total pages: {total_pages}")
        
        text = ""
        for page_num, page in enumerate(pdf_reader.pages, 1):
            if page_num % 50 == 0:
                print(f"   Processing page {page_num}/{total_pages}...")
            text += page.extract_text() + "\n\n"
        
        print(f"✓ Extracted {len(text)} characters\n")
        return text

def clean_text(text: str) -> str:
    """STEP 1: Remove non-content sections"""
    print("🧹 Cleaning text...")
    
    # Find PREAMBLE and start from there
    preamble_match = re.search(r'PREAMBLE', text, re.IGNORECASE)
    if preamble_match:
        text = text[preamble_match.start():]
        print("   ✓ Found PREAMBLE, starting from there")
    
    # Remove amendment footnotes
    text = re.sub(r'(?:Subs\.|Ins\.|Omitted)\s+by\s+the\s+Constitution[^\n]*', '', text)
    
    # Remove page numbers (standalone numbers on lines)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    print("   ✓ Cleaned text\n")
    return text

def extract_parts_and_chapters(text: str):
    """STEP 2: Identify document structure"""
    print("📑 Extracting document structure...")
    
    structure = []
    
    # Find all PARTS
    part_pattern = r'PART\s+([IVXLCDM]+)\s*\n\s*([^\n]+)'
    part_matches = list(re.finditer(part_pattern, text, re.IGNORECASE))
    
    for i, match in enumerate(part_matches):
        part_num = match.group(1).strip()
        part_title = match.group(2).strip()
        
        start_pos = match.start()
        end_pos = part_matches[i + 1].start() if i + 1 < len(part_matches) else len(text)
        part_text = text[start_pos:end_pos]
        
        structure.append({
            "part": f"PART {part_num}",
            "part_title": part_title,
            "text": part_text,
            "start": start_pos,
            "end": end_pos
        })
    
    print(f"   ✓ Found {len(structure)} parts\n")
    return structure

def parse_article_content(content: str):
    """STEP 5: Parse internal structure (clauses, subclauses)"""
    clauses = []
    
    # Match clauses like (1), (2), (3)
    clause_pattern = r'\((\d+)\)\s*([^(]+?)(?=\(\d+\)|$)'
    clause_matches = re.finditer(clause_pattern, content, re.DOTALL)
    
    for match in clause_matches:
        clause_num = match.group(1)
        clause_text = match.group(2).strip()
        
        # Extract subclauses (a), (b), (c)
        subclauses = []
        subclause_pattern = r'\(([a-z])\)\s*([^(]+?)(?=\([a-z]\)|$)'
        for sub_match in re.finditer(subclause_pattern, clause_text, re.DOTALL):
            subclauses.append({
                "subclause": f"({sub_match.group(1)})",
                "text": sub_match.group(2).strip()
            })
        
        clauses.append({
            "clause": f"({clause_num})",
            "text": clause_text,
            "subclauses": subclauses if subclauses else None
        })
    
    return clauses if clauses else None

def parse_constitution_articles(text: str):
    """Parse constitution text into structured articles following strict rules"""
    print("🔍 Parsing articles from constitution text...\n")
    
    # STEP 1: Clean text
    text = clean_text(text)
    
    # STEP 2: Extract parts
    parts = extract_parts_and_chapters(text)
    
    documents = []
    
    # STEP 3: Extract articles from each part
    for part_info in parts:
        part_text = part_info["text"]
        
        # STEP 3: Article pattern - matches [21., 21A., 243ZB., etc.
        # Pattern: optional "[", number + optional letters, ".", title
        article_pattern = r'^\s*\[?(\d+[A-Z]{0,2})\.\s+([^\n—]+?)(?:—|\.—)?\s*'
        
        lines = part_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            match = re.match(article_pattern, line)
            
            if match:
                article_num = match.group(1).strip()
                title = match.group(2).strip()
                
                # STEP 4: Handle edge cases
                status = "active"
                if line.startswith('[') and 'Omitted' in line:
                    status = "omitted"
                    i += 1
                    continue
                
                # Collect content until next article
                content_lines = []
                i += 1
                
                while i < len(lines):
                    next_line = lines[i]
                    # Check if this is the start of next article
                    if re.match(article_pattern, next_line):
                        break
                    # Check if we hit next PART
                    if re.match(r'PART\s+[IVXLCDM]+', next_line, re.IGNORECASE):
                        break
                    content_lines.append(next_line)
                    i += 1
                
                content = '\n'.join(content_lines).strip()
                
                # STEP 6: Clean content
                content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
                content = re.sub(r' +', ' ', content)
                
                # STEP 7: Validation - skip if too short
                if len(content) < 30:
                    continue
                
                # Limit length
                if len(content) > 3000:
                    content = content[:3000] + "..."
                
                # STEP 5: Parse clauses
                clauses = parse_article_content(content)
                
                # STEP 7: Output format
                doc = {
                    "doc_id": f"CONST_ART_{article_num}",
                    "part": part_info["part"],
                    "part_title": part_info["part_title"],
                    "article_number": article_num,
                    "title": title,
                    "content": content,
                    "clauses": clauses,
                    "status": status,
                    "collection": "statutes",
                    "jurisdiction": "All-India",
                    "metadata": {
                        "doc_type": "constitution",
                        "article": article_num,
                        "year": 1950,
                        "part": part_info["part"],
                        "tags": ["constitution", "fundamental law", part_info["part_title"].lower()]
                    }
                }
                
                documents.append(doc)
            else:
                i += 1
    
    # STEP 8: Validation - remove duplicates
    seen = set()
    unique_docs = []
    for doc in documents:
        if doc["article_number"] not in seen:
            seen.add(doc["article_number"])
            unique_docs.append(doc)
    
    print(f"✓ Parsed {len(unique_docs)} unique articles\n")
    return unique_docs

def chunk_large_text(text: str, chunk_size: int = 1500, overlap: int = 200):
    """Split large text into overlapping chunks"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary
        if end < len(text):
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            
            if break_point > chunk_size * 0.7:  # At least 70% through
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks

def save_to_json(documents, output_path="data/constitution_parsed.json"):
    """Save parsed articles to JSON file for inspection"""
    import json
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved parsed articles to: {output_path}\n")

def ingest_documents(documents):
    """Ingest documents into Qdrant and BM25"""
    print("=" * 70)
    print("Ingesting Constitution Articles")
    print("=" * 70)
    print(f"\nIngesting {len(documents)} articles...\n")
    
    success_count = 0
    error_count = 0
    
    for i, doc in enumerate(documents, 1):
        try:
            # Format title for display
            title = f"Constitution of India - Article {doc['article_number']}: {doc['title']}"
            
            # Add to Qdrant
            retriever.add_document(
                doc_id=doc["doc_id"],
                title=title,
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc["jurisdiction"],
                metadata=doc["metadata"]
            )
            
            # Add to BM25
            bm25_searcher.add_document(
                doc_id=doc["doc_id"],
                title=title,
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc["jurisdiction"],
                **doc["metadata"]
            )
            
            if i % 20 == 0:
                print(f"✓ Progress: {i}/{len(documents)} articles...")
            
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error adding {doc['doc_id']}: {e}")
            error_count += 1
    
    print(f"\n{'=' * 70}")
    print(f"✓ Successfully added: {success_count} articles")
    if error_count > 0:
        print(f"✗ Errors: {error_count} articles")
    print(f"{'=' * 70}\n")
    
    return success_count, error_count

def main():
    print("\n🇮🇳 Indian Constitution PDF Ingestion\n")
    
    pdf_path = "data/IndianConstitution.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ Error: {pdf_path} not found!")
        return
    
    # Initialize collections
    print("Initializing Qdrant collections...")
    try:
        retriever.initialize_collections()
        print("✓ Collections initialized\n")
    except Exception as e:
        print(f"⚠️  Collections may already exist: {e}\n")
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Parse into articles
    documents = parse_constitution_articles(text)
    
    if not documents:
        print("❌ No articles found!\n")
        return
    
    # Save parsed JSON for inspection
    save_to_json(documents)
    
    # Ingest documents
    success, errors = ingest_documents(documents)
    
    # Test retrieval
    if success > 0:
        print("\n🧪 Testing retrieval...")
        print("-" * 70)
        
        test_queries = [
            "fundamental rights",
            "Article 21 life and liberty",
            "equality before law"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            try:
                results = retriever.retrieve(
                    query=query,
                    collection="statutes",
                    top_k=3
                )
                for j, result in enumerate(results, 1):
                    print(f"  {j}. {result['title'][:80]}...")
            except Exception as e:
                print(f"  Error: {e}")
    
    print(f"\n✅ Constitution ingestion complete! {success} articles added.\n")
    print(f"📄 Review parsed structure: data/constitution_parsed.json\n")

if __name__ == "__main__":
    main()
