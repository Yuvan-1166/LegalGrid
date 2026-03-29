#!/usr/bin/env python3
"""Bulk data ingestion script for expanding the legal corpus"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retriever import retriever
from app.rag.bm25_search import bm25_searcher
from app.utils.chunking import document_chunker
import json

# Expanded Indian legal documents
LEGAL_DOCUMENTS = [
    # Constitution Articles
    {
        "doc_id": "CONST_ART_12",
        "title": "Constitution of India - Article 12: Definition of State",
        "content": """In this Part, unless the context otherwise requires, 'the State' includes the Government and Parliament of India and the Government and the Legislature of each of the States and all local or other authorities within the territory of India or under the control of the Government of India.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "doc_type": "constitution",
            "article": 12,
            "year": 1950,
            "tags": ["fundamental rights", "state", "definition"]
        }
    },
    {
        "doc_id": "CONST_ART_15",
        "title": "Constitution of India - Article 15: Prohibition of discrimination",
        "content": """The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them. No citizen shall, on grounds only of religion, race, caste, sex, place of birth or any of them, be subject to any disability, liability, restriction or condition with regard to access to shops, public restaurants, hotels and places of public entertainment; or the use of wells, tanks, bathing ghats, roads and places of public resort maintained wholly or partly out of State funds or dedicated to the use of the general public.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "doc_type": "constitution",
            "article": 15,
            "year": 1950,
            "tags": ["fundamental rights", "equality", "discrimination"]
        }
    },
    {
        "doc_id": "CONST_ART_19",
        "title": "Constitution of India - Article 19: Protection of certain rights regarding freedom of speech",
        "content": """All citizens shall have the right to freedom of speech and expression; to assemble peaceably and without arms; to form associations or unions; to move freely throughout the territory of India; to reside and settle in any part of the territory of India; and to practise any profession, or to carry on any occupation, trade or business.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "doc_type": "constitution",
            "article": 19,
            "year": 1950,
            "tags": ["fundamental rights", "freedom", "speech"]
        }
    },
    {
        "doc_id": "CONST_ART_32",
        "title": "Constitution of India - Article 32: Remedies for enforcement of rights",
        "content": """The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed. The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, whichever may be appropriate, for the enforcement of any of the rights conferred by this Part.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "doc_type": "constitution",
            "article": 32,
            "year": 1950,
            "tags": ["fundamental rights", "remedies", "writs"]
        }
    },
    # IPC Sections
    {
        "doc_id": "IPC_302",
        "title": "IPC Section 302 - Punishment for murder",
        "content": """Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Penal Code",
            "section": 302,
            "year": 1860,
            "tags": ["criminal", "murder", "punishment"]
        }
    },
    {
        "doc_id": "IPC_304",
        "title": "IPC Section 304 - Punishment for culpable homicide not amounting to murder",
        "content": """Whoever commits culpable homicide not amounting to murder shall be punished with imprisonment for life, or imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine, if the act by which the death is caused is done with the intention of causing death, or of causing such bodily injury as is likely to cause death.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Penal Code",
            "section": 304,
            "year": 1860,
            "tags": ["criminal", "homicide", "punishment"]
        }
    },
    {
        "doc_id": "IPC_375",
        "title": "IPC Section 375 - Rape",
        "content": """A man is said to commit rape if he has sexual intercourse with a woman under circumstances falling under any of the following descriptions: Against her will, Without her consent, With her consent when obtained by putting her or any person in whom she is interested in fear of death or hurt, With her consent when the man knows that he is not her husband and that her consent is given because she believes that he is another man to whom she is or believes herself to be lawfully married, With or without her consent when she is under eighteen years of age.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Penal Code",
            "section": 375,
            "year": 1860,
            "tags": ["criminal", "sexual offence", "rape"]
        }
    },
    {
        "doc_id": "IPC_498A",
        "title": "IPC Section 498A - Husband or relative of husband subjecting woman to cruelty",
        "content": """Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine. Explanation: For the purpose of this section, 'cruelty' means any wilful conduct which is of such a nature as is likely to drive the woman to commit suicide or to cause grave injury or danger to life, limb or health (whether mental or physical) of the woman; or harassment of the woman where such harassment is with a view to coercing her or any person related to her to meet any unlawful demand for any property or valuable security or is on account of failure by her or any person related to her to meet such demand.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Penal Code",
            "section": "498A",
            "year": 1860,
            "tags": ["criminal", "domestic violence", "cruelty"]
        }
    },
    # Indian Contract Act
    {
        "doc_id": "ICA_2",
        "title": "Indian Contract Act Section 2 - Interpretation clause",
        "content": """In this Act the following words and expressions are used in the following senses, unless a contrary intention appears from the context: When one person signifies to another his willingness to do or to abstain from doing anything, with a view to obtaining the assent of that other to such act or abstinence, he is said to make a proposal. When the person to whom the proposal is made signifies his assent thereto, the proposal is said to be accepted. A proposal, when accepted, becomes a promise.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Contract Act",
            "section": 2,
            "year": 1872,
            "tags": ["contract", "definition", "proposal"]
        }
    },
    {
        "doc_id": "ICA_23",
        "title": "Indian Contract Act Section 23 - What considerations and objects are lawful",
        "content": """The consideration or object of an agreement is lawful, unless it is forbidden by law; or is of such a nature that, if permitted, it would defeat the provisions of any law; or is fraudulent; or involves or implies injury to the person or property of another; or the Court regards it as immoral, or opposed to public policy. In each of these cases, the consideration or object of an agreement is said to be unlawful. Every agreement of which the object or consideration is unlawful is void.""",
        "collection": "statutes",
        "jurisdiction": "All-India",
        "metadata": {
            "act_name": "Indian Contract Act",
            "section": 23,
            "year": 1872,
            "tags": ["contract", "lawful", "consideration"]
        }
    },
    # Sample Case Law
    {
        "doc_id": "CASE_KESAVANANDA",
        "title": "Kesavananda Bharati v. State of Kerala (1973)",
        "content": """The Supreme Court held that while Parliament has wide powers to amend the Constitution, it cannot alter the 'basic structure' of the Constitution. This landmark judgment established the basic structure doctrine, which limits the power of Parliament to amend the Constitution. The Court identified several features as part of the basic structure including: supremacy of the Constitution, republican and democratic form of government, secular character of the Constitution, separation of powers between the legislature, executive and judiciary, and federal character of the Constitution.""",
        "collection": "cases",
        "jurisdiction": "All-India",
        "metadata": {
            "court": "Supreme Court",
            "year": 1973,
            "judges": ["Chief Justice S.M. Sikri"],
            "citation_count": 500,
            "holding": "Basic structure doctrine established",
            "tags": ["constitutional law", "basic structure", "landmark"]
        }
    },
    {
        "doc_id": "CASE_MANEKA_GANDHI",
        "title": "Maneka Gandhi v. Union of India (1978)",
        "content": """The Supreme Court expanded the scope of Article 21 (right to life and personal liberty) to include the right to travel abroad. The Court held that the procedure established by law must be just, fair and reasonable, not arbitrary. This case revolutionized the interpretation of fundamental rights and established that Articles 14, 19 and 21 are not mutually exclusive but form a golden triangle. The Court emphasized that any law depriving a person of personal liberty must satisfy the test of reasonableness.""",
        "collection": "cases",
        "jurisdiction": "All-India",
        "metadata": {
            "court": "Supreme Court",
            "year": 1978,
            "judges": ["Justice P.N. Bhagwati"],
            "citation_count": 450,
            "holding": "Expanded scope of Article 21",
            "tags": ["constitutional law", "personal liberty", "landmark"]
        }
    },
    {
        "doc_id": "CASE_VISHAKA",
        "title": "Vishaka v. State of Rajasthan (1997)",
        "content": """The Supreme Court laid down guidelines for prevention of sexual harassment of women at workplace. In the absence of legislation, the Court issued directions to be followed by all employers until suitable legislation is enacted. The guidelines include: express prohibition of sexual harassment, preventive steps, complaint mechanism, disciplinary action, and awareness programs. This case is significant for recognizing sexual harassment as a violation of fundamental rights under Articles 14, 15 and 21.""",
        "collection": "cases",
        "jurisdiction": "All-India",
        "metadata": {
            "court": "Supreme Court",
            "year": 1997,
            "judges": ["Justice J.S. Verma"],
            "citation_count": 300,
            "holding": "Guidelines for sexual harassment at workplace",
            "tags": ["women rights", "sexual harassment", "workplace"]
        }
    },
    {
        "doc_id": "CASE_SHREYA_SINGHAL",
        "title": "Shreya Singhal v. Union of India (2015)",
        "content": """The Supreme Court struck down Section 66A of the Information Technology Act, 2000, which criminalized sending offensive messages through communication services. The Court held that the section was unconstitutional as it violated the freedom of speech and expression guaranteed under Article 19(1)(a). The judgment emphasized that restrictions on free speech must be narrowly tailored and cannot be vague or overbroad. This case is important for protecting online free speech in India.""",
        "collection": "cases",
        "jurisdiction": "All-India",
        "metadata": {
            "court": "Supreme Court",
            "year": 2015,
            "judges": ["Justice J. Chelameswar", "Justice R.F. Nariman"],
            "citation_count": 200,
            "holding": "Section 66A IT Act struck down",
            "tags": ["free speech", "internet", "constitutional law"]
        }
    },
    {
        "doc_id": "CASE_NAVTEJ_JOHAR",
        "title": "Navtej Singh Johar v. Union of India (2018)",
        "content": """The Supreme Court decriminalized consensual homosexual acts by reading down Section 377 of the Indian Penal Code. The Court held that Section 377, insofar as it criminalizes consensual sexual conduct between adults of the same sex, is unconstitutional. The judgment recognized the rights of LGBTQ+ community and held that sexual orientation is a natural phenomenon and discrimination on this ground violates fundamental rights. The Court emphasized that constitutional morality must prevail over social morality.""",
        "collection": "cases",
        "jurisdiction": "All-India",
        "metadata": {
            "court": "Supreme Court",
            "year": 2018,
            "judges": ["Chief Justice Dipak Misra"],
            "citation_count": 150,
            "holding": "Section 377 partially struck down",
            "tags": ["LGBTQ rights", "constitutional law", "equality"]
        }
    }
]

def ingest_documents():
    """Ingest all documents into both Qdrant and BM25 index"""
    print("=" * 60)
    print("Bulk Data Ingestion")
    print("=" * 60)
    print(f"\nIngesting {len(LEGAL_DOCUMENTS)} documents...\n")
    
    success_count = 0
    error_count = 0
    
    for doc in LEGAL_DOCUMENTS:
        try:
            # Add to Qdrant (vector database)
            retriever.add_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc["jurisdiction"],
                metadata=doc["metadata"]
            )
            
            # Add to BM25 index
            bm25_searcher.add_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc["jurisdiction"],
                **doc["metadata"]
            )
            
            print(f"✓ Added: {doc['title']}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error adding {doc['doc_id']}: {e}")
            error_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"Ingestion Complete")
    print(f"{'=' * 60}")
    print(f"✓ Successfully added: {success_count} documents")
    if error_count > 0:
        print(f"✗ Errors: {error_count} documents")
    print(f"\nTotal documents in corpus: {success_count + 5}")  # +5 from seed data

def test_retrieval():
    """Test retrieval with sample queries"""
    print(f"\n{'=' * 60}")
    print("Testing Retrieval")
    print(f"{'=' * 60}\n")
    
    test_queries = [
        ("murder and homicide laws", "statutes"),
        ("fundamental rights and equality", "statutes"),
        ("sexual harassment at workplace", "cases"),
        ("basic structure of constitution", "cases"),
    ]
    
    for query, collection in test_queries:
        print(f"\nQuery: '{query}' in {collection}")
        print("-" * 60)
        
        from app.rag.hybrid_retriever import hybrid_retriever
        results = hybrid_retriever.retrieve(
            query=query,
            collection=collection,
            top_k=3,
            use_hybrid=True
        )
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Score: {result.get('fusion_score', result.get('score', 0)):.3f}")
            print(f"   Method: {result.get('retrieval_method', 'unknown')}")

def main():
    print("\n🚀 Starting bulk data ingestion...\n")
    
    # Ingest documents
    ingest_documents()
    
    # Test retrieval
    test_retrieval()
    
    print(f"\n✅ Bulk ingestion complete!\n")

if __name__ == "__main__":
    main()
