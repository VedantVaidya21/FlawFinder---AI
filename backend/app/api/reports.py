from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_user, require_exec_or_admin
from ..models.user import User
from ..models.report import Report, ReportType, ReportStatus
from ..schemas.report import ReportCreate, ReportResponse, CEOReportRequest

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/ceo", response_model=ReportResponse)
def generate_ceo_report(
    report_request: CEOReportRequest,
    current_user: User = Depends(require_exec_or_admin),
    db: Session = Depends(get_db)
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
    
    # Create report record
    db_report = Report(
        title="CEO Report - Process Analysis",
        report_type=ReportType.CEO_REPORT,
        status=ReportStatus.COMPLETED,
        content=report_content,
        file_url="/reports/ceo-report.pdf",  # Mock URL
        user_id=current_user.id,
        process_flow_id=report_request.flow_id
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report


@router.get("/", response_model=List[ReportResponse])
def get_reports(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all reports for current user"""
    reports = db.query(Report).filter(
        Report.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific report by ID"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download report file"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    if not report.file_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not available"
        )
    
    # TODO: Implement actual file download logic
    return {"download_url": report.file_url} 