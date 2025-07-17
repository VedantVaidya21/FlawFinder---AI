from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from db.session import Base

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    raw_data = Column(JSON, nullable=False)
