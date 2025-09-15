from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from neo4j.time import DateTime as Neo4jDateTime
from .base_neo4j import BaseNode


class ReportType(str, Enum):
    CEO_REPORT = "ceo_report"
    DEPARTMENT_REPORT = "department_report"
    TECHNICAL_REPORT = "technical_report"


class ReportStatus(str, Enum):
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class Report(BaseNode):
    """Neo4j model for Report"""
    title: str
    report_type: ReportType
    status: ReportStatus = ReportStatus.GENERATING
    content: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None
    user_id: str
    process_flow_id: Optional[str] = None

    # 🔥 Neo4j datetime conversion
    @field_validator("created_at", "updated_at", mode="before")
    def convert_neo4j_datetime(cls, v):
        if isinstance(v, Neo4jDateTime):
            return datetime(
                year=v.year,
                month=v.month,
                day=v.day,
                hour=v.hour,
                minute=v.minute,
                second=v.second,
                microsecond=v.nanosecond // 1000,
                tzinfo=v.tzinfo,
            )
        return v

    class Config:
        json_encoders = {
            **BaseNode.Config.json_encoders,
            datetime: lambda v: v.isoformat() if v else None,
        }

    @classmethod
    async def get_by_user(cls, user_id: str, skip: int = 0, limit: int = 100) -> List["Report"]:
        """Get all reports for a user"""
        query = """
        MATCH (r:Report {user_id: $user_id})
        RETURN r
        ORDER BY r.created_at DESC
        SKIP $skip
        LIMIT $limit
        """
        from ..core.database import db
        async with db.get_session() as session:
            result = await session.run(query, user_id=user_id, skip=skip, limit=limit)
            records = await result.values()
            return [cls(**record[0]) for record in records if record and record[0]]

    @classmethod
    async def get_by_id_and_user(cls, report_id: str, user_id: str) -> Optional["Report"]:
        """Get a specific report by ID and user"""
        query = """
        MATCH (r:Report {id: $report_id, user_id: $user_id})
        RETURN r
        """
        from ..core.database import db
        async with db.get_session() as session:
            result = await session.run(query, report_id=report_id, user_id=user_id)
            record = await result.single()
            if not record:
                return None
            return cls(**record["r"])


class ReportCreate(BaseModel):
    """Model for creating a new report"""
    title: str
    report_type: ReportType
    content: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None
    process_flow_id: Optional[str] = None


class ReportResponse(BaseModel):
    """Response model for report"""
    id: str
    title: str
    report_type: ReportType
    status: ReportStatus = ReportStatus.GENERATING
    content: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None
    user_id: str
    process_flow_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CEOReportRequest(BaseModel):
    """Request model for CEO report generation"""
    flow_id: str
