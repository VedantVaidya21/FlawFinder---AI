from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from ..core.neo4j import get_neo4j


class FlowStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessFlowBase(BaseModel):
    name: str
    description: Optional[str] = None
    raw_input: str  # Original text/diagram input
    parsed_graph: Optional[Dict[str, Any]] = None  # Parsed graph structure
    version: int = 1
    status: FlowStatus = FlowStatus.DRAFT
    brutality_score: Optional[float] = None
    user_id: str
    organization_id: Optional[str] = None


class ProcessFlowCreate(ProcessFlowBase):
    pass


class ProcessFlowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    raw_input: Optional[str] = None
    parsed_graph: Optional[Dict[str, Any]] = None
    version: Optional[int] = None
    status: Optional[FlowStatus] = None
    brutality_score: Optional[float] = None
    organization_id: Optional[str] = None


class ProcessFlow(ProcessFlowBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class ProcessFlowService:
    """Neo4j data access layer for ProcessFlow operations"""

    @staticmethod
    def create_process_flow(flow_data: ProcessFlowCreate) -> Optional[ProcessFlow]:
        """Create a new process flow in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (pf:ProcessFlow {
            id: randomUUID(),
            name: $name,
            description: $description,
            raw_input: $raw_input,
            parsed_graph: $parsed_graph,
            version: $version,
            status: $status,
            brutality_score: $brutality_score,
            user_id: $user_id,
            organization_id: $organization_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN pf
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "name": flow_data.name,
                "description": flow_data.description,
                "raw_input": flow_data.raw_input,
                "parsed_graph": flow_data.parsed_graph,
                "version": flow_data.version,
                "status": flow_data.status.value,
                "brutality_score": flow_data.brutality_score,
                "user_id": flow_data.user_id,
                "organization_id": flow_data.organization_id
            })

            if result:
                record = result[0]["pf"]
                return ProcessFlow(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    raw_input=record["raw_input"],
                    parsed_graph=record.get("parsed_graph"),
                    version=record.get("version", 1),
                    status=FlowStatus(record["status"]),
                    brutality_score=record.get("brutality_score"),
                    user_id=record["user_id"],
                    organization_id=record.get("organization_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating process flow: {e}")
        return None

    @staticmethod
    def get_process_flow_by_id(flow_id: str) -> Optional[ProcessFlow]:
        """Get process flow by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (pf:ProcessFlow {id: $id, is_active: true})
        RETURN pf
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": flow_id})
            if result:
                record = result[0]["pf"]
                return ProcessFlow(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    raw_input=record["raw_input"],
                    parsed_graph=record.get("parsed_graph"),
                    version=record.get("version", 1),
                    status=FlowStatus(record["status"]),
                    brutality_score=record.get("brutality_score"),
                    user_id=record["user_id"],
                    organization_id=record.get("organization_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting process flow by ID: {e}")
        return None

    @staticmethod
    def update_process_flow(flow_id: str, flow_data: ProcessFlowUpdate) -> Optional[ProcessFlow]:
        """Update process flow information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["pf.updated_at = datetime()"]
        params = {"id": flow_id}

        if flow_data.name is not None:
            set_parts.append("pf.name = $name")
            params["name"] = flow_data.name
        if flow_data.description is not None:
            set_parts.append("pf.description = $description")
            params["description"] = flow_data.description
        if flow_data.raw_input is not None:
            set_parts.append("pf.raw_input = $raw_input")
            params["raw_input"] = flow_data.raw_input
        if flow_data.parsed_graph is not None:
            set_parts.append("pf.parsed_graph = $parsed_graph")
            params["parsed_graph"] = flow_data.parsed_graph
        if flow_data.version is not None:
            set_parts.append("pf.version = $version")
            params["version"] = flow_data.version
        if flow_data.status is not None:
            set_parts.append("pf.status = $status")
            params["status"] = flow_data.status.value
        if flow_data.brutality_score is not None:
            set_parts.append("pf.brutality_score = $brutality_score")
            params["brutality_score"] = flow_data.brutality_score
        if flow_data.organization_id is not None:
            set_parts.append("pf.organization_id = $organization_id")
            params["organization_id"] = flow_data.organization_id

        query = f"""
        MATCH (pf:ProcessFlow {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN pf
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["pf"]
                return ProcessFlow(
                    id=record["id"],
                    name=record["name"],
                    description=record.get("description"),
                    raw_input=record["raw_input"],
                    parsed_graph=record.get("parsed_graph"),
                    version=record.get("version", 1),
                    status=FlowStatus(record["status"]),
                    brutality_score=record.get("brutality_score"),
                    user_id=record["user_id"],
                    organization_id=record.get("organization_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating process flow: {e}")
        return None

    @staticmethod
    def delete_process_flow(flow_id: str) -> bool:
        """Soft delete process flow by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (pf:ProcessFlow {id: $id, is_active: true})
        SET pf.is_active = false, pf.updated_at = datetime()
        RETURN count(pf) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": flow_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting process flow: {e}")
        return False

    @staticmethod
    def get_process_flows_by_user(user_id: str, skip: int = 0, limit: int = 100) -> List[ProcessFlow]:
        """Get all process flows for a specific user with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (pf:ProcessFlow {user_id: $user_id, is_active: true})
        RETURN pf
        ORDER BY pf.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"user_id": user_id, "skip": skip, "limit": limit})
            flows = []
            for record in result:
                flow_data = record["pf"]
                flows.append(ProcessFlow(
                    id=flow_data["id"],
                    name=flow_data["name"],
                    description=flow_data.get("description"),
                    raw_input=flow_data["raw_input"],
                    parsed_graph=flow_data.get("parsed_graph"),
                    version=flow_data.get("version", 1),
                    status=FlowStatus(flow_data["status"]),
                    brutality_score=flow_data.get("brutality_score"),
                    user_id=flow_data["user_id"],
                    organization_id=flow_data.get("organization_id"),
                    created_at=flow_data["created_at"].to_native(),
                    updated_at=flow_data["updated_at"].to_native(),
                    is_active=flow_data["is_active"]
                ))
            return flows
        except Exception as e:
            print(f"Error getting process flows by user: {e}")
        return []

    @staticmethod
    def get_process_flows_by_organization(org_id: str, skip: int = 0, limit: int = 100) -> List[ProcessFlow]:
        """Get all process flows for a specific organization with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (pf:ProcessFlow {organization_id: $organization_id, is_active: true})
        RETURN pf
        ORDER BY pf.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"organization_id": org_id, "skip": skip, "limit": limit})
            flows = []
            for record in result:
                flow_data = record["pf"]
                flows.append(ProcessFlow(
                    id=flow_data["id"],
                    name=flow_data["name"],
                    description=flow_data.get("description"),
                    raw_input=flow_data["raw_input"],
                    parsed_graph=flow_data.get("parsed_graph"),
                    version=flow_data.get("version", 1),
                    status=FlowStatus(flow_data["status"]),
                    brutality_score=flow_data.get("brutality_score"),
                    user_id=flow_data["user_id"],
                    organization_id=flow_data.get("organization_id"),
                    created_at=flow_data["created_at"].to_native(),
                    updated_at=flow_data["updated_at"].to_native(),
                    is_active=flow_data["is_active"]
                ))
            return flows
        except Exception as e:
            print(f"Error getting process flows by organization: {e}")
        return []

    @staticmethod
    def get_process_flows_by_status(status: FlowStatus, skip: int = 0, limit: int = 100) -> List[ProcessFlow]:
        """Get all process flows of a specific status with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (pf:ProcessFlow {status: $status, is_active: true})
        RETURN pf
        ORDER BY pf.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"status": status.value, "skip": skip, "limit": limit})
            flows = []
            for record in result:
                flow_data = record["pf"]
                flows.append(ProcessFlow(
                    id=flow_data["id"],
                    name=flow_data["name"],
                    description=flow_data.get("description"),
                    raw_input=flow_data["raw_input"],
                    parsed_graph=flow_data.get("parsed_graph"),
                    version=flow_data.get("version", 1),
                    status=FlowStatus(flow_data["status"]),
                    brutality_score=flow_data.get("brutality_score"),
                    user_id=flow_data["user_id"],
                    organization_id=flow_data.get("organization_id"),
                    created_at=flow_data["created_at"].to_native(),
                    updated_at=flow_data["updated_at"].to_native(),
                    is_active=flow_data["is_active"]
                ))
            return flows
        except Exception as e:
            print(f"Error getting process flows by status: {e}")
        return []
