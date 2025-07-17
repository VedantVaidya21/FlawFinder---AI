from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from db.models import User, Workflow
from models.schemas import AnalysisRequest, AnalysisResponse, FlawCreate, FixSuggestionCreate, FlawResponse, FixSuggestionResponse
from utils.auth import get_current_user
from utils.responses import success_response, error_response
from services.workflow_service import WorkflowService
from services.ai_service import AIAnalysisService

router = APIRouter()
workflow_service = WorkflowService()
ai_service = AIAnalysisService()

@router.post("/", response_model=dict)
async def analyze_workflow(
    request: AnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze workflow and identify flaws using AI."""
    
    # Get workflow
    workflow = workflow_service.get_workflow(db, request.workflow_id)
    
    # Check if user owns this workflow
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to analyze this workflow"
        )
    
    # Update workflow status
    workflow.status = "processing"
    db.commit()
    
    try:
        # Run AI analysis
        analysis_result = ai_service.analyze_workflow(workflow.raw_data)
        
        # Save flaws to database
        flaws = []
        for flaw_data in analysis_result["flaws"]:
            flaw_create = FlawCreate(
                workflow_id=workflow.id,
                flaw_type=flaw_data["flaw_type"],
                severity=flaw_data["severity"],
                title=flaw_data["title"],
                description=flaw_data["description"],
                location=flaw_data.get("location", ""),
                impact_score=flaw_data.get("impact_score", 0.0)
            )
            flaw = workflow_service.create_flaw(db, flaw_create)
            flaws.append(flaw)
        
        # Save fix suggestions to database
        fix_suggestions = []
        for i, suggestion_data in enumerate(analysis_result["fix_suggestions"]):
            # Link suggestion to corresponding flaw (assuming same order)
            if i < len(flaws):
                suggestion_create = FixSuggestionCreate(
                    flaw_id=flaws[i].id,
                    title=suggestion_data["title"],
                    description=suggestion_data["description"],
                    implementation_effort=suggestion_data["implementation_effort"],
                    expected_impact=suggestion_data["expected_impact"],
                    priority=suggestion_data["priority"],
                    estimated_time=suggestion_data.get("estimated_time", "")
                )
                suggestion = workflow_service.create_fix_suggestion(db, suggestion_create)
                fix_suggestions.append(suggestion)
        
        # Update workflow status
        workflow.status = "analyzed"
        workflow.processed_data = {
            "analysis_results": analysis_result,
            "flaws_count": len(flaws),
            "brutality_score": analysis_result["brutality_score"]
        }
        db.commit()
        
        # Prepare response
        flaw_responses = [FlawResponse(
            id=flaw.id,
            workflow_id=flaw.workflow_id,
            flaw_type=flaw.flaw_type,
            severity=flaw.severity,
            title=flaw.title,
            description=flaw.description,
            location=flaw.location,
            impact_score=flaw.impact_score,
            created_at=flaw.created_at
        ) for flaw in flaws]
        
        fix_suggestion_responses = [FixSuggestionResponse(
            id=suggestion.id,
            flaw_id=suggestion.flaw_id,
            title=suggestion.title,
            description=suggestion.description,
            implementation_effort=suggestion.implementation_effort,
            expected_impact=suggestion.expected_impact,
            priority=suggestion.priority,
            estimated_time=suggestion.estimated_time,
            created_at=suggestion.created_at
        ) for suggestion in fix_suggestions]
        
        analysis_response = AnalysisResponse(
            workflow_id=workflow.id,
            flaws=flaw_responses,
            fix_suggestions=fix_suggestion_responses,
            brutality_score=analysis_result["brutality_score"],
            total_flaws=len(flaws),
            processing_time=analysis_result["processing_time"]
        )
        
        return success_response(
            message="Workflow analysis completed successfully",
            data=analysis_response.dict()
        )
        
    except Exception as e:
        # Update workflow status to failed
        workflow.status = "failed"
        db.commit()
        
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/{workflow_id}", response_model=dict)
async def get_analysis_results(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get existing analysis results for a workflow."""
    
    # Get workflow
    workflow = workflow_service.get_workflow(db, workflow_id)
    
    # Check if user owns this workflow
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this analysis"
        )
    
    # Get flaws and fix suggestions
    flaws = workflow_service.list_flaws_by_workflow(db, workflow_id)
    
    all_fix_suggestions = []
    for flaw in flaws:
        suggestions = workflow_service.list_fix_suggestions_by_flaw(db, flaw.id)
        all_fix_suggestions.extend(suggestions)
    
    if not flaws:
        raise HTTPException(
            status_code=404,
            detail="No analysis results found for this workflow"
        )
    
    # Prepare response
    flaw_responses = [FlawResponse(
        id=flaw.id,
        workflow_id=flaw.workflow_id,
        flaw_type=flaw.flaw_type,
        severity=flaw.severity,
        title=flaw.title,
        description=flaw.description,
        location=flaw.location,
        impact_score=flaw.impact_score,
        created_at=flaw.created_at
    ) for flaw in flaws]
    
    fix_suggestion_responses = [FixSuggestionResponse(
        id=suggestion.id,
        flaw_id=suggestion.flaw_id,
        title=suggestion.title,
        description=suggestion.description,
        implementation_effort=suggestion.implementation_effort,
        expected_impact=suggestion.expected_impact,
        priority=suggestion.priority,
        estimated_time=suggestion.estimated_time,
        created_at=suggestion.created_at
    ) for suggestion in all_fix_suggestions]
    
    # Calculate brutality score
    severity_weights = {"critical": 10, "high": 7, "medium": 5, "low": 2}
    total_score = sum(severity_weights.get(flaw.severity, 0) for flaw in flaws)
    brutality_score = (total_score / len(flaws)) if flaws else 0
    
    analysis_response = AnalysisResponse(
        workflow_id=workflow_id,
        flaws=flaw_responses,
        fix_suggestions=fix_suggestion_responses,
        brutality_score=brutality_score,
        total_flaws=len(flaws),
        processing_time=0.0  # Not available for existing results
    )
    
    return success_response(
        message="Analysis results retrieved successfully",
        data=analysis_response.dict()
    )

@router.get("/status/{workflow_id}", response_model=dict)
async def get_analysis_status(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the analysis status of a workflow."""
    
    # Get workflow
    workflow = workflow_service.get_workflow(db, workflow_id)
    
    # Check if user owns this workflow
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this workflow"
        )
    
    return success_response(
        message="Analysis status retrieved successfully",
        data={
            "workflow_id": workflow_id,
            "status": workflow.status,
            "updated_at": workflow.updated_at.isoformat()
        }
    )
