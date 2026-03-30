#!/usr/bin/env python3
"""
Test all API endpoints to verify system functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

def print_test(name, passed, details=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name}")
    if details:
        print(f"     {details}")

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        passed = response.status_code == 200 and response.json().get("status") == "ok"
        print_test("Health Check", passed)
        return passed
    except Exception as e:
        print_test("Health Check", False, str(e))
        return False

def test_contract_analysis():
    """Test contract analysis endpoint"""
    try:
        data = {
            "contract_text": "This agreement is made between Party A and Party B. Party A agrees to provide services for a fee of Rs. 100,000. The agreement shall be governed by Indian law.",
            "jurisdiction": "All-India"
        }
        response = requests.post(f"{BASE_URL}{API_PREFIX}/contracts/analyze", json=data)
        passed = response.status_code == 200
        
        if passed:
            result = response.json()
            details = f"Risk Score: {result.get('overall_risk_score', 'N/A')}, Clauses: {len(result.get('clauses', []))}"
        else:
            details = f"Status: {response.status_code}"
        
        print_test("Contract Analysis", passed, details)
        return passed
    except Exception as e:
        print_test("Contract Analysis", False, str(e))
        return False

def test_case_search():
    """Test case law search endpoint"""
    try:
        data = {
            "case_description": "Contract dispute regarding breach of agreement",
            "jurisdiction": "All-India",
            "top_k": 5
        }
        response = requests.post(f"{BASE_URL}{API_PREFIX}/cases/search", json=data)
        passed = response.status_code == 200
        
        if passed:
            result = response.json()
            details = f"Found {len(result.get('precedents', []))} precedents"
        else:
            details = f"Status: {response.status_code}"
        
        print_test("Case Law Search", passed, details)
        return passed
    except Exception as e:
        print_test("Case Law Search", False, str(e))
        return False

def test_compliance_check():
    """Test compliance checking endpoint"""
    try:
        data = {
            "org_profile": {
                "name": "Test Tech Pvt Ltd",
                "type": "private_company",
                "industry": "technology",
                "size": "50-200",
                "jurisdiction": "All-India"
            },
            "regulations": ["Companies Act 2013", "IT Act 2000"]
        }
        response = requests.post(f"{BASE_URL}{API_PREFIX}/compliance/check", json=data)
        passed = response.status_code == 200
        
        if passed:
            result = response.json()
            report = result.get('report', {})
            details = f"Score: {report.get('compliance_score', 0):.1f}%, Gaps: {len(report.get('gaps', []))}"
        else:
            details = f"Status: {response.status_code}"
        
        print_test("Compliance Check", passed, details)
        return passed
    except Exception as e:
        print_test("Compliance Check", False, str(e))
        return False

def test_dispute_mediation():
    """Test dispute mediation endpoint"""
    try:
        data = {
            "dispute": {
                "parties": ["Party A", "Party B"],
                "narrative": "Property dispute over inherited land. Party A claims 60% ownership based on contribution, Party B claims equal split.",
                "claims": ["Party A claims 60% ownership", "Party B claims equal split"],
                "jurisdiction": "All-India"
            }
        }
        response = requests.post(f"{BASE_URL}{API_PREFIX}/disputes/mediate", json=data)
        passed = response.status_code == 200
        
        if passed:
            result = response.json()
            details = f"Outcomes: {len(result.get('proposed_outcomes', []))}, Precedents: {len(result.get('precedents', []))}"
        else:
            details = f"Status: {response.status_code}"
        
        print_test("Dispute Mediation", passed, details)
        return passed
    except Exception as e:
        print_test("Dispute Mediation", False, str(e))
        return False

def test_qdrant_search():
    """Test Qdrant search endpoint"""
    try:
        data = {
            "query": "fundamental rights",
            "collection": "statutes",
            "jurisdiction": "All-India",
            "top_k": 3
        }
        response = requests.post(f"{BASE_URL}{API_PREFIX}/qdrant/search", json=data)
        passed = response.status_code == 200
        
        if passed:
            result = response.json()
            details = f"Found {len(result.get('results', []))} documents"
        else:
            details = f"Status: {response.status_code}"
        
        print_test("Qdrant Search", passed, details)
        return passed
    except Exception as e:
        print_test("Qdrant Search", False, str(e))
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("LegalGrid API Endpoint Tests")
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Contract Analysis", test_contract_analysis),
        ("Case Law Search", test_case_search),
        ("Compliance Check", test_compliance_check),
        ("Dispute Mediation", test_dispute_mediation),
        ("Qdrant Search", test_qdrant_search),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ FAIL | {name}: {str(e)}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"Passed: {passed_count}/{total_count}")
    print(f"Failed: {total_count - passed_count}/{total_count}")
    print(f"Success Rate: {passed_count/total_count*100:.1f}%")
    print()
    
    if passed_count == total_count:
        print("🎉 All tests passed! System is operational.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
