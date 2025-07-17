from sqlalchemy import Column, Integer, String, ForeignKey
from db.session import Base

class FixSuggestion(Base):
    __tablename__ = "fix_suggestions"
    id = Column(Integer, primary_key=True, index=True)
    flaw_id = Column(Integer, ForeignKey("flaws.id"), nullable=False)
    suggestion = Column(String, nullable=False)
