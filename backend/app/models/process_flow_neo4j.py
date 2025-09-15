# backend\app\models\process_flow_neo4j.py
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from neo4j.time import DateTime as Neo4jDateTime
from .base_neo4j import BaseNode


class FlowStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessFlow(BaseNode):
    """Neo4j model for ProcessFlow"""
    name: str
    description: Optional[str] = None
    raw_input: str
    parsed_graph: Optional[Dict[str, Any]] = None
    version: int = 1
    status: FlowStatus = FlowStatus.DRAFT
    brutality_score: Optional[float] = None
    user_id: str
    organization_id: Optional[str] = None
    is_active: bool = True

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
    async def get_by_user(cls, user_id: str) -> List["ProcessFlow"]:
        """Get all process flows for a user"""
        query = """
        MATCH (f:ProcessFlow {user_id: $user_id, is_active: true})
        RETURN f
        """
        async with cls.db.get_session() as session:
            result = await session.run(query, user_id=user_id)
            records = await result.values()
            return [cls(**record[0]) for record in records if record and record[0]]

    @classmethod
    async def get_by_id_and_user(cls, flow_id: str, user_id: str) -> Optional["ProcessFlow"]:
        """Get a specific process flow by ID and user"""
        query = """
        MATCH (f:ProcessFlow {id: $flow_id, user_id: $user_id, is_active: true})
        RETURN f
        """
        async with cls.db.get_session() as session:
            result = await session.run(query, flow_id=flow_id, user_id=user_id)
            record = await result.single()
            if not record:
                return None
            return cls(**record["f"])

    async def soft_delete(self) -> None:
        """Soft delete the process flow"""
        self.is_active = False
        await self.save()


class ProcessFlowCreate(BaseModel):
    """Model for creating a new process flow"""
    name: str
    description: Optional[str] = None
    raw_input: str
    organization_id: Optional[str] = None


class ProcessFlowResponse(BaseModel):
    """Response model for process flow"""
    id: str
    name: str
    description: Optional[str] = None
    raw_input: str
    parsed_graph: Optional[Dict[str, Any]] = None
    version: int = 1
    status: FlowStatus = FlowStatus.DRAFT
    brutality_score: Optional[float] = None
    user_id: str
    organization_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
