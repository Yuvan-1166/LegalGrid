"""
Input validation utilities
Ensures data quality and security
"""

from pydantic import BaseModel, validator, Field
from typing import Optional, List
import re

class ContractAnalysisInput(BaseModel):
    """Validated input for contract analysis"""
    contract_text: str = Field(..., min_length=100, max_length=50000)
    jurisdiction: str = Field(default="All-India")
    
    @validator('contract_text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Contract text cannot be empty")
        
        # Remove excessive whitespace
        v = re.sub(r'\s+', ' ', v.strip())
        
        if len(v) < 100:
            raise ValueError("Contract text too short (minimum 100 characters)")
        
        if len(v) > 50000:
            raise ValueError("Contract text too long (maximum 50,000 characters)")
        
        return v
    
    @validator('jurisdiction')
    def validate_jurisdiction(cls, v):
        valid_jurisdictions = [
            "All-India", "Delhi", "Mumbai", "Bangalore", 
            "Chennai", "Kolkata", "Hyderabad"
        ]
        if v not in valid_jurisdictions:
            raise ValueError(f"Invalid jurisdiction. Must be one of: {', '.join(valid_jurisdictions)}")
        return v

class CaseSearchInput(BaseModel):
    """Validated input for case law search"""
    query: str = Field(..., min_length=10, max_length=500)
    jurisdiction: str = Field(default="All-India")
    top_k: int = Field(default=5, ge=1, le=20)
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        
        v = v.strip()
        
        if len(v) < 10:
            raise ValueError("Query too short (minimum 10 characters)")
        
        if len(v) > 500:
            raise ValueError("Query too long (maximum 500 characters)")
        
        return v

class ComplianceCheckInput(BaseModel):
    """Validated input for compliance checking"""
    org_name: str = Field(..., min_length=2, max_length=200)
    org_type: str
    industry: str
    size: str
    jurisdiction: str = Field(default="All-India")
    regulations: List[str] = Field(..., min_items=1, max_items=10)
    
    @validator('org_type')
    def validate_org_type(cls, v):
        valid_types = [
            "private_company", "public_company", "partnership",
            "sole_proprietorship", "llp", "ngo", "startup"
        ]
        if v not in valid_types:
            raise ValueError(f"Invalid organization type. Must be one of: {', '.join(valid_types)}")
        return v
    
    @validator('size')
    def validate_size(cls, v):
        valid_sizes = [
            "1-10", "11-50", "51-200", "201-500", 
            "501-1000", "1000+"
        ]
        if v not in valid_sizes:
            raise ValueError(f"Invalid size. Must be one of: {', '.join(valid_sizes)}")
        return v
    
    @validator('regulations')
    def validate_regulations(cls, v):
        if not v:
            raise ValueError("At least one regulation must be specified")
        
        # Remove duplicates
        v = list(set(v))
        
        if len(v) > 10:
            raise ValueError("Maximum 10 regulations can be checked at once")
        
        return v

class DisputeMediationInput(BaseModel):
    """Validated input for dispute mediation"""
    parties: List[str] = Field(..., min_items=2, max_items=5)
    narrative: str = Field(..., min_length=50, max_length=5000)
    claims: List[str] = Field(..., min_items=1, max_items=20)
    jurisdiction: str = Field(default="All-India")
    
    @validator('parties')
    def validate_parties(cls, v):
        if len(v) < 2:
            raise ValueError("At least 2 parties required for mediation")
        
        if len(v) > 5:
            raise ValueError("Maximum 5 parties supported")
        
        # Remove duplicates
        v = list(set(v))
        
        return v
    
    @validator('narrative')
    def validate_narrative(cls, v):
        if not v or not v.strip():
            raise ValueError("Narrative cannot be empty")
        
        v = v.strip()
        
        if len(v) < 50:
            raise ValueError("Narrative too short (minimum 50 characters)")
        
        if len(v) > 5000:
            raise ValueError("Narrative too long (maximum 5,000 characters)")
        
        return v
