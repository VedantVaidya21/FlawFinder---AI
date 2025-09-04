from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..models.user import User
from ..models.agentops import MLPipeline, DriftMetric, RetrainingEvent, PipelineStatus, DriftType
from ..schemas.agentops import PipelineCreate, PipelineResponse, DriftMetricCreate, DriftMetricResponse, PipelineStatusResponse

router = APIRouter(prefix="/agentops", tags=["agentops"])


@router.post("/pipelines", response_model=PipelineResponse)
def create_pipeline(
    pipeline_data: PipelineCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Register a new ML pipeline"""
    db_pipeline = MLPipeline(
        name=pipeline_data.name,
        description=pipeline_data.description,
        model_path=pipeline_data.model_path,
        metrics_endpoint=pipeline_data.metrics_endpoint,
        metadata=pipeline_data.metadata,
        user_id=current_user.id,
        status=PipelineStatus.ACTIVE
    )
    
    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    
    return db_pipeline


@router.get("/pipelines", response_model=List[PipelineResponse])
def get_pipelines(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all pipelines for current user"""
    pipelines = db.query(MLPipeline).filter(
        MLPipeline.user_id == current_user.id
    ).all()
    
    return pipelines


@router.get("/pipelines/{pipeline_id}", response_model=PipelineResponse)
def get_pipeline(
    pipeline_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific pipeline by ID"""
    pipeline = db.query(MLPipeline).filter(
        MLPipeline.id == pipeline_id,
        MLPipeline.user_id == current_user.id
    ).first()
    
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )
    
    return pipeline


@router.post("/pipelines/{pipeline_id}/monitor", response_model=DriftMetricResponse)
def monitor_drift(
    pipeline_id: int,
    drift_data: DriftMetricCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Capture drift metrics for a pipeline"""
    pipeline = db.query(MLPipeline).filter(
        MLPipeline.id == pipeline_id,
        MLPipeline.user_id == current_user.id
    ).first()
    
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )
    
    # Create drift metric
    db_drift = DriftMetric(
        drift_type=DriftType(drift_data.drift_type),
        metric_value=drift_data.metric_value,
        threshold=drift_data.threshold,
        metadata=drift_data.metadata,
        pipeline_id=pipeline_id
    )
    
    db.add(db_drift)
    db.commit()
    db.refresh(db_drift)
    
    return db_drift


@router.post("/pipelines/{pipeline_id}/retrain")
def trigger_retraining(
    pipeline_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Trigger model retraining for a pipeline"""
    pipeline = db.query(MLPipeline).filter(
        MLPipeline.id == pipeline_id,
        MLPipeline.user_id == current_user.id
    ).first()
    
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )
    
    # Create retraining event
    db_retrain = RetrainingEvent(
        trigger_reason="Manual trigger",
        status="pending",
        pipeline_id=pipeline_id
    )
    
    db.add(db_retrain)
    db.commit()
    db.refresh(db_retrain)
    
    # TODO: Implement actual retraining logic
    # This would typically queue a Celery task
    
    return {
        "message": "Retraining triggered successfully",
        "retraining_id": db_retrain.id
    }


@router.get("/pipelines/{pipeline_id}/status", response_model=PipelineStatusResponse)
def get_pipeline_status(
    pipeline_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current pipeline health and status"""
    pipeline = db.query(MLPipeline).filter(
        MLPipeline.id == pipeline_id,
        MLPipeline.user_id == current_user.id
    ).first()
    
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )
    
    # Get latest metrics
    latest_metrics = db.query(DriftMetric).filter(
        DriftMetric.pipeline_id == pipeline_id
    ).order_by(DriftMetric.created_at.desc()).limit(5).all()
    
    # Get last retraining event
    last_retrain = db.query(RetrainingEvent).filter(
        RetrainingEvent.pipeline_id == pipeline_id
    ).order_by(RetrainingEvent.created_at.desc()).first()
    
    # Calculate health score (mock implementation)
    health_score = 85.0  # TODO: Implement actual health calculation
    
    return {
        "pipeline_id": pipeline_id,
        "status": pipeline.status,
        "last_retrain": last_retrain.created_at.isoformat() if last_retrain else None,
        "latest_metrics": [
            {
                "drift_type": metric.drift_type,
                "metric_value": metric.metric_value,
                "threshold": metric.threshold,
                "timestamp": metric.created_at.isoformat()
            }
            for metric in latest_metrics
        ],
        "health_score": health_score
    } 