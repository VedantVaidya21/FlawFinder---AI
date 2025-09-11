from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from ..core.neo4j import get_neo4j


class PipelineStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class DriftType(str, Enum):
    DATA_DRIFT = "data_drift"
    CONCEPT_DRIFT = "concept_drift"
    LABEL_DRIFT = "label_drift"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class MLPipelineBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_path: Optional[str] = None
    metrics_endpoint: Optional[str] = None
    status: PipelineStatus = PipelineStatus.ACTIVE
    pipeline_metadata: Optional[Dict[str, Any]] = None
    user_id: str


class MLPipelineCreate(MLPipelineBase):
    pass


class MLPipelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model_path: Optional[str] = None
    metrics_endpoint: Optional[str] = None
    status: Optional[PipelineStatus] = None
    pipeline_metadata: Optional[Dict[str, Any]] = None


class MLPipeline(MLPipelineBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class DriftMetricBase(BaseModel):
    drift_type: DriftType
    metric_value: float
    threshold: float
    timestamp: datetime
    drift_metadata: Optional[Dict[str, Any]] = None
    pipeline_id: str


class DriftMetricCreate(DriftMetricBase):
    pass


class DriftMetricUpdate(BaseModel):
    drift_type: Optional[DriftType] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    timestamp: Optional[datetime] = None
    drift_metadata: Optional[Dict[str, Any]] = None


class DriftMetric(DriftMetricBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class RetrainingEventBase(BaseModel):
    trigger_reason: str
    status: TaskStatus = TaskStatus.PENDING
    model_version: Optional[str] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    retraining_metadata: Optional[Dict[str, Any]] = None
    pipeline_id: str


class RetrainingEventCreate(RetrainingEventBase):
    pass


class RetrainingEventUpdate(BaseModel):
    trigger_reason: Optional[str] = None
    status: Optional[TaskStatus] = None
    model_version: Optional[str] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    retraining_metadata: Optional[Dict[str, Any]] = None


class RetrainingEvent(RetrainingEventBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class MLPipelineService:
    """Neo4j data access layer for MLPipeline operations"""

    @staticmethod
    def create_pipeline(pipeline_data: MLPipelineCreate) -> Optional[MLPipeline]:
        """Create a new ML pipeline in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (p:MLPipeline {
            id: randomUUID(),
            name: $name,
            description: $description,
            model_path: $model_path,
            metrics_endpoint: $metrics_endpoint,
            status: $status,
            pipeline_metadata: $pipeline_metadata,
            user_id: $user_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN p
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "name": pipeline_data.name,
                "description": pipeline_data.description,
                "model_path": pipeline_data.model_path,
                "metrics_endpoint": pipeline_data.metrics_endpoint,
                "status": pipeline_data.status.value,
                "pipeline_metadata": pipeline_data.pipeline_metadata,
                "user_id": pipeline_data.user_id
            })

            if result:
                record = result[0]["p"]
                return MLPipeline(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    model_path=record.get("model_path"),
                    metrics_endpoint=record.get("metrics_endpoint"),
                    status=PipelineStatus(record["status"]),
                    pipeline_metadata=record.get("pipeline_metadata"),
                    user_id=record["user_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating pipeline: {e}")
        return None

    @staticmethod
    def get_pipeline_by_id(pipeline_id: str) -> Optional[MLPipeline]:
        """Get pipeline by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (p:MLPipeline {id: $id, is_active: true})
        RETURN p
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": pipeline_id})
            if result:
                record = result[0]["p"]
                return MLPipeline(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    model_path=record.get("model_path"),
                    metrics_endpoint=record.get("metrics_endpoint"),
                    status=PipelineStatus(record["status"]),
                    pipeline_metadata=record.get("pipeline_metadata"),
                    user_id=record["user_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting pipeline by ID: {e}")
        return None

    @staticmethod
    def update_pipeline(pipeline_id: str, pipeline_data: MLPipelineUpdate) -> Optional[MLPipeline]:
        """Update pipeline information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["p.updated_at = datetime()"]
        params = {"id": pipeline_id}

        if pipeline_data.name is not None:
            set_parts.append("p.name = $name")
            params["name"] = pipeline_data.name
        if pipeline_data.description is not None:
            set_parts.append("p.description = $description")
            params["description"] = pipeline_data.description
        if pipeline_data.model_path is not None:
            set_parts.append("p.model_path = $model_path")
            params["model_path"] = pipeline_data.model_path
        if pipeline_data.metrics_endpoint is not None:
            set_parts.append("p.metrics_endpoint = $metrics_endpoint")
            params["metrics_endpoint"] = pipeline_data.metrics_endpoint
        if pipeline_data.status is not None:
            set_parts.append("p.status = $status")
            params["status"] = pipeline_data.status.value
        if pipeline_data.pipeline_metadata is not None:
            set_parts.append("p.pipeline_metadata = $pipeline_metadata")
            params["pipeline_metadata"] = pipeline_data.pipeline_metadata

        query = f"""
        MATCH (p:MLPipeline {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN p
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["p"]
                return MLPipeline(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    model_path=record.get("model_path"),
                    metrics_endpoint=record.get("metrics_endpoint"),
                    status=PipelineStatus(record["status"]),
                    pipeline_metadata=record.get("pipeline_metadata"),
                    user_id=record["user_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating pipeline: {e}")
        return None

    @staticmethod
    def delete_pipeline(pipeline_id: str) -> bool:
        """Soft delete pipeline by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (p:MLPipeline {id: $id, is_active: true})
        SET p.is_active = false, p.updated_at = datetime()
        RETURN count(p) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": pipeline_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting pipeline: {e}")
        return False

    @staticmethod
    def get_pipelines_by_user(user_id: str, skip: int = 0, limit: int = 100) -> List[MLPipeline]:
        """Get all pipelines for a specific user with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (p:MLPipeline {user_id: $user_id, is_active: true})
        RETURN p
        ORDER BY p.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"user_id": user_id, "skip": skip, "limit": limit})
            pipelines = []
            for record in result:
                pipeline_data = record["p"]
                pipelines.append(MLPipeline(
                    id=pipeline_data["id"],
                    name=pipeline_data["name"],
                    description=pipeline_data.get("description"),
                    model_path=pipeline_data.get("model_path"),
                    metrics_endpoint=pipeline_data.get("metrics_endpoint"),
                    status=PipelineStatus(pipeline_data["status"]),
                    pipeline_metadata=pipeline_data.get("pipeline_metadata"),
                    user_id=pipeline_data["user_id"],
                    created_at=pipeline_data["created_at"].to_native(),
                    updated_at=pipeline_data["updated_at"].to_native(),
                    is_active=pipeline_data["is_active"]
                ))
            return pipelines
        except Exception as e:
            print(f"Error getting pipelines by user: {e}")
        return []

    @staticmethod
    def get_pipelines_by_status(status: PipelineStatus, skip: int = 0, limit: int = 100) -> List[MLPipeline]:
        """Get all pipelines with a specific status with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (p:MLPipeline {status: $status, is_active: true})
        RETURN p
        ORDER BY p.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"status": status.value, "skip": skip, "limit": limit})
            pipelines = []
            for record in result:
                pipeline_data = record["p"]
                pipelines.append(MLPipeline(
                    id=pipeline_data["id"],
                    name=pipeline_data["name"],
                    description=pipeline_data.get("description"),
                    model_path=pipeline_data.get("model_path"),
                    metrics_endpoint=pipeline_data.get("metrics_endpoint"),
                    status=PipelineStatus(pipeline_data["status"]),
                    pipeline_metadata=pipeline_data.get("pipeline_metadata"),
                    user_id=pipeline_data["user_id"],
                    created_at=pipeline_data["created_at"].to_native(),
                    updated_at=pipeline_data["updated_at"].to_native(),
                    is_active=pipeline_data["is_active"]
                ))
            return pipelines
        except Exception as e:
            print(f"Error getting pipelines by status: {e}")
        return []


class DriftMetricService:
    """Neo4j data access layer for DriftMetric operations"""

    @staticmethod
    def create_drift_metric(metric_data: DriftMetricCreate) -> Optional[DriftMetric]:
        """Create a new drift metric in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (dm:DriftMetric {
            id: randomUUID(),
            drift_type: $drift_type,
            metric_value: $metric_value,
            threshold: $threshold,
            timestamp: datetime($timestamp),
            drift_metadata: $drift_metadata,
            pipeline_id: $pipeline_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN dm
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "drift_type": metric_data.drift_type.value,
                "metric_value": metric_data.metric_value,
                "threshold": metric_data.threshold,
                "timestamp": metric_data.timestamp.isoformat(),
                "drift_metadata": metric_data.drift_metadata,
                "pipeline_id": metric_data.pipeline_id
            })

            if result:
                record = result[0]["dm"]
                return DriftMetric(
                    id=record["id"],
                    drift_type=DriftType(record["drift_type"]),
                    metric_value=record["metric_value"],
                    threshold=record["threshold"],
                    timestamp=record["timestamp"].to_native(),
                    drift_metadata=record.get("drift_metadata"),
                    pipeline_id=record["pipeline_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating drift metric: {e}")
        return None

    @staticmethod
    def get_drift_metrics_by_pipeline(pipeline_id: str, skip: int = 0, limit: int = 100) -> List[DriftMetric]:
        """Get all drift metrics for a specific pipeline with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (dm:DriftMetric {pipeline_id: $pipeline_id, is_active: true})
        RETURN dm
        ORDER BY dm.timestamp DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"pipeline_id": pipeline_id, "skip": skip, "limit": limit})
            metrics = []
            for record in result:
                metric_data = record["dm"]
                metrics.append(DriftMetric(
                    id=metric_data["id"],
                    drift_type=DriftType(metric_data["drift_type"]),
                    metric_value=metric_data["metric_value"],
                    threshold=metric_data["threshold"],
                    timestamp=metric_data["timestamp"].to_native(),
                    drift_metadata=metric_data.get("drift_metadata"),
                    pipeline_id=metric_data["pipeline_id"],
                    created_at=metric_data["created_at"].to_native(),
                    updated_at=metric_data["updated_at"].to_native(),
                    is_active=metric_data["is_active"]
                ))
            return metrics
        except Exception as e:
            print(f"Error getting drift metrics by pipeline: {e}")
        return []

    @staticmethod
    def get_drift_metrics_above_threshold(threshold: float, skip: int = 0, limit: int = 100) -> List[DriftMetric]:
        """Get all drift metrics above a certain threshold with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (dm:DriftMetric {is_active: true})
        WHERE dm.metric_value >= $threshold
        RETURN dm
        ORDER BY dm.metric_value DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"threshold": threshold, "skip": skip, "limit": limit})
            metrics = []
            for record in result:
                metric_data = record["dm"]
                metrics.append(DriftMetric(
                    id=metric_data["id"],
                    drift_type=DriftType(metric_data["drift_type"]),
                    metric_value=metric_data["metric_value"],
                    threshold=metric_data["threshold"],
                    timestamp=metric_data["timestamp"].to_native(),
                    drift_metadata=metric_data.get("drift_metadata"),
                    pipeline_id=metric_data["pipeline_id"],
                    created_at=metric_data["created_at"].to_native(),
                    updated_at=metric_data["updated_at"].to_native(),
                    is_active=metric_data["is_active"]
                ))
            return metrics
        except Exception as e:
            print(f"Error getting drift metrics above threshold: {e}")
        return []


class RetrainingEventService:
    """Neo4j data access layer for RetrainingEvent operations"""

    @staticmethod
    def create_retraining_event(event_data: RetrainingEventCreate) -> Optional[RetrainingEvent]:
        """Create a new retraining event in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (re:RetrainingEvent {
            id: randomUUID(),
            trigger_reason: $trigger_reason,
            status: $status,
            model_version: $model_version,
            performance_metrics: $performance_metrics,
            retraining_metadata: $retraining_metadata,
            pipeline_id: $pipeline_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN re
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "trigger_reason": event_data.trigger_reason,
                "status": event_data.status.value,
                "model_version": event_data.model_version,
                "performance_metrics": event_data.performance_metrics,
                "retraining_metadata": event_data.retraining_metadata,
                "pipeline_id": event_data.pipeline_id
            })

            if result:
                record = result[0]["re"]
                return RetrainingEvent(
                    id=record["id"],
                    trigger_reason=record["trigger_reason"],
                    status=TaskStatus(record["status"]),
                    model_version=record.get("model_version"),
                    performance_metrics=record.get("performance_metrics"),
                    retraining_metadata=record.get("retraining_metadata"),
                    pipeline_id=record["pipeline_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating retraining event: {e}")
        return None

    @staticmethod
    def get_retraining_events_by_pipeline(pipeline_id: str, skip: int = 0, limit: int = 100) -> List[RetrainingEvent]:
        """Get all retraining events for a specific pipeline with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (re:RetrainingEvent {pipeline_id: $pipeline_id, is_active: true})
        RETURN re
        ORDER BY re.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"pipeline_id": pipeline_id, "skip": skip, "limit": limit})
            events = []
            for record in result:
                event_data = record["re"]
                events.append(RetrainingEvent(
                    id=event_data["id"],
                    trigger_reason=event_data["trigger_reason"],
                    status=TaskStatus(event_data["status"]),
                    model_version=event_data.get("model_version"),
                    performance_metrics=event_data.get("performance_metrics"),
                    retraining_metadata=event_data.get("retraining_metadata"),
                    pipeline_id=event_data["pipeline_id"],
                    created_at=event_data["created_at"].to_native(),
                    updated_at=event_data["updated_at"].to_native(),
                    is_active=event_data["is_active"]
                ))
            return events
        except Exception as e:
            print(f"Error getting retraining events by pipeline: {e}")
        return []

    @staticmethod
    def get_retraining_events_by_status(status: TaskStatus, skip: int = 0, limit: int = 100) -> List[RetrainingEvent]:
        """Get all retraining events with a specific status with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (re:RetrainingEvent {status: $status, is_active: true})
        RETURN re
        ORDER BY re.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"status": status.value, "skip": skip, "limit": limit})
            events = []
            for record in result:
                event_data = record["re"]
                events.append(RetrainingEvent(
                    id=event_data["id"],
                    trigger_reason=event_data["trigger_reason"],
                    status=TaskStatus(event_data["status"]),
                    model_version=event_data.get("model_version"),
                    performance_metrics=event_data.get("performance_metrics"),
                    retraining_metadata=event_data.get("retraining_metadata"),
                    pipeline_id=event_data["pipeline_id"],
                    created_at=event_data["created_at"].to_native(),
                    updated_at=event_data["updated_at"].to_native(),
                    is_active=event_data["is_active"]
                ))
            return events
        except Exception as e:
            print(f"Error getting retraining events by status: {e}")
        return []
