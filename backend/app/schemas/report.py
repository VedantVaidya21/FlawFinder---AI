from typing import Optional, Dict, Any
from pydantic import BaseModel
from .base import BaseSchema


class ReportCreate(BaseSchema):
    """Create report request schema"""
    title: str
    report_type: str
    process_flow_id: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None


class ReportResponse(BaseSchema):
    """Report response schema"""
    id: str
    title: str
    report_type: str
    status: str
    content: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None
    user_id: str
    process_flow_id: Optional[str] = None
    created_at: str
    updated_at: str


class CEOReportRequest(BaseSchema):
    """CEO report generation request schema"""
    flow_id: Optional[str] = None
    include_departments: Optional[bool] = True
    format: str = "pdf"  # pdf, json
