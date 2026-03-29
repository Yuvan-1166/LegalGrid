"""Indian Kanoon scraper for legal documents"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import re

class IndianKanoonScraper:
    BASE_URL = "https://indiankanoon.org"
    
    def __init__(self, rate_limit: float = 1.0):
        """
        Initialize scraper
        
        Args:
            rate_limit: Seconds to wait between requests (be respectful!)
        """
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational Research Bot)'
        })
    
    def search_cases(
        self,
        query: str,
        page: int = 0,
        results_per_page: int = 10
    ) -> List[Dict]:
        """
        Search for cases on Indian Kanoon
        
        Args:
            query: Search query
            page: Page number (0-indexed)
            results_per_page: Number of results per page
            
        Returns:
            List of case metadata
        """
        url = f"{self.BASE_URL}/search/"
        params = {
            "formInput": query,
            "pagenum": page
        }
        
        try:
            time.sleep(self.rate_limit)
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            cases = []
            
            # Find all result divs
            result_divs = soup.find_all('div', class_='result')
            
            for div in result_divs[:results_per_page]:
                case = self._parse_case_result(div)
                if case:
                    cases.append(case)
            
            return cases
        
        except Exception as e:
            print(f"Error searching cases: {e}")
            return []
    
    def _parse_case_result(self, div) -> Optional[Dict]:
        """Parse a single case result"""
        try:
            # Extract title and link
            title_tag = div.find('a', class_='cite_tag')
            if not title_tag:
                return None
            
            title = title_tag.get_text(strip=True)
            link = title_tag.get('href', '')
            
            # Extract doc ID from link
            doc_id_match = re.search(r'/doc/(\d+)/', link)
            doc_id = doc_id_match.group(1) if doc_id_match else None
            
            # Extract snippet
            snippet_tag = div.find('div', class_='result_snippet')
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            
            # Extract court and year
            court = "Unknown"
            year = None
            
            # Try to extract from title
            if "Supreme Court" in title:
                court = "Supreme Court"
            elif "High Court" in title:
                court_match = re.search(r'(\w+)\s+High Court', title)
                if court_match:
                    court = f"{court_match.group(1)} High Court"
            
            year_match = re.search(r'\b(19|20)\d{2}\b', title)
            if year_match:
                year = int(year_match.group(0))
            
            return {
                "doc_id": f"IK_{doc_id}" if doc_id else None,
                "title": title,
                "url": f"{self.BASE_URL}{link}" if link else None,
                "snippet": snippet,
                "court": court,
                "year": year,
                "source": "Indian Kanoon"
            }
        
        except Exception as e:
            print(f"Error parsing case result: {e}")
            return None
    
    def get_case_content(self, doc_id: str) -> Optional[Dict]:
        """
        Fetch full case content
        
        Args:
            doc_id: Document ID (e.g., "IK_12345" or just "12345")
            
        Returns:
            Case content and metadata
        """
        # Extract numeric ID
        numeric_id = doc_id.replace("IK_", "")
        url = f"{self.BASE_URL}/doc/{numeric_id}/"
        
        try:
            time.sleep(self.rate_limit)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('h1', class_='doc_title')
            title = title_tag.get_text(strip=True) if title_tag else "Unknown"
            
            # Extract main content
            content_div = soup.find('div', class_='doc_content')
            if not content_div:
                return None
            
            # Clean content
            content = content_div.get_text(separator='\n', strip=True)
            
            # Extract metadata
            metadata = self._extract_metadata(soup)
            
            return {
                "doc_id": doc_id,
                "title": title,
                "content": content,
                "url": url,
                **metadata
            }
        
        except Exception as e:
            print(f"Error fetching case content: {e}")
            return None
    
    def _extract_metadata(self, soup) -> Dict:
        """Extract metadata from case page"""
        metadata = {
            "court": "Unknown",
            "year": None,
            "judges": [],
            "citations": []
        }
        
        # Try to find metadata in various places
        # This is a simplified version - actual structure may vary
        
        return metadata
    
    def scrape_statutes(self, act_name: str) -> List[Dict]:
        """
        Scrape statute sections
        
        Args:
            act_name: Name of the act (e.g., "Indian Penal Code")
            
        Returns:
            List of statute sections
        """
        # Search for the act
        cases = self.search_cases(act_name, results_per_page=20)
        
        statutes = []
        for case in cases:
            # Filter for actual statute documents
            if "section" in case["title"].lower():
                content = self.get_case_content(case["doc_id"])
                if content:
                    statutes.append(content)
        
        return statutes

# Global scraper instance
indian_kanoon_scraper = IndianKanoonScraper()
