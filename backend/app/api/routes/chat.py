from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from app.core.llm import llm_client
from app.core.session_manager import session_manager
from app.models.chat_session import MessageRole

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    message: str
    session_id: str
    suggestions: Optional[List[str]] = None
    related_actions: Optional[List[Dict[str, str]]] = None

class SessionCreateRequest(BaseModel):
    title: Optional[str] = None

class SessionUpdateRequest(BaseModel):
    title: str

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatMessageRequest):
    try:
        # Get or create session
        if request.session_id:
            session = session_manager.get_session(request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
        else:
            session = session_manager.create_session()
        
        # Add user message to session
        session_manager.add_message(
            session.session_id,
            MessageRole.USER,
            request.message
        )
        
        # Build messages for LLM
        messages = [
            {
                "role": "system",
                "content": "You are an expert AI legal assistant specializing in Indian law. Provide clear, accurate, and helpful responses. Always cite relevant laws when applicable."
            }
        ]
        
        # Get conversation history from session
        history = session_manager.get_conversation_history(session.session_id, max_messages=10)
        messages.extend(history)
        
        # Get response from LLM
        response_content = llm_client.chat(messages, temperature=0.3)
        
        # Add assistant message to session
        session_manager.add_message(
            session.session_id,
            MessageRole.ASSISTANT,
            response_content
        )
        
        # Generate suggestions
        suggestions = generate_suggestions(request.message, response_content)
        
        # Generate related actions
        actions = generate_related_actions(request.message)
        
        return ChatResponse(
            message=response_content,
            session_id=session.session_id,
            suggestions=suggestions,
            related_actions=actions
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_suggestions(user_msg: str, ai_response: str) -> List[str]:
    suggestions = []
    user_lower = user_msg.lower()
    
    if "contract" in user_lower:
        suggestions = [
            "Can you analyze this contract for risks?",
            "What are the key clauses to review?",
            "Are there any compliance issues?"
        ]
    elif "case" in user_lower or "precedent" in user_lower:
        suggestions = [
            "Find similar cases",
            "What are the relevant precedents?",
            "Show me recent judgments"
        ]
    elif "compliance" in user_lower:
        suggestions = [
            "What regulations apply to my business?",
            "How do I ensure compliance?",
            "What are the penalties for non-compliance?"
        ]
    elif "dispute" in user_lower:
        suggestions = [
            "How can this be resolved?",
            "What are my legal options?",
            "Can this be mediated?"
        ]
    else:
        suggestions = [
            "Can you provide more details?",
            "What are the legal implications?",
            "Are there any precedents?"
        ]
    
    return suggestions[:3]

def generate_related_actions(user_msg: str) -> List[Dict[str, str]]:
    actions = []
    user_lower = user_msg.lower()
    
    if "contract" in user_lower:
        actions.append({"label": "Analyze Contract", "link": "/contracts"})
    elif "case" in user_lower or "precedent" in user_lower:
        actions.append({"label": "Search Cases", "link": "/cases"})
    elif "compliance" in user_lower:
        actions.append({"label": "Check Compliance", "link": "/compliance"})
    elif "dispute" in user_lower:
        actions.append({"label": "Mediate Dispute", "link": "/disputes"})
    
    return actions

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    query: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    """Handle document upload and analysis"""
    try:
        # Get or create session
        if session_id:
            session = session_manager.get_session(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
        else:
            session = session_manager.create_session()
        
        # Read file content
        content = await file.read()
        
        # For now, return a simple response
        # In production, you'd process the document here
        response_msg = f"I've received your document '{file.filename}'. {query if query else 'How can I help you analyze it?'}"
        
        # Add to session
        session_manager.add_message(
            session.session_id,
            MessageRole.USER,
            f"[Uploaded: {file.filename}] {query or 'Analyze this document'}"
        )
        session_manager.add_message(
            session.session_id,
            MessageRole.ASSISTANT,
            response_msg
        )
        
        return ChatResponse(
            message=response_msg,
            session_id=session.session_id,
            suggestions=[
                "Analyze this document for risks",
                "Summarize the key points",
                "Check for compliance issues"
            ],
            related_actions=[
                {"label": "Full Analysis", "link": "/contracts"}
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
async def list_sessions(limit: int = 50):
    """List all chat sessions"""
    try:
        sessions = session_manager.list_sessions(limit=limit)
        return {"sessions": [s.dict() for s in sessions]}
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions")
async def create_session(request: SessionCreateRequest):
    """Create a new chat session"""
    try:
        session = session_manager.create_session(title=request.title)
        return {"session_id": session.session_id, "title": session.title}
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a specific session with full history"""
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session.dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session"""
    try:
        success = session_manager.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/sessions/{session_id}/title")
async def update_session_title(session_id: str, request: SessionUpdateRequest):
    """Update session title"""
    try:
        success = session_manager.update_session_title(session_id, request.title)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Title updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating title: {e}")
        raise HTTPException(status_code=500, detail=str(e))

