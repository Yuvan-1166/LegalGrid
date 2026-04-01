import json
import os
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from pathlib import Path
from app.models.chat_session import ChatSession, ChatMessage, SessionSummary, MessageRole
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages chat sessions with persistent storage"""
    
    def __init__(self, storage_path: str = "data/chat_sessions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[str, ChatSession] = {}
        self.max_cache_size = 50
    
    def create_session(self, title: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        
        if not title:
            title = f"New Conversation - {datetime.utcnow().strftime('%b %d, %Y')}"
        
        session = ChatSession(
            session_id=session_id,
            title=title,
            messages=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self._save_session(session)
        self.cache[session_id] = session
        
        logger.info(f"Created new session: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieve a session by ID"""
        # Check cache first
        if session_id in self.cache:
            return self.cache[session_id]
        
        # Load from disk
        session = self._load_session(session_id)
        if session:
            self.cache[session_id] = session
            self._manage_cache()
        
        return session
    
    def add_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str,
        metadata: Optional[Dict] = None
    ) -> ChatMessage:
        """Add a message to a session"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        message = ChatMessage(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            metadata=metadata
        )
        
        session.messages.append(message)
        session.updated_at = datetime.utcnow()
        
        # Auto-generate title from first user message
        if len(session.messages) == 2 and role == MessageRole.USER:
            session.title = self._generate_title(content)
        
        self._save_session(session)
        
        logger.info(f"Added message to session {session_id}")
        return message
    
    def get_conversation_history(
        self,
        session_id: str,
        max_messages: int = 10
    ) -> List[Dict[str, str]]:
        """Get recent conversation history for LLM context"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        # Get last N messages, excluding system messages
        recent_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in session.messages[-max_messages:]
            if msg.role != MessageRole.SYSTEM
        ]
        
        return recent_messages
    
    def list_sessions(self, limit: int = 50) -> List[SessionSummary]:
        """List all sessions sorted by most recent"""
        sessions = []
        
        for file_path in self.storage_path.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                    last_message = None
                    if data.get('messages'):
                        last_msg = data['messages'][-1]
                        last_message = last_msg['content'][:100]
                    
                    sessions.append(SessionSummary(
                        session_id=data['session_id'],
                        title=data['title'],
                        message_count=len(data.get('messages', [])),
                        last_message=last_message,
                        created_at=datetime.fromisoformat(data['created_at']),
                        updated_at=datetime.fromisoformat(data['updated_at'])
                    ))
            except Exception as e:
                logger.error(f"Error loading session {file_path}: {e}")
        
        # Sort by updated_at descending
        sessions.sort(key=lambda x: x.updated_at, reverse=True)
        
        return sessions[:limit]
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        try:
            file_path = self.storage_path / f"{session_id}.json"
            if file_path.exists():
                file_path.unlink()
            
            if session_id in self.cache:
                del self.cache[session_id]
            
            logger.info(f"Deleted session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False
    
    def update_session_title(self, session_id: str, title: str) -> bool:
        """Update session title"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.title = title
        session.updated_at = datetime.utcnow()
        self._save_session(session)
        
        return True
    
    def clear_old_sessions(self, days: int = 30) -> int:
        """Clear sessions older than specified days"""
        count = 0
        cutoff = datetime.utcnow().timestamp() - (days * 86400)
        
        for file_path in self.storage_path.glob("*.json"):
            try:
                if file_path.stat().st_mtime < cutoff:
                    file_path.unlink()
                    count += 1
            except Exception as e:
                logger.error(f"Error clearing old session {file_path}: {e}")
        
        logger.info(f"Cleared {count} old sessions")
        return count
    
    def _save_session(self, session: ChatSession):
        """Save session to disk"""
        try:
            file_path = self.storage_path / f"{session.session_id}.json"
            with open(file_path, 'w') as f:
                json.dump(session.dict(), f, default=str, indent=2)
        except Exception as e:
            logger.error(f"Error saving session {session.session_id}: {e}")
            raise
    
    def _load_session(self, session_id: str) -> Optional[ChatSession]:
        """Load session from disk"""
        try:
            file_path = self.storage_path / f"{session_id}.json"
            if not file_path.exists():
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                return ChatSession(**data)
        except Exception as e:
            logger.error(f"Error loading session {session_id}: {e}")
            return None
    
    def _generate_title(self, first_message: str) -> str:
        """Generate a title from the first user message"""
        # Take first 50 chars or until first sentence
        title = first_message[:50]
        if '.' in title:
            title = title.split('.')[0]
        if '?' in title:
            title = title.split('?')[0]
        
        return title.strip() + ('...' if len(first_message) > 50 else '')
    
    def _manage_cache(self):
        """Manage cache size using LRU strategy"""
        if len(self.cache) > self.max_cache_size:
            # Remove oldest accessed items
            sorted_items = sorted(
                self.cache.items(),
                key=lambda x: x[1].updated_at
            )
            for session_id, _ in sorted_items[:len(self.cache) - self.max_cache_size]:
                del self.cache[session_id]

# Global session manager instance
session_manager = SessionManager()
