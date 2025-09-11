from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..core.neo4j import get_neo4j
from ..core.deps import get_current_active_user, User
from ..schemas.agentops import PipelineCreate, PipelineResponse, DriftMetricCreate, DriftMetricResponse, PipelineStatusResponse
import uuid
from datetime import datetime

router = APIRouter(prefix="/agentops", tags=["agentops"])


@router.post("/pipelines", response_model=PipelineResponse)
def create_pipeline(
    pipeline_data: PipelineCreate,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Register a new ML pipeline"""
    pipeline_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    create_query = """
    CREATE (p:MLPipeline {
        id: $id,
        name: $name,
        description: $description,
        model_path: $model_path,
        metrics_endpoint: $metrics_endpoint,
        metadata: $metadata,
        user_id: $user_id,
        status: $status,
        created_at: $created_at,
        updated_at: $updated_at
    })
    RETURN p
    """

    neo4j_conn.execute_write_query(create_query, {
        "id": pipeline_id,
        "name": pipeline_data.name,
        "description": pipeline_data.description,
        "model_path": pipeline_data.model_path,
        "metrics_endpoint": pipeline_data.metrics_endpoint,
        "metadata": pipeline_data.metadata,
        "user_id": current_user.id,
        "status": "active",
        "created_at": now,
        "updated_at": now
    })

    return {
        "id": pipeline_id,
        "name": pipeline_data.name,
        "description": pipeline_data.description,
        "model_path": pipeline_data.model_path,
        "metrics_endpoint": pipeline_data.metrics_endpoint,
        "metadata": pipeline_data.metadata,
        "user_id": current_user.id,
        "status": "active",
        "created_at": now,
        "updated_at": now
    }


@router.get("/pipelines", response_model=List[PipelineResponse])
def get_pipelines(
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Get all pipelines for current user"""
    query = """
    MATCH (p:MLPipeline)
    WHERE p.user_id = $user_id
    RETURN p.id as id, p.name as name, p.description as description,
           p.model_path as model_path, p.metrics_endpoint as metrics_endpoint,
           p.metadata as metadata, p.user_id as user_id, p.status as status,
           p.created_at as created_at, p.updated_at as updated_at
    """

    result = neo4j_conn.execute_query(query, {
        "user_id": current_user.id
    })

    return result


@router.get("/pipelines/{pipeline_id}", response_model=PipelineResponse)
def get_pipeline(
    pipeline_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Get a specific pipeline by ID"""
    query = """
    MATCH (p:MLPipeline)
    WHERE p.id = $pipeline_id AND p.user_id = $user_id
    RETURN p.id as id, p.name as name, p.description as description,
           p.model_path as model_path, p.metrics_endpoint as metrics_endpoint,
           p.metadata as metadata, p.user_id as user_id, p.status as status,
           p.created_at as created_at, p.updated_at as updated_at
    """

    result = neo4j_conn.execute_query(query, {
        "pipeline_id": pipeline_id,
        "user_id": current_user.id
    })

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )

    return result[0]


@router.post("/pipelines/{pipeline_id}/monitor", response_model=DriftMetricResponse)
def monitor_drift(
    pipeline_id: str,
    drift_data: DriftMetricCreate,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Capture drift metrics for a pipeline"""
    # Check if pipeline exists
    pipeline_query = """
    MATCH (p:MLPipeline)
    WHERE p.id = $pipeline_id AND p.user_id = $user_id
    RETURN p
    """

    pipeline_result = neo4j_conn.execute_query(pipeline_query, {
        "pipeline_id": pipeline_id,
        "user_id": current_user.id
    })

    if not pipeline_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )

    # Create drift metric
    metric_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    create_metric_query = """
    CREATE (m:DriftMetric {
        id: $id,
        drift_type: $drift_type,
        metric_value: $metric_value,
        threshold: $threshold,
        metadata: $metadata,
        pipeline_id: $pipeline_id,
        created_at: $created_at
    })
    RETURN m
    """

    neo4j_conn.execute_write_query(create_metric_query, {
        "id": metric_id,
        "drift_type": drift_data.drift_type,
        "metric_value": drift_data.metric_value,
        "threshold": drift_data.threshold,
        "metadata": drift_data.metadata,
        "pipeline_id": pipeline_id,
        "created_at": now
    })

    return {
        "id": metric_id,
        "drift_type": drift_data.drift_type,
        "metric_value": drift_data.metric_value,
        "threshold": drift_data.threshold,
        "metadata": drift_data.metadata,
        "pipeline_id": pipeline_id,
        "created_at": now
    }


@router.post("/pipelines/{pipeline_id}/retrain")
def trigger_retraining(
    pipeline_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Trigger model retraining for a pipeline"""
    # Check if pipeline exists
    pipeline_query = """
    MATCH (p:MLPipeline)
    WHERE p.id = $pipeline_id AND p.user_id = $user_id
    RETURN p
    """

    pipeline_result = neo4j_conn.execute_query(pipeline_query, {
        "pipeline_id": pipeline_id,
        "user_id": current_user.id
    })

    if not pipeline_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )

    # Create retraining event
    retrain_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    create_retrain_query = """
    CREATE (r:RetrainingEvent {
        id: $id,
        trigger_reason: $trigger_reason,
        status: $status,
        pipeline_id: $pipeline_id,
        created_at: $created_at
    })
    RETURN r
    """

    neo4j_conn.execute_write_query(create_retrain_query, {
        "id": retrain_id,
        "trigger_reason": "Manual trigger",
        "status": "pending",
        "pipeline_id": pipeline_id,
        "created_at": now
    })

    # TODO: Implement actual retraining logic
    # This would typically queue a Celery task

    return {
        "message": "Retraining triggered successfully",
        "retraining_id": retrain_id
    }


@router.get("/pipelines/{pipeline_id}/status", response_model=PipelineStatusResponse)
def get_pipeline_status(
    pipeline_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Get current pipeline health and status"""
    # Check if pipeline exists
    pipeline_query = """
    MATCH (p:MLPipeline)
    WHERE p.id = $pipeline_id AND p.user_id = $user_id
    RETURN p
    """

    pipeline_result = neo4j_conn.execute_query(pipeline_query, {
        "pipeline_id": pipeline_id,
        "user_id": current_user.id
    })

    if not pipeline_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found"
        )

    # Get latest metrics
    metrics_query = """
    MATCH (m:DriftMetric)
    WHERE m.pipeline_id = $pipeline_id
    RETURN m.drift_type as drift_type, m.metric_value as metric_value,
           m.threshold as threshold, m.created_at as created_at
    ORDER BY m.created_at DESC LIMIT 5
    """

    latest_metrics = neo4j_conn.execute_query(metrics_query, {
        "pipeline_id": pipeline_id
    })

    # Get last retraining event
    retrain_query = """
    MATCH (r:RetrainingEvent)
    WHERE r.pipeline_id = $pipeline_id
    RETURN r.created_at as created_at
    ORDER BY r.created_at DESC LIMIT 1
    """

    last_retrain_result = neo4j_conn.execute_query(retrain_query, {
        "pipeline_id": pipeline_id
    })

    last_retrain = last_retrain_result[0] if last_retrain_result else None

    # Calculate health score (mock implementation)
    health_score = 85.0  # TODO: Implement actual health calculation

    return {
        "pipeline_id": pipeline_id,
        "status": pipeline_result[0]["status"],
        "last_retrain": last_retrain["created_at"] if last_retrain else None,
        "latest_metrics": [
            {
                "drift_type": metric["drift_type"],
                "metric_value": metric["metric_value"],
                "threshold": metric["threshold"],
                "timestamp": metric["created_at"]
            }
            for metric in latest_metrics
        ],
        "health_score": health_score
    }
