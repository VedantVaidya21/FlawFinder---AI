from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from .base import BaseSchema


class ProcessFlowCreate(BaseSchema):
    """Create process flow request schema"""
    name: str
    description: Optional[str] = None
    raw_input: str
    organization_id: Optional[str] = None


class ProcessFlowUpdate(BaseSchema):
    """Update process flow request schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    raw_input: Optional[str] = None


class ProcessFlowResponse(BaseSchema):
    """Process flow response schema"""
    id: str
    name: str
    description: Optional[str] = None
    version: int
    status: str
    brutality_score: Optional[float] = None
    user_id: str
    organization_id: Optional[str] = None
    created_at: str
    updated_at: str


class FlowParseRequest(BaseSchema):
    """Flow parsing request schema"""
    flow_id: str


class FlowParseResponse(BaseSchema):
    """Flow parsing response schema"""
    flow_id: str
    parsed_graph: Dict[str, Any]
    findings: List[Dict[str, Any]]
    status: str


class BrutalityScoreResponse(BaseSchema):
    """Brutality score response schema"""
    flow_id: str
    score: float
    breakdown: Dict[str, Any]
    version: str
