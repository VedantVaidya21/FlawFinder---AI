from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Enum, Float
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class TaskType(str, enum.Enum):
    FLOW_PARSING = "flow_parsing"
    SCORE_CALCULATION = "score_calculation"
    REPORT_GENERATION = "report_generation"
    MODEL_TRAINING = "model_training"
    DATA_DRIFT_MONITORING = "data_drift_monitoring"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    __tablename__ = "tasks"
    
    task_type = Column(Enum(TaskType), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    progress = Column(Float, default=0.0)  # 0-100
    result = Column(JSON)  # Task result data
    error_message = Column(Text)
    logs = Column(JSON)  # Array of log messages
    task_metadata = Column(JSON)  # Additional task metadata
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    process_flow_id = Column(Integer, ForeignKey("process_flows.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    process_flow = relationship("ProcessFlow")
    
    def __repr__(self):
        return f"<Task(id={self.id}, type='{self.task_type}', status='{self.status}')>" 