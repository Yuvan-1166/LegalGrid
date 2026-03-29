"""API routes for compliance checking"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ComplianceCheckRequest,
    ComplianceCheckResponse
)
from app.agents.compliance_agent import compliance_agent

router = APIRouter(prefix="/compliance", tags=["compliance"])

@router.post("/check", response_model=ComplianceCheckResponse)
async def check_compliance(request: ComplianceCheckRequest):
    """
    Check organization compliance against specified regulations
    
    Args:
        request: Compliance check request with org profile and regulations
        
    Returns:
        Compliance report with gaps and recommendations
    """
    try:
        # Convert org_profile to dict
        org_profile_dict = request.org_profile.model_dump()
        
        # Check compliance
        report = compliance_agent.check_compliance(
            org_profile=org_profile_dict,
            regulations=request.regulations
        )
        
        return ComplianceCheckResponse(report=report)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Compliance check failed: {str(e)}"
        )

@router.get("/detect-changes/{regulation}")
async def detect_regulatory_changes(
    regulation: str,
    last_check_date: str = None
):
    """
    Detect if a regulation has changed since last check
    
    Args:
        regulation: Name of regulation to check
        last_check_date: ISO format date of last check (optional)
        
    Returns:
        Change detection report
    """
    try:
        result = compliance_agent.detect_regulatory_changes(
            regulation=regulation,
            last_check_date=last_check_date
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Change detection failed: {str(e)}"
        )
