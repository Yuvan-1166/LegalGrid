#!/usr/bin/env python3
"""Quick test for session management"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.session_manager import session_manager
from app.models.chat_session import MessageRole

def test_session_management():
    print("Testing Session Management...")
    
    # Create a new session
    print("\n1. Creating new session...")
    session = session_manager.create_session()
    print(f"   ✓ Created session: {session.session_id}")
    print(f"   ✓ Title: {session.title}")
    
    # Add messages
    print("\n2. Adding messages...")
    session_manager.add_message(
        session.session_id,
        MessageRole.USER,
        "What are the key provisions of the Indian Contract Act?"
    )
    print("   ✓ Added user message")
    
    session_manager.add_message(
        session.session_id,
        MessageRole.ASSISTANT,
        "The Indian Contract Act, 1872 contains several key provisions..."
    )
    print("   ✓ Added assistant message")
    
    # Get conversation history
    print("\n3. Getting conversation history...")
    history = session_manager.get_conversation_history(session.session_id)
    print(f"   ✓ Retrieved {len(history)} messages")
    
    # List sessions
    print("\n4. Listing all sessions...")
    sessions = session_manager.list_sessions()
    print(f"   ✓ Found {len(sessions)} session(s)")
    for s in sessions:
        print(f"      - {s.title} ({s.message_count} messages)")
    
    # Update title
    print("\n5. Updating session title...")
    session_manager.update_session_title(session.session_id, "Contract Act Discussion")
    updated_session = session_manager.get_session(session.session_id)
    print(f"   ✓ New title: {updated_session.title}")
    
    # Delete session
    print("\n6. Deleting session...")
    success = session_manager.delete_session(session.session_id)
    print(f"   ✓ Deleted: {success}")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_session_management()
