from sqlalchemy import Column, Integer, ForeignKey, JSON, Float, String
from sqlalchemy.orm import relationship
from .base import BaseModel


class BrutalityScore(BaseModel):
    __tablename__ = "brutality_scores"
    
    score = Column(Float, nullable=False)  # 0-100
    breakdown = Column(JSON)  # Detailed breakdown of score components
    version = Column(String(50))  # Version of scoring algorithm
    process_flow_id = Column(Integer, ForeignKey("process_flows.id"), nullable=False)
    
    # Relationships
    process_flow = relationship("ProcessFlow", back_populates="brutality_scores")
    
    def __repr__(self):
        return f"<BrutalityScore(id={self.id}, score={self.score}, flow_id={self.process_flow_id})>" 