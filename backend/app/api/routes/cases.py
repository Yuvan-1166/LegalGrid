"""API routes for case law search"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import CaseLawSearchRequest, CaseLawSearchResponse
from app.agents.case_law_agent import case_law_agent
from typing import Dict

router = APIRouter(prefix="/cases", tags=["cases"])

@router.post("/search", response_model=CaseLawSearchResponse)
async def search_precedents(request: CaseLawSearchRequest):
    """
    Search for relevant legal precedents
    
    Args:
        request: Case description and search parameters
        
    Returns:
        List of relevant precedents with rankings
    """
    try:
        # Find precedents
        precedents = case_law_agent.find_precedents(
            case_description=request.case_description,
            jurisdiction=request.jurisdiction,
            top_k=request.top_k
        )
        
        return CaseLawSearchResponse(
            query=request.case_description,
            precedents=precedents
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-strength")
async def analyze_precedent_strength(request: CaseLawSearchRequest) -> Dict:
    """
    Analyze the strength of precedents for a case
    
    Returns:
        Analysis of precedent strength and recommendations
    """
    try:
        # Find precedents
        precedents = case_law_agent.find_precedents(
            case_description=request.case_description,
            jurisdiction=request.jurisdiction,
            top_k=request.top_k
        )
        
        # Analyze strength
        analysis = case_law_agent.analyze_precedent_strength(precedents)
        
        return {
            "query": request.case_description,
            "precedents_found": len(precedents),
            "analysis": analysis,
            "top_precedents": [
                {
                    "title": p.title,
                    "court": p.court,
                    "year": p.year,
                    "relevance": p.relevance_score
                }
                for p in precedents[:3]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
