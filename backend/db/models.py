from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workflows = relationship("Workflow", back_populates="user")

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    raw_data = Column(JSON, nullable=False)
    processed_data = Column(JSON)
    file_type = Column(String(50), nullable=False)  # 'csv' or 'json'
    status = Column(String(50), default="uploaded")  # uploaded, processing, analyzed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workflows")
    flaws = relationship("Flaw", back_populates="workflow")
    reports = relationship("Report", back_populates="workflow")

class Flaw(Base):
    __tablename__ = "flaws"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    flaw_type = Column(String(100), nullable=False)  # bottleneck, redundancy, security, etc.
    severity = Column(String(50), nullable=False)  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255))  # where in the workflow
    impact_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="flaws")
    fix_suggestions = relationship("FixSuggestion", back_populates="flaw")

class FixSuggestion(Base):
    __tablename__ = "fix_suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    flaw_id = Column(Integer, ForeignKey("flaws.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    implementation_effort = Column(String(50))  # low, medium, high
    expected_impact = Column(String(50))  # low, medium, high
    priority = Column(Integer, default=1)
    estimated_time = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    flaw = relationship("Flaw", back_populates="fix_suggestions")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    executive_summary = Column(Text, nullable=False)
    total_flaws = Column(Integer, default=0)
    critical_flaws = Column(Integer, default=0)
    high_flaws = Column(Integer, default=0)
    medium_flaws = Column(Integer, default=0)
    low_flaws = Column(Integer, default=0)
    brutality_score = Column(Float, default=0.0)
    improvement_percentage = Column(Float, default=0.0)
    recommendations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="reports")

class AnalysisSession(Base):
    __tablename__ = "analysis_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    status = Column(String(50), default="started")  # started, completed, failed
    ai_model_used = Column(String(100), default="gpt-4")
    processing_time = Column(Float)  # in seconds
    tokens_used = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
