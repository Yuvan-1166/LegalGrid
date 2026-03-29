from fastapi import APIRouter, HTTPException
from app.rag.retriever import retriever
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/qdrant", tags=["qdrant"])

class InitializeRequest(BaseModel):
    pass

class AddDocumentRequest(BaseModel):
    doc_id: str
    title: str
    content: str
    collection: str
    jurisdiction: str = "All-India"
    metadata: dict = {}

class SearchRequest(BaseModel):
    query: str
    collection: str
    jurisdiction: str = "All-India"
    top_k: int = 5

@router.post("/initialize")
async def initialize_collections():
    """Initialize Qdrant collections"""
    try:
        retriever.initialize_collections()
        return {"message": "Collections initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-document")
async def add_document(request: AddDocumentRequest):
    """Add document to vector database"""
    try:
        retriever.add_document(
            doc_id=request.doc_id,
            title=request.title,
            content=request.content,
            collection=request.collection,
            jurisdiction=request.jurisdiction,
            metadata=request.metadata
        )
        return {"message": "Document added successfully", "doc_id": request.doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_documents(request: SearchRequest):
    """Search for relevant documents"""
    try:
        results = retriever.retrieve(
            query=request.query,
            collection=request.collection,
            jurisdiction=request.jurisdiction,
            top_k=request.top_k
        )
        return {"query": request.query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-cache")
async def clear_cache():
    """Clear retrieval cache"""
    try:
        retriever.clear_cache()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
