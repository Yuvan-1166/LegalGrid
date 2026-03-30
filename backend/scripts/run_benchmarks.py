#!/usr/bin/env python3
"""
Run retrieval benchmarks and generate performance report
Measures Precision@5, NDCG@5, and system performance
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.benchmarks import RetrievalBenchmark, SAMPLE_TEST_QUERIES
from app.rag.hybrid_retriever import hybrid_retriever
from app.core.cache import retrieval_cache
from app.core.monitoring import performance_monitor
import time
import json

def run_retrieval_benchmarks():
    """Run retrieval quality benchmarks"""
    print("=" * 70)
    print("RETRIEVAL QUALITY BENCHMARKS")
    print("=" * 70)
    print()
    
    # Initialize benchmark
    benchmark = RetrievalBenchmark(SAMPLE_TEST_QUERIES)
    
    # Run benchmarks
    print("Running Precision@5 benchmark...")
    precision_5 = benchmark.precision_at_k(hybrid_retriever, k=5)
    
    print("Running NDCG@5 benchmark...")
    ndcg_5 = benchmark.ndcg_at_k(hybrid_retriever, k=5)
    
    # Get full results
    results = benchmark.run_full_benchmark(hybrid_retriever)
    
    print("\n" + "=" * 70)
    print("BENCHMARK RESULTS")
    print("=" * 70)
    print(f"Precision@5: {results['precision_at_5']:.1%}")
    print(f"NDCG@5: {results['ndcg_at_5']:.3f}")
    print(f"Total Queries: {results['total_queries']}")
    print()
    print(f"Target Precision@5: {results['target_precision']:.1%}")
    print(f"Target NDCG@5: {results['target_ndcg']:.3f}")
    print()
    print(f"Precision Target Met: {'✅ YES' if results['precision_met'] else '❌ NO'}")
    print(f"NDCG Target Met: {'✅ YES' if results['ndcg_met'] else '❌ NO'}")
    
    return results

def test_cache_performance():
    """Test caching effectiveness"""
    print("\n" + "=" * 70)
    print("CACHE PERFORMANCE TEST")
    print("=" * 70)
    print()
    
    test_query = "contract enforceability and consideration"
    
    # Clear cache
    retrieval_cache.clear()
    
    # First query (no cache)
    start = time.time()
    results1 = hybrid_retriever.retrieve(
        query=test_query,
        collection="statutes",
        top_k=5,
        use_cache=True
    )
    time_no_cache = time.time() - start
    
    # Second query (with cache)
    start = time.time()
    results2 = hybrid_retriever.retrieve(
        query=test_query,
        collection="statutes",
        top_k=5,
        use_cache=True
    )
    time_with_cache = time.time() - start
    
    speedup = (time_no_cache / time_with_cache) if time_with_cache > 0 else 0
    
    print(f"Query: '{test_query}'")
    print(f"First query (no cache): {time_no_cache:.3f}s")
    print(f"Second query (cached): {time_with_cache:.3f}s")
    print(f"Speedup: {speedup:.1f}x faster")
    print(f"Cache stats: {retrieval_cache.get_stats()}")
    
    return {
        "time_no_cache": time_no_cache,
        "time_with_cache": time_with_cache,
        "speedup": speedup,
        "cache_stats": retrieval_cache.get_stats()
    }

def test_system_performance():
    """Test overall system performance"""
    print("\n" + "=" * 70)
    print("SYSTEM PERFORMANCE TEST")
    print("=" * 70)
    print()
    
    # Test queries
    test_queries = [
        ("murder laws", "statutes"),
        ("fundamental rights", "statutes"),
        ("privacy rights", "cases"),
        ("contract breach", "statutes"),
        ("workplace harassment", "cases")
    ]
    
    times = []
    for query, collection in test_queries:
        start = time.time()
        results = hybrid_retriever.retrieve(
            query=query,
            collection=collection,
            top_k=5,
            use_cache=False  # Test without cache
        )
        duration = time.time() - start
        times.append(duration)
        print(f"✓ Query: '{query}' - {duration:.3f}s - {len(results)} results")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print()
    print(f"Average response time: {avg_time:.3f}s")
    print(f"Min response time: {min_time:.3f}s")
    print(f"Max response time: {max_time:.3f}s")
    print(f"Target: < 3s per query")
    print(f"Status: {'✅ PASS' if avg_time < 3 else '❌ FAIL'}")
    
    return {
        "avg_time": avg_time,
        "min_time": min_time,
        "max_time": max_time,
        "target_met": avg_time < 3
    }

def generate_performance_report(benchmark_results, cache_results, performance_results):
    """Generate comprehensive performance report"""
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "retrieval_quality": {
            "precision_at_5": benchmark_results["precision_at_5"],
            "ndcg_at_5": benchmark_results["ndcg_at_5"],
            "precision_target_met": benchmark_results["precision_met"],
            "ndcg_target_met": benchmark_results["ndcg_met"]
        },
        "cache_performance": {
            "speedup": cache_results["speedup"],
            "time_no_cache": cache_results["time_no_cache"],
            "time_with_cache": cache_results["time_with_cache"]
        },
        "system_performance": {
            "avg_response_time": performance_results["avg_time"],
            "min_response_time": performance_results["min_time"],
            "max_response_time": performance_results["max_time"],
            "target_met": performance_results["target_met"]
        },
        "monitoring": performance_monitor.get_health_status()
    }
    
    # Save report
    report_path = "performance_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 70)
    print("PERFORMANCE REPORT GENERATED")
    print("=" * 70)
    print(f"Report saved to: {report_path}")
    
    return report

def main():
    print("\n🚀 Starting comprehensive performance testing...\n")
    
    # Run all tests
    benchmark_results = run_retrieval_benchmarks()
    cache_results = test_cache_performance()
    performance_results = test_system_performance()
    
    # Generate report
    report = generate_performance_report(
        benchmark_results,
        cache_results,
        performance_results
    )
    
    print("\n✅ All tests complete!\n")
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Retrieval Quality: {'✅ PASS' if benchmark_results['precision_met'] and benchmark_results['ndcg_met'] else '⚠️ NEEDS IMPROVEMENT'}")
    print(f"Cache Performance: ✅ {cache_results['speedup']:.1f}x speedup")
    print(f"System Performance: {'✅ PASS' if performance_results['target_met'] else '❌ FAIL'}")
    print(f"Overall Status: {'✅ HEALTHY' if report['monitoring']['status'] == 'healthy' else '⚠️ ' + report['monitoring']['status'].upper()}")

if __name__ == "__main__":
    main()
