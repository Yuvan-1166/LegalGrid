"""Dispute Mediation Agent for AI-powered conflict resolution"""

from typing import List, Dict
from app.core.llm import llm_client
from app.rag.hybrid_retriever import hybrid_retriever
from app.models.schemas import ProposedOutcome, RetrievedDocument
import json

class MediationAgent:
    def __init__(self):
        self.llm = llm_client
        self.retriever = hybrid_retriever
    
    def mediate(
        self,
        parties: List[str],
        narrative: str,
        claims: List[str],
        jurisdiction: str = "All-India"
    ) -> Dict:
        """
        Mediate a dispute between multiple parties
        
        Args:
            parties: List of party names
            narrative: Description of the dispute
            claims: List of claims made
            jurisdiction: Legal jurisdiction
            
        Returns:
            Mediation report with parsed claims, precedents, and outcomes
        """
        # Step 1: Parse and structure claims
        parsed_claims = self._parse_claims(parties, narrative, claims)
        
        # Step 2: Retrieve relevant case law and precedents with citations
        precedents = self.retriever.retrieve(
            query=narrative,
            collection="cases",
            jurisdiction=jurisdiction,
            top_k=5,
            use_hybrid=True
        )
        
        # Convert to RetrievedDocument format with citations
        precedent_docs = []
        for i, prec in enumerate(precedents):
            metadata = prec.get("metadata", {})
            citation = f"[{i+1}] {prec.get('title', 'Unknown')} ({metadata.get('year', 'N/A')})"
            metadata["citation"] = citation
            
            precedent_docs.append(RetrievedDocument(
                doc_id=prec.get("id", "unknown"),
                title=prec.get("title", "Unknown Case"),
                content=prec.get("content", "")[:500],
                score=prec.get("fusion_score", prec.get("score", 0.5)),
                metadata=metadata
            ))
        
        # Step 3: Identify common ground and conflicts
        common_ground = self._find_common_ground(parsed_claims)
        
        # Step 4: Generate fair outcomes
        outcomes = self._generate_fair_outcomes(
            parsed_claims,
            common_ground,
            precedent_docs,
            narrative
        )
        
        return {
            "parsed_claims": parsed_claims,
            "precedents": precedent_docs,
            "common_ground": common_ground,
            "proposed_outcomes": outcomes
        }
    
    def _parse_claims(
        self,
        parties: List[str],
        narrative: str,
        claims: List[str]
    ) -> Dict:
        """Parse and structure claims by party"""
        prompt = f"""Analyze this dispute and organize claims by party.

Parties: {', '.join(parties)}
Narrative: {narrative}
Claims: {', '.join(claims)}

For each party, identify:
1. Their main claims
2. Their underlying interests
3. Their desired outcomes

Return as JSON in this format:
{{
  "Party Name": {{
    "claims": ["claim1", "claim2"],
    "interests": ["interest1", "interest2"],
    "desired_outcome": "what they want"
  }}
}}

Return only the JSON object, no other text."""

        try:
            response = self.llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            # Fallback: basic structure
            result = {}
            for party in parties:
                result[party] = {
                    "claims": claims[:len(claims)//len(parties)] if claims else [],
                    "interests": ["To be determined"],
                    "desired_outcome": "Fair resolution"
                }
            return result
    
    def _find_common_ground(self, parsed_claims: Dict) -> Dict:
        """Identify areas of agreement and conflict"""
        prompt = f"""Analyze these party positions and identify:
1. Areas of agreement (common ground)
2. Points of conflict
3. Potential compromise areas

Party Positions:
{json.dumps(parsed_claims, indent=2)}

Return as JSON:
{{
  "agreements": ["point1", "point2"],
  "conflicts": ["conflict1", "conflict2"],
  "compromise_opportunities": ["opportunity1", "opportunity2"]
}}

Return only the JSON object, no other text."""

        try:
            response = self.llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            return {
                "agreements": ["Parties agree to seek fair resolution"],
                "conflicts": ["Multiple competing claims"],
                "compromise_opportunities": ["Negotiated settlement possible"]
            }
    
    def _generate_fair_outcomes(
        self,
        parsed_claims: Dict,
        common_ground: Dict,
        precedents: List[RetrievedDocument],
        narrative: str
    ) -> List[ProposedOutcome]:
        """Generate multiple fair outcome options"""
        # Prepare precedent context
        precedent_context = "\n".join([
            f"- {p.title}: {p.content[:200]}"
            for p in precedents[:3]
        ])
        
        prompt = f"""Based on this dispute, suggest 3 fair outcome options.

Dispute: {narrative}

Party Claims:
{json.dumps(parsed_claims, indent=2)}

Common Ground:
{json.dumps(common_ground, indent=2)}

Similar Cases:
{precedent_context}

Generate 3 different outcome options:
1. Compromise-based (split the difference)
2. Precedent-based (based on similar cases)
3. Interest-based (addresses underlying interests)

Return as JSON array:
[{{
  "outcome_type": "compromise/precedent/interest",
  "description": "Detailed description of the outcome",
  "rationale": "Why this is fair and feasible"
}}]

Return only the JSON array, no other text."""

        try:
            response = self.llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            outcomes_data = json.loads(content)
            
            # Convert to ProposedOutcome objects
            outcomes = []
            for outcome in outcomes_data:
                outcomes.append(ProposedOutcome(
                    outcome_type=outcome.get("outcome_type", "compromise"),
                    description=outcome.get("description", ""),
                    rationale=outcome.get("rationale", "")
                ))
            
            return outcomes
            
        except Exception as e:
            # Fallback outcomes
            return [
                ProposedOutcome(
                    outcome_type="compromise",
                    description="Equal division of disputed assets/claims between parties",
                    rationale="Fair split when no clear precedent exists"
                ),
                ProposedOutcome(
                    outcome_type="precedent",
                    description="Resolution based on similar case outcomes",
                    rationale="Follows established legal precedents"
                ),
                ProposedOutcome(
                    outcome_type="interest",
                    description="Solution addressing underlying interests of all parties",
                    rationale="Focuses on mutual benefit rather than positions"
                )
            ]
    
    def evaluate_fairness(
        self,
        outcome: ProposedOutcome,
        parsed_claims: Dict
    ) -> Dict:
        """Evaluate fairness of a proposed outcome"""
        prompt = f"""Evaluate the fairness of this proposed outcome.

Outcome: {outcome.description}
Rationale: {outcome.rationale}

Party Claims:
{json.dumps(parsed_claims, indent=2)}

Rate the outcome on these dimensions (0-10):
1. Proportionality: Is the outcome proportional to claims?
2. Equity: Do all parties feel heard?
3. Feasibility: Can this be implemented?
4. Sustainability: Will this resolve the dispute long-term?

Return as JSON:
{{
  "proportionality": 0-10,
  "equity": 0-10,
  "feasibility": 0-10,
  "sustainability": 0-10,
  "overall_score": 0-10,
  "concerns": ["concern1", "concern2"]
}}

Return only the JSON object, no other text."""

        try:
            response = self.llm.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            return {
                "proportionality": 7,
                "equity": 7,
                "feasibility": 7,
                "sustainability": 7,
                "overall_score": 7,
                "concerns": ["Evaluation unavailable"]
            }

# Global agent instance
mediation_agent = MediationAgent()
