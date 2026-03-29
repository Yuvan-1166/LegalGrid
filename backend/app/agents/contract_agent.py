from typing import List, Dict
from app.core.llm import llm_client
from app.rag.retriever import retriever
from app.models.schemas import ClauseRisk, ContractAnalysisResponse
from datetime import datetime
import uuid

class ContractAnalysisAgent:
    def __init__(self):
        self.llm = llm_client
        self.retriever = retriever
    
    def analyze(self, contract_text: str, jurisdiction: str = "All-India") -> ContractAnalysisResponse:
        """Analyze contract for risks and compliance"""
        # Step 1: Extract clauses
        clauses = self._extract_clauses(contract_text)
        
        # Step 2: Analyze each clause
        clause_risks = []
        for clause in clauses:
            risk = self._analyze_clause(clause, jurisdiction)
            clause_risks.append(risk)
        
        # Step 3: Calculate overall risk
        overall_risk = self._calculate_overall_risk(clause_risks)
        
        # Step 4: Generate summary
        summary = self._generate_summary(clause_risks, overall_risk)
        
        return ContractAnalysisResponse(
            contract_id=str(uuid.uuid4()),
            analysis_date=datetime.now(),
            overall_risk_score=overall_risk,
            clauses=clause_risks,
            summary=summary
        )
    
    def _extract_clauses(self, contract_text: str) -> List[str]:
        """Extract major clauses from contract"""
        prompt = f"""Extract the major clauses from this contract. Return as a JSON array of strings.
Each clause should be a distinct section (e.g., "Payment Terms", "Liability", "Termination").

Contract:
{contract_text[:2000]}

Return format: {{"clauses": ["clause 1 text", "clause 2 text", ...]}}
"""
        response = self.llm.chat([{"role": "user", "content": prompt}], temperature=0.1)
        
        try:
            data = self.llm.extract_json(response)
            return data.get("clauses", [contract_text[:500]])  # Fallback to first 500 chars
        except:
            # Fallback: split by paragraphs
            return [p.strip() for p in contract_text.split('\n\n') if len(p.strip()) > 50][:5]
    
    def _analyze_clause(self, clause: str, jurisdiction: str) -> ClauseRisk:
        """Analyze individual clause for risks"""
        # Retrieve relevant laws
        relevant_laws = self.retriever.retrieve(
            query=clause,
            collection="statutes",
            jurisdiction=jurisdiction,
            top_k=3
        )
        
        # Analyze with LLM
        laws_context = "\n".join([
            f"- {doc['title']}: {doc['content'][:200]}"
            for doc in relevant_laws
        ])
        
        prompt = f"""Analyze this contract clause for legal risks under Indian law.

Clause:
{clause}

Relevant Laws:
{laws_context}

Provide:
1. Risk score (0-100, where 0=no risk, 100=high risk)
2. Red flags (list of specific issues)
3. Recommendations (list of suggested changes)

Return as JSON: {{
    "risk_score": 0-100,
    "red_flags": ["flag1", "flag2"],
    "recommendations": ["rec1", "rec2"]
}}
"""
        response = self.llm.chat([{"role": "user", "content": prompt}], temperature=0.1)
        
        try:
            data = self.llm.extract_json(response)
            return ClauseRisk(
                clause=clause[:200] + "..." if len(clause) > 200 else clause,
                risk_score=data.get("risk_score", 50),
                red_flags=data.get("red_flags", []),
                recommendations=data.get("recommendations", []),
                relevant_laws=[{
                    "doc_id": doc["doc_id"],
                    "title": doc["title"],
                    "content": doc["content"],
                    "score": doc["score"],
                    "metadata": doc["metadata"]
                } for doc in relevant_laws]
            )
        except Exception as e:
            return ClauseRisk(
                clause=clause[:200],
                risk_score=50,
                red_flags=["Unable to analyze clause"],
                recommendations=["Manual review recommended"],
                relevant_laws=[]
            )
    
    def _calculate_overall_risk(self, clause_risks: List[ClauseRisk]) -> int:
        """Calculate overall contract risk score"""
        if not clause_risks:
            return 50
        return int(sum(c.risk_score for c in clause_risks) / len(clause_risks))
    
    def _generate_summary(self, clause_risks: List[ClauseRisk], overall_risk: int) -> str:
        """Generate contract analysis summary"""
        high_risk_clauses = [c for c in clause_risks if c.risk_score > 70]
        
        if overall_risk > 70:
            risk_level = "HIGH"
        elif overall_risk > 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        summary = f"Overall Risk: {risk_level} ({overall_risk}/100). "
        
        if high_risk_clauses:
            summary += f"Found {len(high_risk_clauses)} high-risk clause(s). "
        
        summary += "Review recommendations for each clause."
        
        return summary

# Global agent instance
contract_agent = ContractAnalysisAgent()
