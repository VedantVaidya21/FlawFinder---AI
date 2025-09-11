from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from ..core.neo4j import get_neo4j


class ReportType(str, Enum):
    CEO_REPORT = "ceo_report"
    DEPARTMENT_REPORT = "department_report"
    TECHNICAL_REPORT = "technical_report"


class ReportStatus(str, Enum):
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportBase(BaseModel):
    title: str
    report_type: ReportType
    status: ReportStatus = ReportStatus.GENERATING
    content: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None
    user_id: str
    process_flow_id: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    report_type: Optional[ReportType] = None
    status: Optional[ReportStatus] = None
    content: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None
    process_flow_id: Optional[str] = None


class Report(ReportBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class ReportService:
    """Neo4j data access layer for Report operations"""

    @staticmethod
    def create_report(report_data: ReportCreate) -> Optional[Report]:
        """Create a new report in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (r:Report {
            id: randomUUID(),
            title: $title,
            report_type: $report_type,
            status: $status,
            content: $content,
            file_url: $file_url,
            report_metadata: $report_metadata,
            user_id: $user_id,
            process_flow_id: $process_flow_id,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN r
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "title": report_data.title,
                "report_type": report_data.report_type.value,
                "status": report_data.status.value,
                "content": report_data.content,
                "file_url": report_data.file_url,
                "report_metadata": report_data.report_metadata,
                "user_id": report_data.user_id,
                "process_flow_id": report_data.process_flow_id
            })

            if result:
                record = result[0]["r"]
                return Report(
                    id=record["id"],
                    title=record["title"],
                    report_type=ReportType(record["report_type"]),
                    status=ReportStatus(record["status"]),
                    content=record.get("content"),
                    file_url=record.get("file_url"),
                    report_metadata=record.get("report_metadata"),
                    user_id=record["user_id"],
                    process_flow_id=record.get("process_flow_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating report: {e}")
        return None

    @staticmethod
    def get_report_by_id(report_id: str) -> Optional[Report]:
        """Get report by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (r:Report {id: $id, is_active: true})
        RETURN r
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": report_id})
            if result:
                record = result[0]["r"]
                return Report(
                    id=record["id"],
                    title=record["title"],
                    report_type=ReportType(record["report_type"]),
                    status=ReportStatus(record["status"]),
                    content=record.get("content"),
                    file_url=record.get("file_url"),
                    report_metadata=record.get("report_metadata"),
                    user_id=record["user_id"],
                    process_flow_id=record.get("process_flow_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting report by ID: {e}")
        return None

    @staticmethod
    def update_report(report_id: str, report_data: ReportUpdate) -> Optional[Report]:
        """Update report information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["r.updated_at = datetime()"]
        params = {"id": report_id}

        if report_data.title is not None:
            set_parts.append("r.title = $title")
            params["title"] = report_data.title
        if report_data.report_type is not None:
            set_parts.append("r.report_type = $report_type")
            params["report_type"] = report_data.report_type.value
        if report_data.status is not None:
            set_parts.append("r.status = $status")
            params["status"] = report_data.status.value
        if report_data.content is not None:
            set_parts.append("r.content = $content")
            params["content"] = report_data.content
        if report_data.file_url is not None:
            set_parts.append("r.file_url = $file_url")
            params["file_url"] = report_data.file_url
        if report_data.report_metadata is not None:
            set_parts.append("r.report_metadata = $report_metadata")
            params["report_metadata"] = report_data.report_metadata
        if report_data.process_flow_id is not None:
            set_parts.append("r.process_flow_id = $process_flow_id")
            params["process_flow_id"] = report_data.process_flow_id

        query = f"""
        MATCH (r:Report {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN r
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["r"]
                return Report(
                    id=record["id"],
                    title=record["title"],
                    report_type=ReportType(record["report_type"]),
                    status=ReportStatus(record["status"]),
                    content=record.get("content"),
                    file_url=record.get("file_url"),
                    report_metadata=record.get("report_metadata"),
                    user_id=record["user_id"],
                    process_flow_id=record.get("process_flow_id"),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating report: {e}")
        return None

    @staticmethod
    def delete_report(report_id: str) -> bool:
        """Soft delete report by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (r:Report {id: $id, is_active: true})
        SET r.is_active = false, r.updated_at = datetime()
        RETURN count(r) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": report_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting report: {e}")
        return False

    @staticmethod
    def get_reports_by_user(user_id: str, skip: int = 0, limit: int = 100) -> List[Report]:
        """Get all reports for a specific user with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (r:Report {user_id: $user_id, is_active: true})
        RETURN r
        ORDER BY r.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"user_id": user_id, "skip": skip, "limit": limit})
            reports = []
            for record in result:
                report_data = record["r"]
                reports.append(Report(
                    id=report_data["id"],
                    title=report_data["title"],
                    report_type=ReportType(report_data["report_type"]),
                    status=ReportStatus(report_data["status"]),
                    content=report_data.get("content"),
                    file_url=report_data.get("file_url"),
                    report_metadata=report_data.get("report_metadata"),
                    user_id=report_data["user_id"],
                    process_flow_id=report_data.get("process_flow_id"),
                    created_at=report_data["created_at"].to_native(),
                    updated_at=report_data["updated_at"].to_native(),
                    is_active=report_data["is_active"]
                ))
            return reports
        except Exception as e:
            print(f"Error getting reports by user: {e}")
        return []

    @staticmethod
    def get_reports_by_process_flow(process_flow_id: str) -> List[Report]:
        """Get all reports for a specific process flow"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (r:Report {process_flow_id: $process_flow_id, is_active: true})
        RETURN r
        ORDER BY r.created_at DESC
        """

        try:
            result = neo4j_conn.execute_query(query, {"process_flow_id": process_flow_id})
            reports = []
            for record in result:
                report_data = record["r"]
                reports.append(Report(
                    id=report_data["id"],
                    title=report_data["title"],
                    report_type=ReportType(report_data["report_type"]),
                    status=ReportStatus(report_data["status"]),
                    content=report_data.get("content"),
                    file_url=report_data.get("file_url"),
                    report_metadata=report_data.get("report_metadata"),
                    user_id=report_data["user_id"],
                    process_flow_id=report_data.get("process_flow_id"),
                    created_at=report_data["created_at"].to_native(),
                    updated_at=report_data["updated_at"].to_native(),
                    is_active=report_data["is_active"]
                ))
            return reports
        except Exception as e:
            print(f"Error getting reports by process flow: {e}")
        return []

    @staticmethod
    def get_reports_by_type(report_type: ReportType, skip: int = 0, limit: int = 100) -> List[Report]:
        """Get all reports of a specific type with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (r:Report {report_type: $report_type, is_active: true})
        RETURN r
        ORDER BY r.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"report_type": report_type.value, "skip": skip, "limit": limit})
            reports = []
            for record in result:
                report_data = record["r"]
                reports.append(Report(
                    id=report_data["id"],
                    title=report_data["title"],
                    report_type=ReportType(report_data["report_type"]),
                    status=ReportStatus(report_data["status"]),
                    content=report_data.get("content"),
                    file_url=report_data.get("file_url"),
                    report_metadata=report_data.get("report_metadata"),
                    user_id=report_data["user_id"],
                    process_flow_id=report_data.get("process_flow_id"),
                    created_at=report_data["created_at"].to_native(),
                    updated_at=report_data["updated_at"].to_native(),
                    is_active=report_data["is_active"]
                ))
            return reports
        except Exception as e:
            print(f"Error getting reports by type: {e}")
        return []
