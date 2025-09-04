from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Enum, Float, DateTime
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel
from .task import TaskStatus


class PipelineStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class DriftType(str, enum.Enum):
    DATA_DRIFT = "data_drift"
    CONCEPT_DRIFT = "concept_drift"
    LABEL_DRIFT = "label_drift"


class MLPipeline(BaseModel):
    __tablename__ = "ml_pipelines"
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    model_path = Column(String(500))
    metrics_endpoint = Column(String(500))
    status = Column(Enum(PipelineStatus), default=PipelineStatus.ACTIVE)
    pipeline_metadata = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User")
    drift_metrics = relationship("DriftMetric", back_populates="pipeline")
    retraining_events = relationship("RetrainingEvent", back_populates="pipeline")
    
    def __repr__(self):
        return f"<MLPipeline(id={self.id}, name='{self.name}', status='{self.status}')>"


class DriftMetric(BaseModel):
    __tablename__ = "drift_metrics"
    
    drift_type = Column(Enum(DriftType), nullable=False)
    metric_value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    drift_metadata = Column(JSON)
    pipeline_id = Column(Integer, ForeignKey("ml_pipelines.id"), nullable=False)
    
    # Relationships
    pipeline = relationship("MLPipeline", back_populates="drift_metrics")
    
    def __repr__(self):
        return f"<DriftMetric(id={self.id}, type='{self.drift_type}', value={self.metric_value})>"


class RetrainingEvent(BaseModel):
    __tablename__ = "retraining_events"
    
    trigger_reason = Column(String(255), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    model_version = Column(String(100))
    performance_metrics = Column(JSON)
    retraining_metadata = Column(JSON)
    pipeline_id = Column(Integer, ForeignKey("ml_pipelines.id"), nullable=False)
    
    # Relationships
    pipeline = relationship("MLPipeline", back_populates="retraining_events")
    
    def __repr__(self):
        return f"<RetrainingEvent(id={self.id}, reason='{self.trigger_reason}', status='{self.status}')>" 