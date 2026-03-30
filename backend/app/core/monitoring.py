"""
Performance monitoring utilities
Tracks response times and system metrics
"""

import time
from typing import Dict, List
from collections import defaultdict
from datetime import datetime

class PerformanceMonitor:
    """Monitor API performance and system metrics"""
    
    def __init__(self):
        self.request_times: Dict[str, List[float]] = defaultdict(list)
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.start_time = time.time()
    
    def record_request(self, endpoint: str, duration: float, success: bool = True):
        """Record request metrics"""
        self.request_times[endpoint].append(duration)
        self.request_counts[endpoint] += 1
        
        if not success:
            self.error_counts[endpoint] += 1
    
    def get_stats(self, endpoint: str = None) -> Dict:
        """Get performance statistics"""
        if endpoint:
            times = self.request_times.get(endpoint, [])
            return {
                "endpoint": endpoint,
                "total_requests": self.request_counts.get(endpoint, 0),
                "errors": self.error_counts.get(endpoint, 0),
                "avg_response_time": sum(times) / len(times) if times else 0,
                "min_response_time": min(times) if times else 0,
                "max_response_time": max(times) if times else 0
            }
        
        # Overall stats
        all_times = []
        for times in self.request_times.values():
            all_times.extend(times)
        
        return {
            "uptime_seconds": time.time() - self.start_time,
            "total_requests": sum(self.request_counts.values()),
            "total_errors": sum(self.error_counts.values()),
            "avg_response_time": sum(all_times) / len(all_times) if all_times else 0,
            "endpoints": list(self.request_counts.keys())
        }
    
    def get_health_status(self) -> Dict:
        """Get system health status"""
        stats = self.get_stats()
        total_requests = stats["total_requests"]
        total_errors = stats["total_errors"]
        
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
        avg_response = stats["avg_response_time"]
        
        # Determine health status
        if error_rate > 10 or avg_response > 5:
            status = "unhealthy"
        elif error_rate > 5 or avg_response > 3:
            status = "degraded"
        else:
            status = "healthy"
        
        return {
            "status": status,
            "error_rate": round(error_rate, 2),
            "avg_response_time": round(avg_response, 3),
            "uptime": round(stats["uptime_seconds"], 0)
        }

# Global monitor instance
performance_monitor = PerformanceMonitor()
