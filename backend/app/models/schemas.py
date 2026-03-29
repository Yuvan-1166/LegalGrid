from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Document Models
class Document(BaseModel):
    doc_id: str
    title: str
    content: str
    doc_type: str
    jurisdiction: str = "All-India"
    year: Optional[int] = None
    tags: List[str] = []

class RetrievedDocument(BaseModel):
    doc_id: str
    title: str
    content: str
    score: float
    semantic_score: Optional[float] = None
    metadata: dict = {}

# Contract Analysis Models
class ContractAnalysisRequest(BaseModel):
    contract_text: str
    jurisdiction: str = "All-India"

class ClauseRisk(BaseModel):
    clause: str
    risk_score: int = Field(..., ge=0, le=100)
    red_flags: List[str] = []
    recommendations: List[str] = []
    relevant_laws: List[RetrievedDocument] = []

class ContractAnalysisResponse(BaseModel):
    contract_id: str
    analysis_date: datetime
    overall_risk_score: int
    clauses: List[ClauseRisk]
    summary: str

# Case Law Models
class CaseLawSearchRequest(BaseModel):
    case_description: str
    jurisdiction: str = "All-India"
    top_k: int = Field(default=5, ge=1, le=20)

class Precedent(BaseModel):
    title: str
    year: int
    court: str
    relevance_score: float
    summary: str
    holding: str
    reason_retrieved: str

class CaseLawSearchResponse(BaseModel):
    query: str
    precedents: List[Precedent]

# Compliance Models
class OrganizationProfile(BaseModel):
    org_type: str
    industry: str
    size: str
    jurisdiction: str

class ComplianceGap(BaseModel):
    regulation: str
    requirement: str
    status: str
    action_items: List[str]

class ComplianceCheckRequest(BaseModel):
    org_profile: OrganizationProfile
    regulations: List[str]

class ComplianceCheckResponse(BaseModel):
    org_profile: OrganizationProfile
    gaps: List[ComplianceGap]
    compliance_score: int

# Dispute Mediation Models
class DisputeDescription(BaseModel):
    parties: List[str]
    narrative: str
    claims: List[str]
    jurisdiction: str = "All-India"

class ProposedOutcome(BaseModel):
    outcome_type: str
    description: str
    rationale: str

class DisputeMediationRequest(BaseModel):
    dispute: DisputeDescription

class DisputeMediationResponse(BaseModel):
    parsed_claims: dict
    precedents: List[RetrievedDocument]
    common_ground: dict
    proposed_outcomes: List[ProposedOutcome]
