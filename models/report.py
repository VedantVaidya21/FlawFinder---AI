from sqlalchemy import Column, Integer, String, ForeignKey
from db.session import Base

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    summary = Column(String, nullable=False)
