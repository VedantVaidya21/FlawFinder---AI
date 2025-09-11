from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..core.neo4j import get_neo4j
from ..core.deps import get_current_active_user, require_exec_or_admin, User
from ..schemas.report import ReportCreate, ReportResponse, CEOReportRequest
import uuid
from datetime import datetime

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/ceo", response_model=ReportResponse)
def generate_ceo_report(
    report_request: CEOReportRequest,
    current_user: User = Depends(require_exec_or_admin),
    neo4j_conn = Depends(get_neo4j)
):
    """Generate CEO report"""
    # TODO: Implement actual CEO report generation
    # This is a mock implementation

    report_content = {
        "executive_summary": {
            "brutality_score": 73,
            "total_flaws": 42,
            "fixes_implemented": 18
        },
        "key_findings": [
            {
                "title": "Critical inefficiencies in approval processes",
                "description": "Average approval time: 7.2 days (industry standard: 2.1 days)",
                "severity": "critical"
            },
            {
                "title": "Manual data entry causing delays",
                "description": "38% of workflows involve duplicate data entry",
                "severity": "high"
            }
        ],
        "recommendations": [
            {
                "title": "Implement workflow automation platform",
                "description": "Estimated ROI: 340% within 12 months",
                "priority": "high"
            },
            {
                "title": "Integrate systems to eliminate duplicate data entry",
                "description": "Potential time savings: 15-20 hours per week per employee",
                "priority": "medium"
            }
        ]
    }

    # Create report record in Neo4j
    report_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    create_query = """
    CREATE (r:Report {
        id: $id,
        title: $title,
        report_type: $report_type,
        status: $status,
        content: $content,
        file_url: $file_url,
        user_id: $user_id,
        process_flow_id: $process_flow_id,
        created_at: $created_at,
        updated_at: $updated_at
    })
    RETURN r
    """

    neo4j_conn.execute_write_query(create_query, {
        "id": report_id,
        "title": "CEO Report - Process Analysis",
        "report_type": "ceo_report",
        "status": "completed",
        "content": report_content,
        "file_url": "/reports/ceo-report.pdf",  # Mock URL
        "user_id": current_user.id,
        "process_flow_id": report_request.flow_id,
        "created_at": now,
        "updated_at": now
    })

    return {
        "id": report_id,
        "title": "CEO Report - Process Analysis",
        "report_type": "ceo_report",
        "status": "completed",
        "content": report_content,
        "file_url": "/reports/ceo-report.pdf",
        "user_id": current_user.id,
        "process_flow_id": report_request.flow_id,
        "created_at": now,
        "updated_at": now
    }


@router.get("/", response_model=List[ReportResponse])
def get_reports(
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j),
    skip: int = 0,
    limit: int = 100
):
    """Get all reports for current user"""
    query = """
    MATCH (r:Report)
    WHERE r.user_id = $user_id
    RETURN r.id as id, r.title as title, r.report_type as report_type,
           r.status as status, r.content as content, r.file_url as file_url,
           r.user_id as user_id, r.process_flow_id as process_flow_id,
           r.created_at as created_at, r.updated_at as updated_at
    SKIP $skip LIMIT $limit
    """

    result = neo4j_conn.execute_query(query, {
        "user_id": current_user.id,
        "skip": skip,
        "limit": limit
    })

    return result


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Get a specific report by ID"""
    query = """
    MATCH (r:Report)
    WHERE r.id = $report_id AND r.user_id = $user_id
    RETURN r.id as id, r.title as title, r.report_type as report_type,
           r.status as status, r.content as content, r.file_url as file_url,
           r.user_id as user_id, r.process_flow_id as process_flow_id,
           r.created_at as created_at, r.updated_at as updated_at
    """

    result = neo4j_conn.execute_query(query, {
        "report_id": report_id,
        "user_id": current_user.id
    })

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return result[0]


@router.get("/{report_id}/download")
def download_report(
    report_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Download report file"""
    query = """
    MATCH (r:Report)
    WHERE r.id = $report_id AND r.user_id = $user_id
    RETURN r.file_url as file_url
    """

    result = neo4j_conn.execute_query(query, {
        "report_id": report_id,
        "user_id": current_user.id
    })

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    file_url = result[0].get("file_url")
    if not file_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not available"
        )

    # TODO: Implement actual file download logic
    return {"download_url": file_url}
