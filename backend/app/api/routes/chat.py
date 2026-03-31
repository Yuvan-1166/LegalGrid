from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from app.core.llm import llm_client

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    conversation_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    message: str
    suggestions: Optional[List[str]] = None
    related_actions: Optional[List[Dict[str, str]]] = None

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatMessage):
    try:
        # Build messages for LLM
        messages = [
            {
                "role": "system",
                "content": "You are an expert AI legal assistant specializing in Indian law. Provide clear, accurate, and helpful responses. Always cite relevant laws when applicable."
            }
        ]
        
        # Add conversation history
        for msg in request.conversation_history[-5:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Get response from LLM
        response_content = llm_client.chat(messages, temperature=0.3)
        
        # Generate suggestions
        suggestions = generate_suggestions(request.message, response_content)
        
        # Generate related actions
        actions = generate_related_actions(request.message)
        
        return ChatResponse(
            message=response_content,
            suggestions=suggestions,
            related_actions=actions
        )
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
    query: Optional[str] = Form(None)
):
    """Handle document upload and analysis"""
    try:
        # Read file content
        content = await file.read()
        
        # For now, return a simple response
        # In production, you'd process the document here
        return ChatResponse(
            message=f"I've received your document '{file.filename}'. {query if query else 'How can I help you analyze it?'}",
            suggestions=[
                "Analyze this document for risks",
                "Summarize the key points",
                "Check for compliance issues"
            ],
            related_actions=[
                {"label": "Full Analysis", "link": "/contracts"}
            ]
        )
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

