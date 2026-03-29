"""Compliance Monitoring Agent for regulatory compliance checking"""

from typing import List, Dict, Optional
from datetime import datetime
from app.core.llm import llm_client
from app.rag.hybrid_retriever import hybrid_retriever
from app.models.schemas import ComplianceGap, ComplianceReport
import json

class ComplianceAgent:
    def __init__(self):
        self.llm = llm_client
        self.retriever = hybrid_retriever
    
    def check_compliance(
        self,
        org_profile: Dict,
        regulations: List[str]
    ) -> ComplianceReport:
        """
        Check organization compliance against specified regulations
        
        Args:
            org_profile: Organization details (type, industry, size, jurisdiction)
            regulations: List of regulations to check against
            
        Returns:
            Compliance report with gaps and recommendations
        """
        gaps = []
        compliant_items = []
        
        for regulation in regulations:
            # Retrieve regulation documents
            reg_docs = self.retriever.retrieve(
                query=regulation,
                collection="regulations",
                top_k=3,
                use_hybrid=True
            )
            
            if not reg_docs:
                # Try statutes collection if no regulations found
                reg_docs = self.retriever.retrieve(
                    query=regulation,
                    collection="statutes",
                    top_k=3,
                    use_hybrid=True
                )
            
            # Extract requirements from regulation
            requirements = self._extract_requirements(regulation, reg_docs, org_profile)
            
            # Evaluate compliance for each requirement
            for req in requirements:
                is_compliant, confidence = self._evaluate_compliance(org_profile, req, reg_docs)
                
                if not is_compliant:
                    gap = ComplianceGap(
                        regulation=regulation,
                        requirement=req["requirement"],
                        status="NON_COMPLIANT",
                        severity=req.get("severity", "medium"),
                        action_items=self._suggest_remediation(req, org_profile),
                        deadline=req.get("deadline", "Not specified"),
                        confidence=confidence
                    )
                    gaps.append(gap)
                else:
                    compliant_items.append({
                        "regulation": regulation,
                        "requirement": req["requirement"],
                        "status": "COMPLIANT"
                    })
        
        # Generate overall assessment
        total_checks = len(gaps) + len(compliant_items)
        compliance_score = (len(compliant_items) / total_checks * 100) if total_checks > 0 else 0
        
        return ComplianceReport(
            organization=org_profile.get("name", "Organization"),
            compliance_score=round(compliance_score, 1),
            total_checks=total_checks,
            gaps=gaps,
            compliant_count=len(compliant_items),
            checked_at=datetime.now().isoformat()
        )
    
    def _extract_requirements(
        self,
        regulation: str,
        docs: List[Dict],
        org_profile: Dict
    ) -> List[Dict]:
        """Extract compliance requirements from regulation documents"""
        if not docs:
            return [{
                "requirement": f"Unable to retrieve details for {regulation}",
                "applicability": "Unknown",
                "severity": "low"
            }]
        
        # Combine document content
        context = "\n\n".join([doc.get("content", "")[:500] for doc in docs[:2]])
        
        prompt = f"""Extract key compliance requirements from this regulation that apply to the organization.

Regulation: {regulation}

Organization Profile:
- Type: {org_profile.get('type', 'Unknown')}
- Industry: {org_profile.get('industry', 'Unknown')}
- Size: {org_profile.get('size', 'Unknown')}
- Jurisdiction: {org_profile.get('jurisdiction', 'Unknown')}

Regulation Text:
{context}

Return a JSON array of requirements in this format:
[{{
  "requirement": "Brief description of what must be done",
  "applicability": "Who this applies to",
  "severity": "high/medium/low",
  "deadline": "When it must be done (if specified)"
}}]

Return only the JSON array, no other text."""

        try:
            response = self.llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            requirements = json.loads(content)
            return requirements if isinstance(requirements, list) else [requirements]
            
        except Exception as e:
            # Fallback: create generic requirement
            return [{
                "requirement": f"Comply with {regulation} requirements",
                "applicability": "All organizations",
                "severity": "medium",
                "deadline": "Ongoing"
            }]
    
    def _evaluate_compliance(
        self,
        org_profile: Dict,
        requirement: Dict,
        reg_docs: List[Dict]
    ) -> tuple[bool, float]:
        """
        Evaluate if organization complies with requirement
        
        Returns:
            (is_compliant, confidence_score)
        """
        prompt = f"""Evaluate if this organization likely complies with the requirement.

Organization Profile:
- Type: {org_profile.get('type', 'Unknown')}
- Industry: {org_profile.get('industry', 'Unknown')}
- Size: {org_profile.get('size', 'Unknown')}
- Jurisdiction: {org_profile.get('jurisdiction', 'Unknown')}

Requirement: {requirement['requirement']}
Applicability: {requirement.get('applicability', 'General')}

Based on typical compliance patterns, does this organization likely comply?

Respond in this exact format:
COMPLIANT: YES/NO
CONFIDENCE: 0.0-1.0
REASON: Brief explanation"""

        try:
            response = self.llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse response
            is_compliant = "YES" in content.split("\n")[0].upper()
            
            # Extract confidence
            confidence = 0.5
            for line in content.split("\n"):
                if "CONFIDENCE:" in line.upper():
                    try:
                        confidence = float(line.split(":")[-1].strip())
                    except:
                        pass
            
            return is_compliant, confidence
            
        except Exception as e:
            # Conservative: assume non-compliant if we can't determine
            return False, 0.3
    
    def _suggest_remediation(
        self,
        requirement: Dict,
        org_profile: Dict
    ) -> List[str]:
        """Generate actionable remediation steps"""
        prompt = f"""Suggest 3-5 specific action items to achieve compliance with this requirement.

Requirement: {requirement['requirement']}
Organization Type: {org_profile.get('type', 'Unknown')}
Industry: {org_profile.get('industry', 'Unknown')}

Provide practical, actionable steps. Return as a JSON array of strings.
Example: ["Step 1", "Step 2", "Step 3"]

Return only the JSON array, no other text."""

        try:
            response = self.llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            action_items = json.loads(content)
            return action_items if isinstance(action_items, list) else [str(action_items)]
            
        except Exception as e:
            # Fallback actions
            return [
                f"Review {requirement['requirement']} in detail",
                "Consult with legal counsel",
                "Implement necessary changes",
                "Document compliance measures"
            ]
    
    def detect_regulatory_changes(
        self,
        regulation: str,
        last_check_date: Optional[str] = None
    ) -> Dict:
        """
        Detect if regulation has changed since last check
        
        Args:
            regulation: Name of regulation to check
            last_check_date: ISO format date of last check
            
        Returns:
            Change detection report
        """
        # Retrieve current regulation documents
        current_docs = self.retriever.retrieve(
            query=regulation,
            collection="regulations",
            top_k=3,
            use_hybrid=True
        )
        
        if not current_docs:
            return {
                "regulation": regulation,
                "changed": False,
                "confidence": 0.0,
                "message": "Unable to retrieve regulation documents"
            }
        
        # Check metadata for update dates
        latest_update = None
        for doc in current_docs:
            doc_date = doc.get("metadata", {}).get("updated_at")
            if doc_date:
                if not latest_update or doc_date > latest_update:
                    latest_update = doc_date
        
        changed = False
        if last_check_date and latest_update:
            changed = latest_update > last_check_date
        
        return {
            "regulation": regulation,
            "changed": changed,
            "last_updated": latest_update,
            "last_checked": last_check_date,
            "confidence": 0.8 if latest_update else 0.3,
            "message": "Changes detected" if changed else "No changes detected"
        }

# Global agent instance
compliance_agent = ComplianceAgent()
