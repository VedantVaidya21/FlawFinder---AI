from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from db.database import get_db
from db.models import User, Workflow, Report
from models.schemas import ReportResponse, ReportCreate
from utils.auth import get_current_user
from utils.responses import success_response
from services.workflow_service import WorkflowService
from services.ai_service import AIAnalysisService

router = APIRouter()
workflow_service = WorkflowService()
ai_service = AIAnalysisService()

@router.get("/{workflow_id}", response_model=dict)
async def get_workflow_report(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get executive report and improvement summary for a given workflow."""
    
    # Get workflow
    workflow = workflow_service.get_workflow(db, workflow_id)
    
    # Check if user owns this workflow
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this report"
        )
    
    # Get report
    report = workflow_service.get_report_by_workflow(db, workflow_id)
    
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found for this workflow"
        )
    
    report_response = ReportResponse(
        id=report.id,
        workflow_id=report.workflow_id,
        executive_summary=report.executive_summary,
        total_flaws=report.total_flaws,
        critical_flaws=report.critical_flaws,
        high_flaws=report.high_flaws,
        medium_flaws=report.medium_flaws,
        low_flaws=report.low_flaws,
        brutality_score=report.brutality_score,
        improvement_percentage=report.improvement_percentage,
        recommendations=report.recommendations,
        created_at=report.created_at
    )
    
    return success_response(
        message="Report retrieved successfully",
        data=report_response.dict()
    )

@router.post("/generate/{workflow_id}", response_model=dict)
async def generate_workflow_report(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate and save an executive report for a workflow if not existing."""
    
    # Get workflow
    workflow = workflow_service.get_workflow(db, workflow_id)
    
    # Check if user owns this workflow
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to generate a report for this workflow"
        )
    
    # Check if report already exists
    existing_report = workflow_service.get_report_by_workflow(db, workflow_id)
    if existing_report:
        raise HTTPException(
            status_code=400,
            detail="Report already exists for this workflow"
        )
    
    # Get flaws and corresponding fix suggestions
    flaws = workflow_service.list_flaws_by_workflow(db, workflow_id)
    fix_suggestions = []
    for flaw in flaws:
        suggestions = workflow_service.list_fix_suggestions_by_flaw(db, flaw.id)
        fix_suggestions.extend(suggestions)
    
    # Generate report content
    report_content = ai_service.generate_report(workflow_id, flaws, fix_suggestions)
    
    # Create the report in the database
    report_data = ReportCreate(**report_content)
    report = workflow_service.create_report(db, report_data)
    
    return success_response(
        message="Report generated successfully",
        data=report_content
    )
