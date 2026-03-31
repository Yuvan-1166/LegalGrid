"""Monitoring and Metrics API Routes"""
from fastapi import APIRouter
from app.monitoring.metrics import metrics_collector
from datetime import datetime

router = APIRouter(prefix="/api/v1/monitoring", tags=["monitoring"])

@router.get("/stats")
async def get_stats():
    """Get system metrics and statistics"""
    stats = metrics_collector.get_stats()
    return {
        "timestamp": datetime.now().isoformat(),
        "metrics": stats,
        "status": "healthy"
    }

@router.post("/reset")
async def reset_metrics():
    """Reset all metrics"""
    metrics_collector.reset()
    return {"message": "Metrics reset successfully"}
