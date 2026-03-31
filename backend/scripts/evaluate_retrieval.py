#!/usr/bin/env python3
"""
Retrieval Quality Evaluation Script
Measures Precision@K, NDCG@K, MRR, and MAP for LegalGrid retrieval system

Metrics:
- Precision@5: % of relevant docs in top-5 results
- NDCG@5: Normalized Discounted Cumulative Gain (ranking quality)
- MRR: Mean Reciprocal Rank (position of first relevant result)
- MAP: Mean Average Precision (overall precision across all ranks)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.hybrid_retriever import hybrid_retriever
import json
import numpy as np
from datetime import datetime
from typing import List, Dict

# Test Queries with Ground Truth
TEST_QUERIES = {
    "contracts": [
        {
            "query": "Is one-sided indemnification clause enforceable in Indian contracts?",
            "relevant_docs": ["IPC_023", "IPC_028", "ICA_10", "ICA_23"],
            "relevance_scores": {"IPC_023": 5, "IPC_028": 4, "ICA_10": 5, "ICA_23": 5},
            "domain": "contract"
        },
        {
            "query": "Unfavorable termination clause without notice period legality",
            "relevant_docs": ["LABOR_REG_001", "LABOR_REG_002", "ICA_10"],
            "relevance_scores": {"LABOR_REG_001": 5, "LABOR_REG_002": 4, "ICA_10": 3},
            "domain": "contract"
        },
        {
            "query": "Liability limitation clauses in service agreements",
            "relevant_docs": ["IPC_023", "ICA_10", "ICA_23"],
            "relevance_scores": {"IPC_023": 4, "ICA_10": 5, "ICA_23": 4},
            "domain": "contract"
        },
        {
            "query": "Non-compete clause enforceability in employment contracts",
            "relevant_docs": ["LABOR_REG_001", "LABOR_REG_002", "ICA_23"],
            "relevance_scores": {"LABOR_REG_001": 5, "LABOR_REG_002": 5, "ICA_23": 3},
            "domain": "contract"
        },
        {
            "query": "Intellectual property ownership in contract agreements",
            "relevant_docs": ["IP_REG_001", "IP_REG_002", "ICA_10"],
            "relevance_scores": {"IP_REG_001": 5, "IP_REG_002": 5, "ICA_10": 3},
            "domain": "contract"
        },
    ],
    "cases": [
        {
            "query": "Employment contract termination without notice period",
            "relevant_docs": ["LABOR_REG_001", "LABOR_REG_002"],
            "relevance_scores": {"LABOR_REG_001": 5, "LABOR_REG_002": 4},
            "domain": "case_law"
        },
        {
            "query": "Fundamental rights violation by state authorities",
            "relevant_docs": ["CONST_ART_14", "CONST_ART_15", "CONST_ART_19", "CONST_ART_21"],
            "relevance_scores": {"CONST_ART_14": 5, "CONST_ART_15": 5, "CONST_ART_19": 4, "CONST_ART_21": 5},
            "domain": "case_law"
        },
        {
            "query": "Property dispute between family members",
            "relevant_docs": ["IPC_420", "IPC_406"],
            "relevance_scores": {"IPC_420": 3, "IPC_406": 4},
            "domain": "case_law"
        },
        {
            "query": "Criminal breach of trust and fraud cases",
            "relevant_docs": ["IPC_420", "IPC_406", "IPC_023"],
            "relevance_scores": {"IPC_420": 5, "IPC_406": 5, "IPC_023": 4},
            "domain": "case_law"
        },
        {
            "query": "Constitutional validity of government regulations",
            "relevant_docs": ["CONST_ART_14", "CONST_ART_19", "CONST_ART_21"],
            "relevance_scores": {"CONST_ART_14": 5, "CONST_ART_19": 5, "CONST_ART_21": 4},
            "domain": "case_law"
        },
    ],
    "compliance": [
        {
            "query": "GST compliance requirements for technology startups",
            "relevant_docs": ["GST_REG_001", "GST_REG_002", "GST_REG_003"],
            "relevance_scores": {"GST_REG_001": 5, "GST_REG_002": 5, "GST_REG_003": 4},
            "domain": "compliance"
        },
        {
            "query": "Labor law compliance for small businesses",
            "relevant_docs": ["LABOR_REG_001", "LABOR_REG_002", "LABOR_REG_003"],
            "relevance_scores": {"LABOR_REG_001": 5, "LABOR_REG_002": 5, "LABOR_REG_003": 4},
            "domain": "compliance"
        },
        {
            "query": "Income tax filing requirements for companies",
            "relevant_docs": ["TAX_REG_001", "TAX_REG_002", "TAX_REG_003"],
            "relevance_scores": {"TAX_REG_001": 5, "TAX_REG_002": 5, "TAX_REG_003": 4},
            "domain": "compliance"
        },
        {
            "query": "Intellectual property registration procedures",
            "relevant_docs": ["IP_REG_001", "IP_REG_002", "IP_REG_003"],
            "relevance_scores": {"IP_REG_001": 5, "IP_REG_002": 5, "IP_REG_003": 4},
            "domain": "compliance"
        },
        {
            "query": "Corporate governance compliance for private companies",
            "relevant_docs": ["GST_REG_001", "TAX_REG_001", "LABOR_REG_001"],
            "relevance_scores": {"GST_REG_001": 4, "TAX_REG_001": 4, "LABOR_REG_001": 3},
            "domain": "compliance"
        },
    ],
    "disputes": [
        {
            "query": "Property dispute between siblings over inherited land",
            "relevant_docs": ["IPC_420", "IPC_406"],
            "relevance_scores": {"IPC_420": 3, "IPC_406": 4},
            "domain": "dispute"
        },
        {
            "query": "Business partnership dissolution dispute",
            "relevant_docs": ["ICA_10", "ICA_23", "IPC_420"],
            "relevance_scores": {"ICA_10": 5, "ICA_23": 5, "IPC_420": 3},
            "domain": "dispute"
        },
        {
            "query": "Employment termination dispute with severance pay",
            "relevant_docs": ["LABOR_REG_001", "LABOR_REG_002"],
            "relevance_scores": {"LABOR_REG_001": 5, "LABOR_REG_002": 5},
            "domain": "dispute"
        },
        {
            "query": "Contract breach and damages claim",
            "relevant_docs": ["ICA_10", "ICA_23", "IPC_023"],
            "relevance_scores": {"ICA_10": 5, "ICA_23": 5, "IPC_023": 4},
            "domain": "dispute"
        },
        {
            "query": "Intellectual property infringement dispute",
            "relevant_docs": ["IP_REG_001", "IP_REG_002", "IPC_028"],
            "relevance_scores": {"IP_REG_001": 5, "IP_REG_002": 5, "IPC_028": 4},
            "domain": "dispute"
        },
    ]
}

def evaluate_precision_at_k(queries: Dict, k: int = 5) -> Dict:
    """
    Calculate Precision@K for each domain
    
    Precision@K = (# relevant docs in top-K) / K
    """
    print(f"\n{'='*70}")
    print(f"EVALUATING PRECISION@{k}")
    print('='*70)
    
    results_by_domain = {}
    all_precisions = []
    
    for domain, query_list in queries.items():
        domain_precisions = []
        
        print(f"\nDomain: {domain.upper()}")
        print("-" * 70)
        
        for q in query_list:
            try:
                # Retrieve documents
                retrieved = hybrid_retriever.retrieve(
                    query=q['query'],
                    collection="statutes" if domain in ["contracts", "cases"] else "regulations",
                    top_k=k,
                    use_hybrid=True
                )
                
                # Get relevant and retrieved doc IDs
                relevant = set(q['relevant_docs'])
                retrieved_ids = set([doc.get('doc_id', '') for doc in retrieved])
                
                # Calculate precision
                relevant_retrieved = relevant & retrieved_ids
                precision = len(relevant_retrieved) / k if k > 0 else 0
                
                domain_precisions.append(precision)
                all_precisions.append(precision)
                
                print(f"  Query: {q['query'][:50]}...")
                print(f"    Precision@{k}: {precision:.3f} ({len(relevant_retrieved)}/{k} relevant)")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                domain_precisions.append(0)
                all_precisions.append(0)
        
        # Domain average
        domain_avg = np.mean(domain_precisions) if domain_precisions else 0
        results_by_domain[domain] = {
            "precision": domain_avg,
            "queries": len(domain_precisions)
        }
        print(f"\n  Domain Average: {domain_avg:.3f}")
    
    # Overall average
    overall_precision = np.mean(all_precisions) if all_precisions else 0
    
    return {
        "overall": overall_precision,
        "by_domain": results_by_domain,
        "k": k
    }

def calculate_ndcg(queries: Dict, k: int = 5) -> Dict:
    """
    Calculate NDCG@K (Normalized Discounted Cumulative Gain)
    
    NDCG accounts for ranking order - perfect ranking = 1.0
    Formula: DCG = Σ (rel_i / log2(i+1))
             NDCG = DCG / IDCG
    """
    print(f"\n{'='*70}")
    print(f"EVALUATING NDCG@{k}")
    print('='*70)
    
    results_by_domain = {}
    all_ndcg = []
    
    for domain, query_list in queries.items():
        domain_ndcg = []
        
        print(f"\nDomain: {domain.upper()}")
        print("-" * 70)
        
        for q in query_list:
            try:
                # Retrieve documents
                retrieved = hybrid_retriever.retrieve(
                    query=q['query'],
                    collection="statutes" if domain in ["contracts", "cases"] else "regulations",
                    top_k=k,
                    use_hybrid=True
                )
                
                # Build relevance arrays
                relevance_scores = q.get('relevance_scores', {})
                y_true = []
                
                for doc in retrieved:
                    doc_id = doc.get('doc_id', '')
                    y_true.append(relevance_scores.get(doc_id, 0))
                
                # Pad to k if needed
                while len(y_true) < k:
                    y_true.append(0)
                
                # Calculate DCG
                dcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(y_true))
                
                # Calculate IDCG (ideal DCG with perfect ranking)
                ideal_relevances = sorted(relevance_scores.values(), reverse=True)[:k]
                while len(ideal_relevances) < k:
                    ideal_relevances.append(0)
                idcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(ideal_relevances))
                
                # Calculate NDCG
                ndcg = dcg / idcg if idcg > 0 else 0
                
                domain_ndcg.append(ndcg)
                all_ndcg.append(ndcg)
                
                print(f"  Query: {q['query'][:50]}...")
                print(f"    NDCG@{k}: {ndcg:.3f}")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                domain_ndcg.append(0)
                all_ndcg.append(0)
        
        # Domain average
        domain_avg = np.mean(domain_ndcg) if domain_ndcg else 0
        results_by_domain[domain] = {
            "ndcg": domain_avg,
            "queries": len(domain_ndcg)
        }
        print(f"\n  Domain Average: {domain_avg:.3f}")
    
    # Overall average
    overall_ndcg = np.mean(all_ndcg) if all_ndcg else 0
    
    return {
        "overall": overall_ndcg,
        "by_domain": results_by_domain,
        "k": k
    }

def calculate_mrr(queries: Dict) -> Dict:
    """
    Calculate Mean Reciprocal Rank
    
    MRR = average of (1 / rank of first relevant result)
    """
    print(f"\n{'='*70}")
    print("EVALUATING MRR (Mean Reciprocal Rank)")
    print('='*70)
    
    results_by_domain = {}
    all_rr = []
    
    for domain, query_list in queries.items():
        domain_rr = []
        
        print(f"\nDomain: {domain.upper()}")
        print("-" * 70)
        
        for q in query_list:
            try:
                # Retrieve documents
                retrieved = hybrid_retriever.retrieve(
                    query=q['query'],
                    collection="statutes" if domain in ["contracts", "cases"] else "regulations",
                    top_k=10,
                    use_hybrid=True
                )
                
                # Find rank of first relevant result
                relevant = set(q['relevant_docs'])
                first_relevant_rank = None
                
                for i, doc in enumerate(retrieved, 1):
                    doc_id = doc.get('doc_id', '')
                    if doc_id in relevant:
                        first_relevant_rank = i
                        break
                
                # Calculate reciprocal rank
                rr = 1.0 / first_relevant_rank if first_relevant_rank else 0
                
                domain_rr.append(rr)
                all_rr.append(rr)
                
                print(f"  Query: {q['query'][:50]}...")
                print(f"    RR: {rr:.3f} (first relevant at rank {first_relevant_rank or 'N/A'})")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                domain_rr.append(0)
                all_rr.append(0)
        
        # Domain average
        domain_avg = np.mean(domain_rr) if domain_rr else 0
        results_by_domain[domain] = {
            "mrr": domain_avg,
            "queries": len(domain_rr)
        }
        print(f"\n  Domain Average: {domain_avg:.3f}")
    
    # Overall average
    overall_mrr = np.mean(all_rr) if all_rr else 0
    
    return {
        "overall": overall_mrr,
        "by_domain": results_by_domain
    }

def save_results(results: Dict, filename: str = "metrics/evaluation_baseline.json"):
    """Save evaluation results to JSON file"""
    os.makedirs("metrics", exist_ok=True)
    
    with open(filename, "w") as f:
        json.dumps(results, f, indent=2)
    
    print(f"\n✓ Results saved to: {filename}")

def create_report(results: Dict):
    """Create markdown report"""
    report = f"""# LegalGrid Retrieval Evaluation Results

**Evaluation Date**: {results['evaluation_date']}  
**Total Test Queries**: {results['test_count']}

---

## Overall Metrics

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Precision@5 | {results['metrics']['precision_at_5']:.3f} | >0.800 | {'✅ PASS' if results['metrics']['precision_at_5'] >= 0.80 else '❌ FAIL'} |
| NDCG@5 | {results['metrics']['ndcg_at_5']:.3f} | >0.750 | {'✅ PASS' if results['metrics']['ndcg_at_5'] >= 0.75 else '❌ FAIL'} |
| MRR | {results['metrics']['mrr']:.3f} | >0.850 | {'✅ PASS' if results['metrics']['mrr'] >= 0.85 else '❌ FAIL'} |

---

## By Domain

### Contracts
- Precision@5: {results['metrics']['by_domain']['contracts']['precision']:.3f}
- NDCG@5: {results['metrics']['by_domain']['contracts']['ndcg']:.3f}
- MRR: {results['metrics']['by_domain']['contracts']['mrr']:.3f}

### Cases
- Precision@5: {results['metrics']['by_domain']['cases']['precision']:.3f}
- NDCG@5: {results['metrics']['by_domain']['cases']['ndcg']:.3f}
- MRR: {results['metrics']['by_domain']['cases']['mrr']:.3f}

### Compliance
- Precision@5: {results['metrics']['by_domain']['compliance']['precision']:.3f}
- NDCG@5: {results['metrics']['by_domain']['compliance']['ndcg']:.3f}
- MRR: {results['metrics']['by_domain']['compliance']['mrr']:.3f}

### Disputes
- Precision@5: {results['metrics']['by_domain']['disputes']['precision']:.3f}
- NDCG@5: {results['metrics']['by_domain']['disputes']['ndcg']:.3f}
- MRR: {results['metrics']['by_domain']['disputes']['mrr']:.3f}

---

## Recommendations

"""
    
    # Add recommendations based on results
    if results['metrics']['precision_at_5'] < 0.80:
        report += "- ⚠️ Precision@5 below target - Consider expanding corpus or fine-tuning embeddings\n"
    if results['metrics']['ndcg_at_5'] < 0.75:
        report += "- ⚠️ NDCG@5 below target - Consider adding cross-encoder reranking\n"
    if results['metrics']['mrr'] < 0.85:
        report += "- ⚠️ MRR below target - First relevant result not ranking high enough\n"
    
    if all([
        results['metrics']['precision_at_5'] >= 0.80,
        results['metrics']['ndcg_at_5'] >= 0.75,
        results['metrics']['mrr'] >= 0.85
    ]):
        report += "- ✅ All metrics meet targets - System performing well!\n"
    
    report += "\n---\n\n*Generated by LegalGrid Evaluation System*\n"
    
    with open("EVALUATION_RESULTS.md", "w") as f:
        f.write(report)
    
    print("\n✓ Report saved to: EVALUATION_RESULTS.md")

def main():
    print("\n" + "="*70)
    print("LEGALGRID RETRIEVAL QUALITY EVALUATION")
    print("="*70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Count total queries
    total_queries = sum(len(queries) for queries in TEST_QUERIES.values())
    print(f"Total Test Queries: {total_queries}")
    print(f"Domains: {', '.join(TEST_QUERIES.keys())}")
    
    # Run evaluations
    precision_results = evaluate_precision_at_k(TEST_QUERIES, k=5)
    ndcg_results = calculate_ndcg(TEST_QUERIES, k=5)
    mrr_results = calculate_mrr(TEST_QUERIES)
    
    # Compile results
    results = {
        "evaluation_date": datetime.now().isoformat(),
        "test_count": total_queries,
        "metrics": {
            "precision_at_5": precision_results['overall'],
            "ndcg_at_5": ndcg_results['overall'],
            "mrr": mrr_results['overall'],
            "by_domain": {
                domain: {
                    "precision": precision_results['by_domain'][domain]['precision'],
                    "ndcg": ndcg_results['by_domain'][domain]['ndcg'],
                    "mrr": mrr_results['by_domain'][domain]['mrr'],
                }
                for domain in TEST_QUERIES.keys()
            }
        }
    }
    
    # Print summary
    print(f"\n{'='*70}")
    print("EVALUATION SUMMARY")
    print('='*70)
    print(f"Precision@5: {results['metrics']['precision_at_5']:.3f} (target: >0.800)")
    print(f"NDCG@5:      {results['metrics']['ndcg_at_5']:.3f} (target: >0.750)")
    print(f"MRR:         {results['metrics']['mrr']:.3f} (target: >0.850)")
    print()
    
    # Save results
    save_results(results)
    create_report(results)
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✅ Evaluation complete!\n")

if __name__ == "__main__":
    main()
