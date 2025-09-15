from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from .base import BaseSchema


class PipelineCreate(BaseSchema):
    """Create ML pipeline request schema"""
    name: str
    description: Optional[str] = None
    model_path: str
    metrics_endpoint: str
    pipeline_metadata: Optional[Dict[str, Any]] = None


class PipelineResponse(BaseSchema):
    """ML pipeline response schema"""
    id: int
    name: str
    description: Optional[str] = None
    model_path: str
    metrics_endpoint: str
    status: str
    pipeline_metadata: Optional[Dict[str, Any]] = None
    user_id: int
    created_at: str
    updated_at: str


class DriftMetricCreate(BaseSchema):
    """Create drift metric request schema"""
    drift_type: str
    metric_value: float
    threshold: float
    drift_metadata: Optional[Dict[str, Any]] = None


class DriftMetricResponse(BaseSchema):
    """Drift metric response schema"""
    id: int
    drift_type: str
    metric_value: float
    threshold: float
    timestamp: str
    drift_metadata: Optional[Dict[str, Any]] = None
    pipeline_id: int


class PipelineStatusResponse(BaseSchema):
    """Pipeline status response schema"""
    pipeline_id: int
    status: str
    last_retrain: Optional[str] = None
    latest_metrics: List[Dict[str, Any]]
    health_score: float 