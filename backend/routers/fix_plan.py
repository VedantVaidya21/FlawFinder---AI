from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from db.database import get_db
from db.models import User, Workflow, Flaw, FixSuggestion
from models.schemas import FixSuggestionResponse, FlawResponse
from utils.auth import get_current_user
from utils.responses import success_response
from services.workflow_service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()

@router.get("/{workflow_id}", response_model=dict)
async def get_fix_plan(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get fix suggestions for a given workflow."""
    
    # Get workflow
    workflow = workflow_service.get_workflow(db, workflow_id)
    
    # Check if user owns this workflow
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this fix plan"
        )
    
    # Get flaws for this workflow
    flaws = workflow_service.list_flaws_by_workflow(db, workflow_id)
    
    if not flaws:
        return success_response(
            message="No flaws found for this workflow",
            data={
                "workflow_id": workflow_id,
                "workflow_name": workflow.name,
                "fix_plan": [],
                "summary": {
                    "total_suggestions": 0,
                    "high_priority": 0,
                    "medium_priority": 0,
                    "low_priority": 0,
                    "estimated_total_time": "0 hours"
                }
            }
        )
    
    # Get all fix suggestions for these flaws
    fix_plan = []
    for flaw in flaws:
        suggestions = workflow_service.list_fix_suggestions_by_flaw(db, flaw.id)
        
        flaw_response = FlawResponse(
            id=flaw.id,
            workflow_id=flaw.workflow_id,
            flaw_type=flaw.flaw_type,
            severity=flaw.severity,
            title=flaw.title,
            description=flaw.description,
            location=flaw.location,
            impact_score=flaw.impact_score,
            created_at=flaw.created_at
        )
        
        suggestion_responses = [FixSuggestionResponse(
            id=suggestion.id,
            flaw_id=suggestion.flaw_id,
            title=suggestion.title,
            description=suggestion.description,
            implementation_effort=suggestion.implementation_effort,
            expected_impact=suggestion.expected_impact,
            priority=suggestion.priority,
            estimated_time=suggestion.estimated_time,
            created_at=suggestion.created_at
        ) for suggestion in suggestions]
        
        fix_plan.append({
            "flaw": flaw_response.dict(),
            "suggestions": [s.dict() for s in suggestion_responses]
        })
    
    # Calculate summary statistics
    all_suggestions = []
    for item in fix_plan:
        all_suggestions.extend(item["suggestions"])
    
    summary = {
        "total_suggestions": len(all_suggestions),
        "high_priority": len([s for s in all_suggestions if s["priority"] <= 2]),
        "medium_priority": len([s for s in all_suggestions if s["priority"] == 3]),
        "low_priority": len([s for s in all_suggestions if s["priority"] >= 4]),
        "estimated_total_time": _calculate_total_time(all_suggestions)
    }
    
    return success_response(
        message="Fix plan retrieved successfully",
        data={
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "fix_plan": fix_plan,
            "summary": summary
        }
    )

@router.get("/suggestions/{flaw_id}", response_model=dict)
async def get_flaw_suggestions(
    flaw_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get fix suggestions for a specific flaw."""
    
    # Get flaw
    flaw = db.query(Flaw).filter(Flaw.id == flaw_id).first()
    if not flaw:
        raise HTTPException(
            status_code=404,
            detail="Flaw not found"
        )
    
    # Get workflow to check ownership
    workflow = workflow_service.get_workflow(db, flaw.workflow_id)
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this flaw"
        )
    
    # Get suggestions for this flaw
    suggestions = workflow_service.list_fix_suggestions_by_flaw(db, flaw_id)
    
    suggestion_responses = [FixSuggestionResponse(
        id=suggestion.id,
        flaw_id=suggestion.flaw_id,
        title=suggestion.title,
        description=suggestion.description,
        implementation_effort=suggestion.implementation_effort,
        expected_impact=suggestion.expected_impact,
        priority=suggestion.priority,
        estimated_time=suggestion.estimated_time,
        created_at=suggestion.created_at
    ) for suggestion in suggestions]
    
    return success_response(
        message="Fix suggestions retrieved successfully",
        data={
            "flaw_id": flaw_id,
            "flaw_title": flaw.title,
            "flaw_severity": flaw.severity,
            "suggestions": [s.dict() for s in suggestion_responses]
        }
    )

@router.get("/priority/{workflow_id}", response_model=dict)
async def get_prioritized_fix_plan(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get fix suggestions organized by priority."""
    
    # Get workflow
    workflow = workflow_service.get_workflow(db, workflow_id)
    
    # Check if user owns this workflow
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this fix plan"
        )
    
    # Get all flaws and their suggestions
    flaws = workflow_service.list_flaws_by_workflow(db, workflow_id)
    
    all_suggestions = []
    flaw_map = {}
    
    for flaw in flaws:
        flaw_map[flaw.id] = flaw
        suggestions = workflow_service.list_fix_suggestions_by_flaw(db, flaw.id)
        
        for suggestion in suggestions:
            all_suggestions.append({
                "suggestion": suggestion,
                "flaw": flaw
            })
    
    # Sort by priority and severity
    priority_order = {"critical": 1, "high": 2, "medium": 3, "low": 4}
    all_suggestions.sort(key=lambda x: (
        x["suggestion"].priority,
        priority_order.get(x["flaw"].severity, 5)
    ))
    
    # Group by priority
    high_priority = []
    medium_priority = []
    low_priority = []
    
    for item in all_suggestions:
        suggestion = item["suggestion"]
        flaw = item["flaw"]
        
        suggestion_data = {
            "suggestion_id": suggestion.id,
            "flaw_id": flaw.id,
            "title": suggestion.title,
            "description": suggestion.description,
            "flaw_title": flaw.title,
            "flaw_severity": flaw.severity,
            "implementation_effort": suggestion.implementation_effort,
            "expected_impact": suggestion.expected_impact,
            "priority": suggestion.priority,
            "estimated_time": suggestion.estimated_time
        }
        
        if suggestion.priority <= 2:
            high_priority.append(suggestion_data)
        elif suggestion.priority == 3:
            medium_priority.append(suggestion_data)
        else:
            low_priority.append(suggestion_data)
    
    return success_response(
        message="Prioritized fix plan retrieved successfully",
        data={
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
            "total_suggestions": len(all_suggestions)
        }
    )

def _calculate_total_time(suggestions: List[Dict[str, Any]]) -> str:
    """Calculate total estimated time from suggestions."""
    # This is a simplified calculation
    # In a real implementation, you'd parse time strings and sum them
    
    total_days = 0
    total_hours = 0
    
    for suggestion in suggestions:
        estimated_time = suggestion.get("estimated_time", "")
        if not estimated_time:
            continue
        
        # Simple parsing - in reality, this would be more sophisticated
        if "day" in estimated_time.lower():
            try:
                days = int(estimated_time.split()[0])
                total_days += days
            except:
                pass
        elif "week" in estimated_time.lower():
            try:
                weeks = int(estimated_time.split()[0])
                total_days += weeks * 5  # 5 working days per week
            except:
                pass
        elif "hour" in estimated_time.lower():
            try:
                hours = int(estimated_time.split()[0])
                total_hours += hours
            except:
                pass
    
    # Convert to human-readable format
    if total_days > 0:
        return f"{total_days} days"
    elif total_hours > 0:
        return f"{total_hours} hours"
    else:
        return "Time not specified"
