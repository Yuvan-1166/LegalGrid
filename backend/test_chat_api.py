#!/usr/bin/env python3
"""Test chat API endpoints with session management"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1/chat"

def test_chat_api():
    print("Testing Chat API with Session Management...\n")
    
    # Test 1: Create a new session
    print("1. Creating new session...")
    response = requests.post(f"{BASE_URL}/sessions", json={"title": "Test Session"})
    if response.status_code == 200:
        session_data = response.json()
        session_id = session_data['session_id']
        print(f"   ✓ Session created: {session_id}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return
    
    # Test 2: Send a message
    print("\n2. Sending message to session...")
    response = requests.post(f"{BASE_URL}/message", json={
        "message": "What is the Indian Contract Act?",
        "session_id": session_id
    })
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Response received")
        print(f"   ✓ Message: {data['message'][:100]}...")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        return
    
    # Test 3: Send another message
    print("\n3. Sending follow-up message...")
    response = requests.post(f"{BASE_URL}/message", json={
        "message": "Can you explain section 10?",
        "session_id": session_id
    })
    if response.status_code == 200:
        print("   ✓ Follow-up response received")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    # Test 4: List sessions
    print("\n4. Listing all sessions...")
    response = requests.get(f"{BASE_URL}/sessions")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Found {len(data['sessions'])} session(s)")
        for s in data['sessions']:
            print(f"      - {s['title']} ({s['message_count']} messages)")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    # Test 5: Get specific session
    print("\n5. Getting session details...")
    response = requests.get(f"{BASE_URL}/sessions/{session_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Session has {len(data['messages'])} messages")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    # Test 6: Update title
    print("\n6. Updating session title...")
    response = requests.patch(f"{BASE_URL}/sessions/{session_id}/title", json={
        "title": "Contract Act Discussion"
    })
    if response.status_code == 200:
        print("   ✓ Title updated")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    # Test 7: Delete session
    print("\n7. Deleting session...")
    response = requests.delete(f"{BASE_URL}/sessions/{session_id}")
    if response.status_code == 200:
        print("   ✓ Session deleted")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    print("\n✅ All API tests completed!")

if __name__ == "__main__":
    print("Make sure the backend server is running on http://localhost:8000")
    print("Run: cd backend && source .venv/bin/activate && python main.py\n")
    
    try:
        test_chat_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend server")
        print("Please start the server first: cd backend && source .venv/bin/activate && python main.py")
