from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Organization(BaseModel):
    __tablename__ = "organizations"
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    industry = Column(String(100))
    size = Column(String(50))  # small, medium, large, enterprise
    
    # Relationships
    users = relationship("User", back_populates="organization")
    process_flows = relationship("ProcessFlow", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>" 