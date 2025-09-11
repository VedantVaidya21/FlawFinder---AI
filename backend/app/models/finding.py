from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from ..core.neo4j import get_neo4j


class FindingSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FindingType(str, Enum):
    BOTTLENECK = "bottleneck"
    REDUNDANCY = "redundancy"
    MANUAL_HANDOFF = "manual_handoff"
    WAIT_TIME = "wait_time"
    REWORK_LOOP = "rework_loop"
    DATA_DUPLICATION = "data_duplication"
    INEFFICIENT_PROCESS = "inefficient_process"


class FindingBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: FindingSeverity
    finding_type: FindingType
    impact_score: float  # 0-100
    node_id: Optional[str] = None  # Reference to graph node
    tags: Optional[List[str]] = None  # Array of tags
    recommendations: Optional[List[str]] = None  # Array of recommendations
    process_flow_id: str


class FindingCreate(FindingBase):
    pass


class FindingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[FindingSeverity] = None
    finding_type: Optional[FindingType] = None
    impact_score: Optional[float] = None
    node_id: Optional[str] = None
    tags: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None


class Finding(FindingBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class FindingService:
    """Neo4j data access layer for Finding operations"""

    @staticmethod
    def create_finding(finding_data: FindingCreate) -> Optional[Finding]:
        """Create a new finding in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (f:Finding {
            id: randomUUID(),
            title: $title,
            description: $description,
            severity: $severity,
            finding_type: $finding_type,
            impact_score: $impact_score,
            node_id: $node_id,
            tags: $tags,
            recommendations: $recommendations,
            process_flow_id: $process_flow_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN f
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "title": finding_data.title,
                "description": finding_data.description,
                "severity": finding_data.severity.value,
                "finding_type": finding_data.finding_type.value,
                "impact_score": finding_data.impact_score,
                "node_id": finding_data.node_id,
                "tags": finding_data.tags,
                "recommendations": finding_data.recommendations,
                "process_flow_id": finding_data.process_flow_id
            })

            if result:
                record = result[0]["f"]
                return Finding(
                    id=record["id"],
                    title=record["title"],
                    description=record.get("description"),
                    severity=FindingSeverity(record["severity"]),
                    finding_type=FindingType(record["finding_type"]),
                    impact_score=record["impact_score"],
                    node_id=record.get("node_id"),
                    tags=record.get("tags"),
                    recommendations=record.get("recommendations"),
                    process_flow_id=record["process_flow_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating finding: {e}")
        return None

    @staticmethod
    def get_finding_by_id(finding_id: str) -> Optional[Finding]:
        """Get finding by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (f:Finding {id: $id, is_active: true})
        RETURN f
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": finding_id})
            if result:
                record = result[0]["f"]
                return Finding(
                    id=record["id"],
                    title=record["title"],
                    description=record.get("description"),
                    severity=FindingSeverity(record["severity"]),
                    finding_type=FindingType(record["finding_type"]),
                    impact_score=record["impact_score"],
                    node_id=record.get("node_id"),
                    tags=record.get("tags"),
                    recommendations=record.get("recommendations"),
                    process_flow_id=record["process_flow_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting finding by ID: {e}")
        return None

    @staticmethod
    def update_finding(finding_id: str, finding_data: FindingUpdate) -> Optional[Finding]:
        """Update finding information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["f.updated_at = datetime()"]
        params = {"id": finding_id}

        if finding_data.title is not None:
            set_parts.append("f.title = $title")
            params["title"] = finding_data.title
        if finding_data.description is not None:
            set_parts.append("f.description = $description")
            params["description"] = finding_data.description
        if finding_data.severity is not None:
            set_parts.append("f.severity = $severity")
            params["severity"] = finding_data.severity.value
        if finding_data.finding_type is not None:
            set_parts.append("f.finding_type = $finding_type")
            params["finding_type"] = finding_data.finding_type.value
        if finding_data.impact_score is not None:
            set_parts.append("f.impact_score = $impact_score")
            params["impact_score"] = finding_data.impact_score
        if finding_data.node_id is not None:
            set_parts.append("f.node_id = $node_id")
            params["node_id"] = finding_data.node_id
        if finding_data.tags is not None:
            set_parts.append("f.tags = $tags")
            params["tags"] = finding_data.tags
        if finding_data.recommendations is not None:
            set_parts.append("f.recommendations = $recommendations")
            params["recommendations"] = finding_data.recommendations

        query = f"""
        MATCH (f:Finding {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN f
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["f"]
                return Finding(
                    id=record["id"],
                    title=record["title"],
                    description=record.get("description"),
                    severity=FindingSeverity(record["severity"]),
                    finding_type=FindingType(record["finding_type"]),
                    impact_score=record["impact_score"],
                    node_id=record.get("node_id"),
                    tags=record.get("tags"),
                    recommendations=record.get("recommendations"),
                    process_flow_id=record["process_flow_id"],
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating finding: {e}")
        return None

    @staticmethod
    def delete_finding(finding_id: str) -> bool:
        """Soft delete finding by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (f:Finding {id: $id, is_active: true})
        SET f.is_active = false, f.updated_at = datetime()
        RETURN count(f) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": finding_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting finding: {e}")
        return False

    @staticmethod
    def get_findings_by_process_flow(process_flow_id: str, skip: int = 0, limit: int = 100) -> List[Finding]:
        """Get all findings for a specific process flow with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (f:Finding {process_flow_id: $process_flow_id, is_active: true})
        RETURN f
        ORDER BY f.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"process_flow_id": process_flow_id, "skip": skip, "limit": limit})
            findings = []
            for record in result:
                finding_data = record["f"]
                findings.append(Finding(
                    id=finding_data["id"],
                    title=finding_data["title"],
                    description=finding_data.get("description"),
                    severity=FindingSeverity(finding_data["severity"]),
                    finding_type=FindingType(finding_data["finding_type"]),
                    impact_score=finding_data["impact_score"],
                    node_id=finding_data.get("node_id"),
                    tags=finding_data.get("tags"),
                    recommendations=finding_data.get("recommendations"),
                    process_flow_id=finding_data["process_flow_id"],
                    created_at=finding_data["created_at"].to_native(),
                    updated_at=finding_data["updated_at"].to_native(),
                    is_active=finding_data["is_active"]
                ))
            return findings
        except Exception as e:
            print(f"Error getting findings by process flow: {e}")
        return []

    @staticmethod
    def get_findings_by_severity(severity: FindingSeverity, skip: int = 0, limit: int = 100) -> List[Finding]:
        """Get all findings of a specific severity with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (f:Finding {severity: $severity, is_active: true})
        RETURN f
        ORDER BY f.impact_score DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"severity": severity.value, "skip": skip, "limit": limit})
            findings = []
            for record in result:
                finding_data = record["f"]
                findings.append(Finding(
                    id=finding_data["id"],
                    title=finding_data["title"],
                    description=finding_data.get("description"),
                    severity=FindingSeverity(finding_data["severity"]),
                    finding_type=FindingType(finding_data["finding_type"]),
                    impact_score=finding_data["impact_score"],
                    node_id=finding_data.get("node_id"),
                    tags=finding_data.get("tags"),
                    recommendations=finding_data.get("recommendations"),
                    process_flow_id=finding_data["process_flow_id"],
                    created_at=finding_data["created_at"].to_native(),
                    updated_at=finding_data["updated_at"].to_native(),
                    is_active=finding_data["is_active"]
                ))
            return findings
        except Exception as e:
            print(f"Error getting findings by severity: {e}")
        return []

    @staticmethod
    def get_findings_by_type(finding_type: FindingType, skip: int = 0, limit: int = 100) -> List[Finding]:
        """Get all findings of a specific type with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (f:Finding {finding_type: $finding_type, is_active: true})
        RETURN f
        ORDER BY f.impact_score DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"finding_type": finding_type.value, "skip": skip, "limit": limit})
            findings = []
            for record in result:
                finding_data = record["f"]
                findings.append(Finding(
                    id=finding_data["id"],
                    title=finding_data["title"],
                    description=finding_data.get("description"),
                    severity=FindingSeverity(finding_data["severity"]),
                    finding_type=FindingType(finding_data["finding_type"]),
                    impact_score=finding_data["impact_score"],
                    node_id=finding_data.get("node_id"),
                    tags=finding_data.get("tags"),
                    recommendations=finding_data.get("recommendations"),
                    process_flow_id=finding_data["process_flow_id"],
                    created_at=finding_data["created_at"].to_native(),
                    updated_at=finding_data["updated_at"].to_native(),
                    is_active=finding_data["is_active"]
                ))
            return findings
        except Exception as e:
            print(f"Error getting findings by type: {e}")
        return []
