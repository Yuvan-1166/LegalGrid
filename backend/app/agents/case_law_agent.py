"""Case Law Agent for finding relevant legal precedents"""

from typing import List, Dict, Optional
from datetime import datetime
from app.core.llm import llm_client
from app.rag.hybrid_retriever import hybrid_retriever
from app.models.schemas import Precedent
import uuid

class CaseLawAgent:
    def __init__(self):
        self.llm = llm_client
        self.retriever = hybrid_retriever
    
    def find_precedents(
        self,
        case_description: str,
        jurisdiction: str = "All-India",
        top_k: int = 5
    ) -> List[Precedent]:
        """
        Find relevant legal precedents for a case
        
        Args:
            case_description: Description of the case or legal issue
            jurisdiction: Jurisdiction to search in
            top_k: Number of precedents to return
            
        Returns:
            List of relevant precedents with rankings
        """
        # Step 1: Retrieve similar cases using hybrid search
        similar_cases = self.retriever.retrieve(
            query=case_description,
            collection="cases",
            jurisdiction=jurisdiction,
            top_k=top_k * 2,  # Get more for re-ranking
            use_hybrid=True
        )
        
        # Step 2: Multi-factor ranking
        ranked_cases = self._multi_factor_rank(case_description, similar_cases)
        
        # Step 3: Extract key information and format
        precedents = []
        for case, score in ranked_cases[:top_k]:
            precedent = self._format_precedent(case, score, case_description)
            precedents.append(precedent)
        
        return precedents
    
    def _multi_factor_rank(
        self,
        query: str,
        cases: List[Dict]
    ) -> List[tuple]:
        """
        Rank cases by multiple factors:
        - Semantic similarity (from retrieval)
        - Citation authority (how often cited)
        - Temporal relevance (recency)
        - Court hierarchy (SC > HC > District)
        - Keyword matching bonus
        """
        scored_cases = []
        query_lower = query.lower()
        
        for case in cases:
            # Factor 1: Semantic similarity (already in fusion_score)
            semantic_score = case.get("fusion_score", case.get("score", 0.5))
            
            # Factor 2: Citation authority (estimate from metadata)
            citation_count = case.get("metadata", {}).get("citation_count", 0)
            authority_score = min(citation_count / 100, 1.0)  # Normalize to 0-1
            
            # Factor 3: Temporal relevance (newer is better, but not too much weight)
            year = case.get("metadata", {}).get("year", 2000)
            current_year = datetime.now().year
            age = current_year - year
            recency_score = max(0, 1 - (age / 50))  # Decay over 50 years
            
            # Factor 4: Court hierarchy
            court = case.get("metadata", {}).get("court", "Unknown")
            hierarchy_score = self._get_court_hierarchy_score(court)
            
            # Factor 5: Keyword matching bonus (check if query keywords appear in title/content)
            keyword_bonus = 0.0
            title = case.get("title", "").lower()
            content = case.get("content", "").lower()
            
            # Extract important keywords from query (simple approach)
            query_keywords = [w for w in query_lower.split() if len(w) > 3]
            if query_keywords:
                matches = sum(1 for kw in query_keywords if kw in title or kw in content)
                keyword_bonus = min(matches / len(query_keywords), 1.0)
            
            # Combined score with adjusted weights
            combined_score = (
                0.40 * semantic_score +      # Semantic similarity
                0.15 * authority_score +      # Citation authority
                0.10 * recency_score +        # Recency
                0.15 * hierarchy_score +      # Court hierarchy
                0.20 * keyword_bonus          # Keyword matching bonus
            )
            
            scored_cases.append((case, combined_score))
        
        # Sort by combined score
        return sorted(scored_cases, key=lambda x: x[1], reverse=True)
    
    def _get_court_hierarchy_score(self, court: str) -> float:
        """Assign score based on court hierarchy"""
        court_lower = court.lower()
        
        if "supreme court" in court_lower:
            return 1.0
        elif "high court" in court_lower:
            return 0.7
        elif "district" in court_lower or "sessions" in court_lower:
            return 0.4
        elif "tribunal" in court_lower:
            return 0.5
        else:
            return 0.3
    
    def _format_precedent(
        self,
        case: Dict,
        relevance_score: float,
        query: str
    ) -> Precedent:
        """Format case data into Precedent schema with citations"""
        metadata = case.get("metadata", {})
        
        # Extract or generate summary
        summary = self._generate_summary(case, query)
        
        # Extract holding
        holding = metadata.get("holding", "Holding not available")
        
        # Generate explanation with citation
        reason = self._explain_retrieval(case, relevance_score)
        citation = metadata.get("citation", f"{case.get('title', 'Unknown')} ({metadata.get('year', 'N/A')})")
        reason_with_citation = f"{reason} Citation: {citation}"
        
        return Precedent(
            title=case.get("title", "Unknown Case"),
            year=metadata.get("year", 2000),
            court=metadata.get("court", "Unknown Court"),
            relevance_score=round(relevance_score, 3),
            summary=summary,
            holding=holding,
            reason_retrieved=reason_with_citation
        )
    
    def _generate_summary(self, case: Dict, query: str) -> str:
        """Generate concise summary of the case"""
        content = case.get("content", "")
        
        # If content is short, use it directly
        if len(content) < 300:
            return content
        
        # For longer content, extract first 250 chars as summary
        # This is faster than LLM and works well for our use case
        summary = content[:250].strip()
        
        # Try to end at a sentence boundary
        last_period = summary.rfind('.')
        if last_period > 100:  # Only if we have at least 100 chars
            summary = summary[:last_period + 1]
        else:
            summary += "..."
        
        return summary
    
    def _explain_retrieval(self, case: Dict, score: float) -> str:
        """Explain why this case was retrieved"""
        method = case.get("retrieval_method", "unknown")
        court = case.get("metadata", {}).get("court", "Unknown")
        year = case.get("metadata", {}).get("year", "Unknown")
        
        explanation = f"Retrieved via {method} search. "
        explanation += f"Relevance score: {score:.2%}. "
        explanation += f"From {court} ({year}). "
        
        # Add specific reasons
        if score > 0.8:
            explanation += "Highly relevant to your case."
        elif score > 0.6:
            explanation += "Moderately relevant with similar legal principles."
        else:
            explanation += "May provide useful context."
        
        return explanation
    
    def analyze_precedent_strength(
        self,
        precedents: List[Precedent]
    ) -> Dict:
        """
        Analyze the strength of precedents found
        
        Returns:
            Analysis of precedent strength and consistency
        """
        if not precedents:
            return {
                "strength": "weak",
                "consistency": "none",
                "recommendation": "Insufficient precedents found"
            }
        
        # Count by court
        sc_count = sum(1 for p in precedents if "Supreme Court" in p.court)
        hc_count = sum(1 for p in precedents if "High Court" in p.court)
        
        # Average relevance
        avg_relevance = sum(p.relevance_score for p in precedents) / len(precedents)
        
        # Determine strength
        if sc_count >= 2 and avg_relevance > 0.7:
            strength = "strong"
        elif (sc_count >= 1 or hc_count >= 2) and avg_relevance > 0.6:
            strength = "moderate"
        else:
            strength = "weak"
        
        # Determine consistency
        if len(precedents) >= 3 and avg_relevance > 0.65:
            consistency = "high"
        elif len(precedents) >= 2:
            consistency = "moderate"
        else:
            consistency = "low"
        
        # Generate recommendation
        if strength == "strong":
            recommendation = "Strong precedent support. Case has solid legal backing."
        elif strength == "moderate":
            recommendation = "Moderate precedent support. Additional research recommended."
        else:
            recommendation = "Weak precedent support. Consider alternative legal strategies."
        
        return {
            "strength": strength,
            "consistency": consistency,
            "supreme_court_cases": sc_count,
            "high_court_cases": hc_count,
            "average_relevance": round(avg_relevance, 3),
            "recommendation": recommendation
        }

# Global agent instance
case_law_agent = CaseLawAgent()
