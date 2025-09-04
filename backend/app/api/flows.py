from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..models.user import User
from ..models.process_flow import ProcessFlow, FlowStatus
from ..schemas.flow import ProcessFlowCreate, ProcessFlowResponse, FlowParseRequest, FlowParseResponse, BrutalityScoreResponse

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("/", response_model=ProcessFlowResponse)
def create_flow(
    flow_data: ProcessFlowCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new process flow"""
    db_flow = ProcessFlow(
        name=flow_data.name,
        description=flow_data.description,
        raw_input=flow_data.raw_input,
        user_id=current_user.id,
        organization_id=flow_data.organization_id or current_user.organization_id,
        status=FlowStatus.DRAFT
    )
    
    db.add(db_flow)
    db.commit()
    db.refresh(db_flow)
    
    return db_flow


@router.get("/", response_model=List[ProcessFlowResponse])
def get_flows(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all flows for current user"""
    flows = db.query(ProcessFlow).filter(
        ProcessFlow.user_id == current_user.id,
        ProcessFlow.is_active == True
    ).offset(skip).limit(limit).all()
    
    return flows


@router.get("/{flow_id}", response_model=ProcessFlowResponse)
def get_flow(
    flow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific flow by ID"""
    flow = db.query(ProcessFlow).filter(
        ProcessFlow.id == flow_id,
        ProcessFlow.user_id == current_user.id,
        ProcessFlow.is_active == True
    ).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    return flow


@router.post("/{flow_id}/parse", response_model=FlowParseResponse)
def parse_flow(
    flow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Parse a process flow and extract findings"""
    flow = db.query(ProcessFlow).filter(
        ProcessFlow.id == flow_id,
        ProcessFlow.user_id == current_user.id,
        ProcessFlow.is_active == True
    ).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    # TODO: Implement actual flow parsing logic
    # This is a mock implementation
    parsed_graph = {
        "nodes": [
            {"id": "start", "type": "start", "label": "Start"},
            {"id": "process1", "type": "process", "label": "Process 1"},
            {"id": "end", "type": "end", "label": "End"}
        ],
        "edges": [
            {"from": "start", "to": "process1"},
            {"from": "process1", "to": "end"}
        ]
    }
    
    findings = [
        {
            "title": "Manual handoff detected",
            "severity": "high",
            "type": "manual_handoff",
            "impact_score": 85.0,
            "node_id": "process1"
        }
    ]
    
    # Update flow status
    flow.status = FlowStatus.COMPLETED  # type: ignore
    flow.parsed_graph = parsed_graph  # type: ignore
    db.commit()
    
    return {
        "flow_id": flow_id,
        "parsed_graph": parsed_graph,
        "findings": findings,
        "status": "completed"
    }


@router.get("/{flow_id}/score", response_model=BrutalityScoreResponse)
def get_brutality_score(
    flow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get brutality score for a flow"""
    flow = db.query(ProcessFlow).filter(
        ProcessFlow.id == flow_id,
        ProcessFlow.user_id == current_user.id,
        ProcessFlow.is_active == True
    ).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    # TODO: Implement actual brutality score calculation
    # This is a mock implementation
    score = 73.0
    breakdown = {
        "wait_times": 25.0,
        "manual_handoffs": 30.0,
        "rework_loops": 18.0
    }
    
    return {
        "flow_id": flow_id,
        "score": score,
        "breakdown": breakdown,
        "version": "1.0"
    }


@router.get("/{flow_id}/fixes")
def get_role_based_fixes(
    flow_id: int,
    role: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get role-based fixes for a flow"""
    flow = db.query(ProcessFlow).filter(
        ProcessFlow.id == flow_id,
        ProcessFlow.user_id == current_user.id,
        ProcessFlow.is_active == True
    ).first()
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )
    
    # TODO: Implement role-based fix generation
    # This is a mock implementation
    fixes = {
        "engineer": [
            {
                "title": "Implement automated workflow",
                "description": "Replace manual process with automated workflow",
                "tools": ["Zapier", "Power Automate"],
                "steps": ["Map current process", "Design automation", "Implement and test"]
            }
        ],
        "exec": [
            {
                "title": "Strategic process optimization",
                "description": "High-level process improvement recommendations",
                "impact": "High",
                "roi": "340% within 12 months"
            }
        ]
    }
    
    return fixes.get(role, []) 