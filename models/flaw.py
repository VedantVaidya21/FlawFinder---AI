from sqlalchemy import Column, Integer, String, ForeignKey
from db.session import Base

class Flaw(Base):
    __tablename__ = "flaws"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    flaw_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
