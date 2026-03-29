"""API routes for dispute mediation"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    DisputeMediationRequest,
    DisputeMediationResponse
)
from app.agents.mediation_agent import mediation_agent

router = APIRouter(prefix="/disputes", tags=["disputes"])

@router.post("/mediate", response_model=DisputeMediationResponse)
async def mediate_dispute(request: DisputeMediationRequest):
    """
    Mediate a dispute between multiple parties
    
    Args:
        request: Dispute mediation request with parties, narrative, and claims
        
    Returns:
        Mediation report with parsed claims, precedents, and proposed outcomes
    """
    try:
        result = mediation_agent.mediate(
            parties=request.dispute.parties,
            narrative=request.dispute.narrative,
            claims=request.dispute.claims,
            jurisdiction=request.dispute.jurisdiction
        )
        
        return DisputeMediationResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Mediation failed: {str(e)}"
        )

@router.post("/evaluate-outcome")
async def evaluate_outcome(
    outcome_description: str,
    outcome_rationale: str,
    parsed_claims: dict
):
    """
    Evaluate the fairness of a proposed outcome
    
    Args:
        outcome_description: Description of the proposed outcome
        outcome_rationale: Rationale for the outcome
        parsed_claims: Parsed claims by party
        
    Returns:
        Fairness evaluation scores
    """
    try:
        from app.models.schemas import ProposedOutcome
        
        outcome = ProposedOutcome(
            outcome_type="custom",
            description=outcome_description,
            rationale=outcome_rationale
        )
        
        evaluation = mediation_agent.evaluate_fairness(
            outcome=outcome,
            parsed_claims=parsed_claims
        )
        
        return evaluation
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}"
        )
