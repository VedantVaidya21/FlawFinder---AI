from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Float, Enum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class FlowStatus(str, enum.Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessFlow(BaseModel):
    __tablename__ = "process_flows"
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    raw_input = Column(Text, nullable=False)  # Original text/diagram input
    parsed_graph = Column(JSON)  # Parsed graph structure
    version = Column(Integer, default=1)
    status = Column(Enum(FlowStatus), default=FlowStatus.DRAFT)
    brutality_score = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="process_flows")
    organization = relationship("Organization", back_populates="process_flows")
    findings = relationship("Finding", back_populates="process_flow")
    brutality_scores = relationship("BrutalityScore", back_populates="process_flow")
    
    def __repr__(self):
        return f"<ProcessFlow(id={self.id}, name='{self.name}', status='{self.status}')>" 