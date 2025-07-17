from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from db.database import get_db
from db.models import User, Workflow, Flaw
from models.schemas import DashboardStats, WorkflowResponse
from utils.auth import get_current_user
from utils.responses import success_response
from services.workflow_service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()

@router.get("/{user_id}", response_model=dict)
async def get_dashboard_stats(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for a user."""
    
    # Check if user can access this dashboard
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this dashboard"
        )
    
    # Get user workflows
    workflows = workflow_service.list_workflows_by_user(db, user_id)
    
    # Get all flaws for user workflows
    workflow_ids = [w.id for w in workflows]
    flaws = []
    if workflow_ids:
        flaws = db.query(Flaw).filter(Flaw.workflow_id.in_(workflow_ids)).all()
    
    # Calculate statistics
    total_workflows = len(workflows)
    total_flaws = len(flaws)
    
    # Calculate average brutality score
    avg_brutality_score = 0.0
    if flaws:
        severity_weights = {"critical": 10, "high": 7, "medium": 5, "low": 2}
        total_score = sum(severity_weights.get(flaw.severity, 0) for flaw in flaws)
        avg_brutality_score = total_score / total_flaws if total_flaws > 0 else 0
    
    # Get recent workflows (last 5)
    recent_workflows = sorted(workflows, key=lambda x: x.created_at, reverse=True)[:5]
    recent_workflow_responses = [WorkflowResponse(
        id=w.id,
        name=w.name,
        raw_data=w.raw_data,
        processed_data=w.processed_data,
        file_type=w.file_type,
        status=w.status,
        created_at=w.created_at,
        updated_at=w.updated_at
    ) for w in recent_workflows]
    
    # Calculate flaw distribution by type
    flaw_distribution = {}
    for flaw in flaws:
        flaw_type = flaw.flaw_type
        flaw_distribution[flaw_type] = flaw_distribution.get(flaw_type, 0) + 1
    
    # Calculate severity distribution
    severity_distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for flaw in flaws:
        severity = flaw.severity
        if severity in severity_distribution:
            severity_distribution[severity] += 1
    
    # Prepare dashboard stats
    dashboard_stats = DashboardStats(
        total_workflows=total_workflows,
        total_flaws=total_flaws,
        avg_brutality_score=avg_brutality_score,
        recent_workflows=recent_workflow_responses,
        flaw_distribution=flaw_distribution,
        severity_distribution=severity_distribution
    )
    
    return success_response(
        message="Dashboard statistics retrieved successfully",
        data=dashboard_stats.dict()
    )

@router.get("/", response_model=dict)
async def get_current_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for the current user."""
    return await get_dashboard_stats(current_user.id, current_user, db)

@router.get("/charts/{user_id}", response_model=dict)
async def get_dashboard_charts(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chart data for dashboard visualizations."""
    
    # Check if user can access this dashboard
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this dashboard"
        )
    
    # Get user workflows
    workflows = workflow_service.list_workflows_by_user(db, user_id)
    workflow_ids = [w.id for w in workflows]
    
    # Get flaws for charts
    flaws = []
    if workflow_ids:
        flaws = db.query(Flaw).filter(Flaw.workflow_id.in_(workflow_ids)).all()
    
    # Prepare chart data
    chart_data = {
        "flaw_types_pie": _get_flaw_types_chart_data(flaws),
        "severity_distribution": _get_severity_distribution_chart_data(flaws),
        "workflow_status_pie": _get_workflow_status_chart_data(workflows),
        "flaws_over_time": _get_flaws_over_time_chart_data(flaws),
        "brutality_score_trend": _get_brutality_score_trend_data(workflows, flaws)
    }
    
    return success_response(
        message="Dashboard chart data retrieved successfully",
        data=chart_data
    )

def _get_flaw_types_chart_data(flaws) -> Dict[str, Any]:
    """Generate pie chart data for flaw types."""
    flaw_types = {}
    for flaw in flaws:
        flaw_type = flaw.flaw_type
        flaw_types[flaw_type] = flaw_types.get(flaw_type, 0) + 1
    
    return {
        "labels": list(flaw_types.keys()),
        "data": list(flaw_types.values()),
        "colors": [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", 
            "#9966FF", "#FF9F40", "#FF6384", "#C9CBCF"
        ][:len(flaw_types)]
    }

def _get_severity_distribution_chart_data(flaws) -> Dict[str, Any]:
    """Generate bar chart data for severity distribution."""
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for flaw in flaws:
        severity = flaw.severity
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    return {
        "labels": ["Critical", "High", "Medium", "Low"],
        "data": [
            severity_counts["critical"],
            severity_counts["high"],
            severity_counts["medium"],
            severity_counts["low"]
        ],
        "colors": ["#FF4444", "#FF8800", "#FFCC00", "#44FF44"]
    }

def _get_workflow_status_chart_data(workflows) -> Dict[str, Any]:
    """Generate pie chart data for workflow status."""
    status_counts = {}
    for workflow in workflows:
        status = workflow.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return {
        "labels": list(status_counts.keys()),
        "data": list(status_counts.values()),
        "colors": [
            "#36A2EB", "#FFCE56", "#4BC0C0", "#FF6384", 
            "#9966FF", "#FF9F40"
        ][:len(status_counts)]
    }

def _get_flaws_over_time_chart_data(flaws) -> Dict[str, Any]:
    """Generate line chart data for flaws over time."""
    # Group flaws by date
    date_counts = {}
    for flaw in flaws:
        date = flaw.created_at.date().isoformat()
        date_counts[date] = date_counts.get(date, 0) + 1
    
    # Sort by date
    sorted_dates = sorted(date_counts.keys())
    
    return {
        "labels": sorted_dates,
        "data": [date_counts[date] for date in sorted_dates],
        "color": "#36A2EB"
    }

def _get_brutality_score_trend_data(workflows, flaws) -> Dict[str, Any]:
    """Generate line chart data for brutality score trend."""
    # Calculate brutality score for each workflow
    workflow_scores = {}
    severity_weights = {"critical": 10, "high": 7, "medium": 5, "low": 2}
    
    for workflow in workflows:
        workflow_flaws = [f for f in flaws if f.workflow_id == workflow.id]
        if workflow_flaws:
            total_score = sum(severity_weights.get(f.severity, 0) for f in workflow_flaws)
            avg_score = total_score / len(workflow_flaws)
            workflow_scores[workflow.created_at.date().isoformat()] = avg_score
    
    # Sort by date
    sorted_dates = sorted(workflow_scores.keys())
    
    return {
        "labels": sorted_dates,
        "data": [workflow_scores[date] for date in sorted_dates],
        "color": "#FF6384"
    }
