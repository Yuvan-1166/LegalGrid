#!/usr/bin/env python3
"""Corpus expansion via API - adds 80+ documents"""
import requests
import json
import time

API_BASE = "http://localhost:8000/api/v1/qdrant"

def add_doc(doc_id, title, content, collection, metadata):
    """Add document via API"""
    try:
        response = requests.post(
            f"{API_BASE}/add-document",
            json={
                "doc_id": doc_id,
                "title": title,
                "content": content,
                "collection": collection,
                "jurisdiction": "All-India",
                "metadata": metadata
            },
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Constitution Articles
constitution_docs = [
    ("CONST_ART_13", "Constitution - Article 13: Laws inconsistent with fundamental rights",
     "All laws in force in the territory of India immediately before the commencement of this Constitution, in so far as they are inconsistent with the provisions of this Part, shall, to the extent of such inconsistency, be void. The State shall not make any law which takes away or abridges the rights conferred by this Part.",
     {"article": 13, "year": 1950, "tags": ["fundamental rights", "judicial review"]}),
    
    ("CONST_ART_16", "Constitution - Article 16: Equality of opportunity in public employment",
     "There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State. No citizen shall, on grounds only of religion, race, caste, sex, descent, place of birth, residence or any of them, be ineligible for, or discriminated against in respect of, any employment or office under the State.",
     {"article": 16, "year": 1950, "tags": ["equality", "employment", "reservation"]}),
]

# IPC Sections
ipc_docs = [
    ("IPC_299", "IPC Section 299 - Culpable homicide",
     "Whoever causes death by doing an act with the intention of causing death, or with the intention of causing such bodily injury as is likely to cause death, or with the knowledge that he is likely by such act to cause death, commits the offence of culpable homicide.",
     {"section": 299, "year": 1860, "act_name": "Indian Penal Code", "tags": ["criminal", "homicide"]}),
    
    ("IPC_300", "IPC Section 300 - Murder",
     "Culpable homicide is murder if the act by which the death is caused is done with the intention of causing death, or with the intention of causing such bodily injury as the offender knows to be likely to cause the death of the person to whom the harm is caused.",
     {"section": 300, "year": 1860, "act_name": "Indian Penal Code", "tags": ["criminal", "murder"]}),
    
    ("IPC_307", "IPC Section 307 - Attempt to murder",
     "Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty of murder, shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine.",
     {"section": 307, "year": 1860, "act_name": "Indian Penal Code", "tags": ["criminal", "attempt to murder"]}),
]

# Landmark Cases
case_docs = [
    ("CASE_ADM_JABALPUR", "ADM Jabalpur v. Shivkant Shukla (1976)",
     "During the Emergency of 1975-77, the Supreme Court held that the right to life and personal liberty under Article 21 could be suspended during Emergency. This controversial judgment was later criticized and effectively overruled by subsequent decisions. The case is remembered as a dark chapter in Indian constitutional history where the Court failed to protect fundamental rights during Emergency.",
     {"court": "Supreme Court", "year": 1976, "citation_count": 200, "tags": ["emergency", "fundamental rights", "article 21"]}),
    
    ("CASE_PUTTASWAMY", "K.S. Puttaswamy v. Union of India (2017)",
     "The Supreme Court unanimously held that the right to privacy is a fundamental right protected under Article 21 of the Constitution. The nine-judge bench overruled earlier judgments that had held privacy was not a fundamental right. This judgment has far-reaching implications for data protection, surveillance, and individual autonomy.",
     {"court": "Supreme Court", "year": 2017, "citation_count": 300, "tags": ["privacy", "fundamental rights", "data protection"]}),
]

def main():
    print("=" * 70)
    print("CORPUS EXPANSION VIA API")
    print("=" * 70)
    
    all_docs = constitution_docs + ipc_docs + case_docs
    success = 0
    failed = 0
    
    print(f"\nAdding {len(all_docs)} documents...\n")
    
    for doc_id, title, content, metadata in all_docs:
        collection = "cases" if doc_id.startswith("CASE_") else "statutes"
        
        if add_doc(doc_id, title, content, collection, metadata):
            print(f"✓ {doc_id}")
            success += 1
        else:
            print(f"✗ {doc_id}")
            failed += 1
        
        time.sleep(0.1)  # Rate limiting
    
    print(f"\n{'=' * 70}")
    print(f"RESULTS")
    print(f"{'=' * 70}")
    print(f"✓ Success: {success}")
    print(f"✗ Failed: {failed}")
    print(f"Total corpus: ~{20 + success} documents")

if __name__ == "__main__":
    main()
