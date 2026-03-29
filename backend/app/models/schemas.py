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
    name: Optional[str] = "Organization"
    type: str = Field(..., description="e.g., private_company, public_company, startup")
    industry: str = Field(..., description="e.g., technology, manufacturing, finance")
    size: str = Field(..., description="e.g., 1-50, 50-200, 200+ employees")
    jurisdiction: str = Field(default="All-India")

class ComplianceGap(BaseModel):
    regulation: str
    requirement: str
    status: str
    severity: str = Field(default="medium", description="high, medium, or low")
    action_items: List[str]
    deadline: str = Field(default="Not specified")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

class ComplianceReport(BaseModel):
    organization: str
    compliance_score: float
    total_checks: int
    gaps: List[ComplianceGap]
    compliant_count: int
    checked_at: str

class ComplianceCheckRequest(BaseModel):
    org_profile: OrganizationProfile
    regulations: List[str] = Field(..., description="List of regulations to check")

class ComplianceCheckResponse(BaseModel):
    report: ComplianceReport

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
