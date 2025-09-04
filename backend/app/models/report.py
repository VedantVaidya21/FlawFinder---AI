from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class ReportType(str, enum.Enum):
    CEO_REPORT = "ceo_report"
    DEPARTMENT_REPORT = "department_report"
    TECHNICAL_REPORT = "technical_report"


class ReportStatus(str, enum.Enum):
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class Report(BaseModel):
    __tablename__ = "reports"
    
    title = Column(String(255), nullable=False)
    report_type = Column(Enum(ReportType), nullable=False)
    status = Column(Enum(ReportStatus), default=ReportStatus.GENERATING)
    content = Column(JSON)  # Report content structure
    file_url = Column(String(500))  # URL to downloadable PDF
    report_metadata = Column(JSON)  # Additional metadata
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    process_flow_id = Column(Integer, ForeignKey("process_flows.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    process_flow = relationship("ProcessFlow")
    
    def __repr__(self):
        return f"<Report(id={self.id}, title='{self.title}', type='{self.report_type}')>" 