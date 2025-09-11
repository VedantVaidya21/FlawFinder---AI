from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from ..core.neo4j import get_neo4j


class TaskType(str, Enum):
    FLOW_PARSING = "flow_parsing"
    SCORE_CALCULATION = "score_calculation"
    REPORT_GENERATION = "report_generation"
    MODEL_TRAINING = "model_training"
    DATA_DRIFT_MONITORING = "data_drift_monitoring"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskBase(BaseModel):
    task_type: TaskType
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0  # 0-100
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    logs: Optional[List[str]] = None
    task_metadata: Optional[Dict[str, Any]] = None
    user_id: str
    process_flow_id: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    task_type: Optional[TaskType] = None
    status: Optional[TaskStatus] = None
    progress: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    logs: Optional[List[str]] = None
    task_metadata: Optional[Dict[str, Any]] = None
    process_flow_id: Optional[str] = None


class Task(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class TaskService:
    """Neo4j data access layer for Task operations"""

    @staticmethod
    def create_task(task_data: TaskCreate) -> Optional[Task]:
        """Create a new task in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (t:Task {
            id: randomUUID(),
            task_type: $task_type,
            status: $status,
            progress: $progress,
            result: $result,
            error_message: $error_message,
            logs: $logs,
            task_metadata: $task_metadata,
            user_id: $user_id,
            process_flow_id: $process_flow_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN t
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "task_type": task_data.task_type.value,
                "status": task_data.status.value,
                "progress": task_data.progress,
                "result": task_data.result,
                "error_message": task_data.error_message,
                "logs": task_data.logs,
                "task_metadata": task_data.task_metadata,
                "user_id": task_data.user_id,
                "process_flow_id": task_data.process_flow_id
            })

            if result:
                record = result[0]["t"]
                return Task(
                    id=record["id"],
                    task_type=TaskType(record["task_type"]),
                    status=TaskStatus(record["status"]),
                    progress=record.get("progress", 0.0),
                    result=record.get("result"),
                    error_message=record.get("error_message"),
                    logs=record.get("logs"),
                    task_metadata=record.get("task_metadata"),
                    user_id=record["user_id"],
                    process_flow_id=record.get("process_flow_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating task: {e}")
        return None

    @staticmethod
    def get_task_by_id(task_id: str) -> Optional[Task]:
        """Get task by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (t:Task {id: $id, is_active: true})
        RETURN t
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": task_id})
            if result:
                record = result[0]["t"]
                return Task(
                    id=record["id"],
                    task_type=TaskType(record["task_type"]),
                    status=TaskStatus(record["status"]),
                    progress=record.get("progress", 0.0),
                    result=record.get("result"),
                    error_message=record.get("error_message"),
                    logs=record.get("logs"),
                    task_metadata=record.get("task_metadata"),
                    user_id=record["user_id"],
                    process_flow_id=record.get("process_flow_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting task by ID: {e}")
        return None

    @staticmethod
    def update_task(task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Update task information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["t.updated_at = datetime()"]
        params = {"id": task_id}

        if task_data.task_type is not None:
            set_parts.append("t.task_type = $task_type")
            params["task_type"] = task_data.task_type.value
        if task_data.status is not None:
            set_parts.append("t.status = $status")
            params["status"] = task_data.status.value
        if task_data.progress is not None:
            set_parts.append("t.progress = $progress")
            params["progress"] = task_data.progress
        if task_data.result is not None:
            set_parts.append("t.result = $result")
            params["result"] = task_data.result
        if task_data.error_message is not None:
            set_parts.append("t.error_message = $error_message")
            params["error_message"] = task_data.error_message
        if task_data.logs is not None:
            set_parts.append("t.logs = $logs")
            params["logs"] = task_data.logs
        if task_data.task_metadata is not None:
            set_parts.append("t.task_metadata = $task_metadata")
            params["task_metadata"] = task_data.task_metadata
        if task_data.process_flow_id is not None:
            set_parts.append("t.process_flow_id = $process_flow_id")
            params["process_flow_id"] = task_data.process_flow_id

        query = f"""
        MATCH (t:Task {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN t
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["t"]
                return Task(
                    id=record["id"],
                    task_type=TaskType(record["task_type"]),
                    status=TaskStatus(record["status"]),
                    progress=record.get("progress", 0.0),
                    result=record.get("result"),
                    error_message=record.get("error_message"),
                    logs=record.get("logs"),
                    task_metadata=record.get("task_metadata"),
                    user_id=record["user_id"],
                    process_flow_id=record.get("process_flow_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating task: {e}")
        return None

    @staticmethod
    def delete_task(task_id: str) -> bool:
        """Soft delete task by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (t:Task {id: $id, is_active: true})
        SET t.is_active = false, t.updated_at = datetime()
        RETURN count(t) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": task_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting task: {e}")
        return False

    @staticmethod
    def get_tasks_by_user(user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks for a specific user with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (t:Task {user_id: $user_id, is_active: true})
        RETURN t
        ORDER BY t.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"user_id": user_id, "skip": skip, "limit": limit})
            tasks = []
            for record in result:
                task_data = record["t"]
                tasks.append(Task(
                    id=task_data["id"],
                    task_type=TaskType(task_data["task_type"]),
                    status=TaskStatus(task_data["status"]),
                    progress=task_data.get("progress", 0.0),
                    result=task_data.get("result"),
                    error_message=task_data.get("error_message"),
                    logs=task_data.get("logs"),
                    task_metadata=task_data.get("task_metadata"),
                    user_id=task_data["user_id"],
                    process_flow_id=task_data.get("process_flow_id"),
                    created_at=task_data["created_at"].to_native(),
                    updated_at=task_data["updated_at"].to_native(),
                    is_active=task_data["is_active"]
                ))
            return tasks
        except Exception as e:
            print(f"Error getting tasks by user: {e}")
        return []

    @staticmethod
    def get_tasks_by_process_flow(process_flow_id: str) -> List[Task]:
        """Get all tasks for a specific process flow"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (t:Task {process_flow_id: $process_flow_id, is_active: true})
        RETURN t
        ORDER BY t.created_at DESC
        """

        try:
            result = neo4j_conn.execute_query(query, {"process_flow_id": process_flow_id})
            tasks = []
            for record in result:
                task_data = record["t"]
                tasks.append(Task(
                    id=task_data["id"],
                    task_type=TaskType(task_data["task_type"]),
                    status=TaskStatus(task_data["status"]),
                    progress=task_data.get("progress", 0.0),
                    result=task_data.get("result"),
                    error_message=task_data.get("error_message"),
                    logs=task_data.get("logs"),
                    task_metadata=task_data.get("task_metadata"),
                    user_id=task_data["user_id"],
                    process_flow_id=task_data.get("process_flow_id"),
                    created_at=task_data["created_at"].to_native(),
                    updated_at=task_data["updated_at"].to_native(),
                    is_active=task_data["is_active"]
                ))
            return tasks
        except Exception as e:
            print(f"Error getting tasks by process flow: {e}")
        return []

    @staticmethod
    def get_tasks_by_status(status: TaskStatus, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks of a specific status with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (t:Task {status: $status, is_active: true})
        RETURN t
        ORDER BY t.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"status": status.value, "skip": skip, "limit": limit})
            tasks = []
            for record in result:
                task_data = record["t"]
                tasks.append(Task(
                    id=task_data["id"],
                    task_type=TaskType(task_data["task_type"]),
                    status=TaskStatus(task_data["status"]),
                    progress=task_data.get("progress", 0.0),
                    result=task_data.get("result"),
                    error_message=task_data.get("error_message"),
                    logs=task_data.get("logs"),
                    task_metadata=task_data.get("task_metadata"),
                    user_id=task_data["user_id"],
                    process_flow_id=task_data.get("process_flow_id"),
                    created_at=task_data["created_at"].to_native(),
                    updated_at=task_data["updated_at"].to_native(),
                    is_active=task_data["is_active"]
                ))
            return tasks
        except Exception as e:
            print(f"Error getting tasks by status: {e}")
        return []
