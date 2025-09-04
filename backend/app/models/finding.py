from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Float, Enum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class FindingSeverity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FindingType(str, enum.Enum):
    BOTTLENECK = "bottleneck"
    REDUNDANCY = "redundancy"
    MANUAL_HANDOFF = "manual_handoff"
    WAIT_TIME = "wait_time"
    REWORK_LOOP = "rework_loop"
    DATA_DUPLICATION = "data_duplication"
    INEFFICIENT_PROCESS = "inefficient_process"


class Finding(BaseModel):
    __tablename__ = "findings"
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(Enum(FindingSeverity), nullable=False)
    finding_type = Column(Enum(FindingType), nullable=False)
    impact_score = Column(Float, nullable=False)  # 0-100
    node_id = Column(String(100))  # Reference to graph node
    tags = Column(JSON)  # Array of tags
    recommendations = Column(JSON)  # Array of recommendations
    process_flow_id = Column(Integer, ForeignKey("process_flows.id"), nullable=False)
    
    # Relationships
    process_flow = relationship("ProcessFlow", back_populates="findings")
    
    def __repr__(self):
        return f"<Finding(id={self.id}, title='{self.title}', severity='{self.severity}')>" 