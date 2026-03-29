"""Quick test script to verify all 4 agents are working"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.status_code == 200

def test_contract_analysis():
    """Test contract analysis agent"""
    print("\n2. Testing Contract Analysis Agent...")
    data = {
        "contract_text": "This agreement is made between Party A and Party B. Party A shall pay Rs. 100,000 to Party B. The agreement is valid for 1 year.",
        "jurisdiction": "All-India"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contracts/analyze", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Risk Score: {result.get('overall_risk_score', 'N/A')}")
        print(f"   Clauses Found: {len(result.get('clauses', []))}")
    else:
        print(f"   Error: {response.text}")
    return response.status_code == 200

def test_case_law_search():
    """Test case law agent"""
    print("\n3. Testing Case Law Search Agent...")
    data = {
        "case_description": "Employment contract termination without notice",
        "jurisdiction": "All-India",
        "top_k": 3
    }
    response = requests.post(f"{BASE_URL}/api/v1/cases/search", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Precedents Found: {len(result.get('precedents', []))}")
        if result.get('precedents'):
            print(f"   Top Result: {result['precedents'][0].get('title', 'N/A')}")
    else:
        print(f"   Error: {response.text}")
    return response.status_code == 200

def test_compliance_check():
    """Test compliance agent"""
    print("\n4. Testing Compliance Agent...")
    data = {
        "org_profile": {
            "name": "Test Company",
            "type": "private_company",
            "industry": "technology",
            "size": "50-200",
            "jurisdiction": "All-India"
        },
        "regulations": ["Companies Act 2013", "GST Act 2017"]
    }
    response = requests.post(f"{BASE_URL}/api/v1/compliance/check", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        report = result.get('report', {})
        print(f"   Compliance Score: {report.get('compliance_score', 'N/A')}%")
        print(f"   Gaps Found: {len(report.get('gaps', []))}")
    else:
        print(f"   Error: {response.text}")
    return response.status_code == 200

def test_dispute_mediation():
    """Test mediation agent"""
    print("\n5. Testing Dispute Mediation Agent...")
    data = {
        "dispute": {
            "parties": ["Party A", "Party B"],
            "narrative": "Property dispute over inherited land. Party A claims 60% ownership, Party B claims equal split.",
            "claims": [
                "Party A contributed more to property maintenance",
                "Party B claims equal inheritance rights"
            ],
            "jurisdiction": "All-India"
        }
    }
    response = requests.post(f"{BASE_URL}/api/v1/disputes/mediate", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Parsed Claims: {len(result.get('parsed_claims', {}))}")
        print(f"   Proposed Outcomes: {len(result.get('proposed_outcomes', []))}")
    else:
        print(f"   Error: {response.text}")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 60)
    print("LegalGrid - All Agents Test Suite")
    print("=" * 60)
    
    results = {
        "Health Check": test_health(),
        "Contract Analysis": test_contract_analysis(),
        "Case Law Search": test_case_law_search(),
        "Compliance Check": test_compliance_check(),
        "Dispute Mediation": test_dispute_mediation()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All agents are working correctly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")

if __name__ == "__main__":
    main()
