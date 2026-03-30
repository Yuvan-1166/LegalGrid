#!/usr/bin/env python3
"""
Comprehensive system test suite
Tests all features, performance, and quality metrics
"""

import requests
import time
import json
from typing import Dict, List

API_BASE = "http://localhost:8000"
API_V1 = f"{API_BASE}/api/v1"

class ComprehensiveTest:
    def __init__(self):
        self.results = {
            "passed": 0,
            "failed": 0,
            "tests": []
        }
    
    def test(self, name: str, func):
        """Run a test and record result"""
        print(f"\n{'=' * 70}")
        print(f"TEST: {name}")
        print('=' * 70)
        
        try:
            start = time.time()
            result = func()
            duration = time.time() - start
            
            self.results["passed"] += 1
            self.results["tests"].append({
                "name": name,
                "status": "PASS",
                "duration": duration,
                "result": result
            })
            
            print(f"✅ PASS ({duration:.2f}s)")
            return True
            
        except Exception as e:
            self.results["failed"] += 1
            self.results["tests"].append({
                "name": name,
                "status": "FAIL",
                "error": str(e)
            })
            
            print(f"❌ FAIL: {e}")
            return False
    
    def print_summary(self):
        """Print test summary"""
        total = self.results["passed"] + self.results["failed"]
        success_rate = (self.results["passed"] / total * 100) if total > 0 else 0
        
        print(f"\n{'=' * 70}")
        print("TEST SUMMARY")
        print('=' * 70)
        print(f"Total Tests: {total}")
        print(f"Passed: {self.results['passed']} ✅")
        print(f"Failed: {self.results['failed']} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if success_rate == 100:
            print("🎉 ALL TESTS PASSED!")
        elif success_rate >= 80:
            print("⚠️ MOST TESTS PASSED - Some issues need attention")
        else:
            print("❌ MULTIPLE FAILURES - System needs fixes")

# Test functions
def test_health():
    """Test health endpoint"""
    response = requests.get(f"{API_BASE}/health", timeout=5)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    return "Health check OK"

def test_contract_analysis():
    """Test contract analysis"""
    response = requests.post(
        f"{API_V1}/contracts/analyze",
        json={
            "contract_text": "This Service Agreement is entered into between Company A and Company B. Company A agrees to provide services for a fee of $10,000. The agreement shall be governed by Indian law. Either party may terminate with 30 days notice.",
            "jurisdiction": "All-India"
        },
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_risk_score" in data
    assert "clauses" in data
    assert len(data["clauses"]) > 0
    return f"Risk Score: {data['overall_risk_score']}, Clauses: {len(data['clauses'])}"

def test_case_search():
    """Test case law search"""
    response = requests.post(
        f"{API_V1}/cases/search",
        json={
            "query": "fundamental rights and equality",
            "jurisdiction": "All-India",
            "top_k": 5
        },
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert "precedents" in data
    assert len(data["precedents"]) > 0
    return f"Found {len(data['precedents'])} precedents"

def test_compliance_check():
    """Test compliance checking"""
    response = requests.post(
        f"{API_V1}/compliance/check",
        json={
            "org_name": "Test Company",
            "org_type": "private_company",
            "industry": "technology",
            "size": "51-200",
            "jurisdiction": "All-India",
            "regulations": ["Companies Act 2013"]
        },
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert "compliance_score" in data
    assert "gaps" in data
    return f"Compliance Score: {data['compliance_score']}%"

def test_dispute_mediation():
    """Test dispute mediation"""
    response = requests.post(
        f"{API_V1}/disputes/mediate",
        json={
            "parties": ["Party A", "Party B"],
            "narrative": "Business partnership dispute over profit sharing",
            "claims": ["Party A claims 60% share", "Party B claims 60% share"],
            "jurisdiction": "All-India"
        },
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert "proposed_outcomes" in data
    assert len(data["proposed_outcomes"]) > 0
    return f"Generated {len(data['proposed_outcomes'])} outcomes"

def test_qdrant_search():
    """Test Qdrant search"""
    response = requests.post(
        f"{API_V1}/qdrant/search",
        json={
            "query": "murder and homicide",
            "collection": "statutes",
            "jurisdiction": "All-India",
            "top_k": 3
        },
        timeout=30
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    return f"Found {len(data['results'])} documents"

def test_response_times():
    """Test response time performance"""
    queries = [
        ("contract breach", "statutes"),
        ("privacy rights", "cases"),
        ("fraud laws", "statutes")
    ]
    
    times = []
    for query, collection in queries:
        start = time.time()
        response = requests.post(
            f"{API_V1}/qdrant/search",
            json={
                "query": query,
                "collection": collection,
                "top_k": 5
            },
            timeout=30
        )
        duration = time.time() - start
        times.append(duration)
        assert response.status_code == 200
    
    avg_time = sum(times) / len(times)
    assert avg_time < 3, f"Average response time {avg_time:.2f}s exceeds 3s target"
    
    return f"Avg: {avg_time:.2f}s, Max: {max(times):.2f}s"

def test_cache_effectiveness():
    """Test caching effectiveness"""
    query = "contract enforceability"
    
    # First query (no cache)
    start = time.time()
    response1 = requests.post(
        f"{API_V1}/qdrant/search",
        json={"query": query, "collection": "statutes", "top_k": 5},
        timeout=30
    )
    time1 = time.time() - start
    
    # Second query (should be cached)
    start = time.time()
    response2 = requests.post(
        f"{API_V1}/qdrant/search",
        json={"query": query, "collection": "statutes", "top_k": 5},
        timeout=30
    )
    time2 = time.time() - start
    
    speedup = time1 / time2 if time2 > 0 else 1
    
    return f"Speedup: {speedup:.1f}x (First: {time1:.3f}s, Cached: {time2:.3f}s)"

def test_input_validation():
    """Test input validation"""
    # Test with invalid input (too short)
    response = requests.post(
        f"{API_V1}/contracts/analyze",
        json={
            "contract_text": "Short",
            "jurisdiction": "All-India"
        },
        timeout=10
    )
    
    # Should return 422 (validation error)
    assert response.status_code == 422, "Should reject short contract text"
    
    return "Validation working correctly"

def main():
    print("\n" + "=" * 70)
    print("LEGALGRID COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"Testing: {API_BASE}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = ComprehensiveTest()
    
    # Run all tests
    tester.test("Health Check", test_health)
    tester.test("Contract Analysis", test_contract_analysis)
    tester.test("Case Law Search", test_case_search)
    tester.test("Compliance Check", test_compliance_check)
    tester.test("Dispute Mediation", test_dispute_mediation)
    tester.test("Qdrant Search", test_qdrant_search)
    tester.test("Response Time Performance", test_response_times)
    tester.test("Cache Effectiveness", test_cache_effectiveness)
    tester.test("Input Validation", test_input_validation)
    
    # Print summary
    tester.print_summary()
    
    # Save results
    with open("test_results.json", "w") as f:
        json.dump(tester.results, f, indent=2)
    
    print(f"\nResults saved to: test_results.json")

if __name__ == "__main__":
    main()
