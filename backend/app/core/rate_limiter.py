"""
Rate limiting for API endpoints
Prevents abuse and ensures fair usage
"""

from fastapi import HTTPException, Request
from typing import Dict
import time
from collections import defaultdict

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from request"""
        # Use IP address as identifier
        return request.client.host if request.client else "unknown"
    
    def _clean_old_requests(self, client_id: str):
        """Remove requests older than 1 minute"""
        current_time = time.time()
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 60
        ]
    
    def check_rate_limit(self, request: Request):
        """Check if request is within rate limit"""
        client_id = self._get_client_id(request)
        current_time = time.time()
        
        # Clean old requests
        self._clean_old_requests(client_id)
        
        # Check rate limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute."
            )
        
        # Add current request
        self.requests[client_id].append(current_time)
    
    def get_stats(self) -> Dict:
        """Get rate limiter statistics"""
        return {
            "total_clients": len(self.requests),
            "requests_per_minute_limit": self.requests_per_minute
        }

# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)
