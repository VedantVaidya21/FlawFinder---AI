# backend/app/api/flows.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..core.deps import get_current_active_user
from ..models.user_neo4j import User
from ..models.process_flow_neo4j import (
    ProcessFlow,
    ProcessFlowCreate,
    ProcessFlowResponse,
)

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("/", response_model=ProcessFlowResponse)
async def create_flow(
    flow_data: ProcessFlowCreate,
    current_user: User = Depends(get_current_active_user),
):
    """Create a new process flow"""
    # Create the process flow using the Neo4j model
    flow = ProcessFlow(
        name=flow_data.name,
        description=flow_data.description,
        raw_input=flow_data.raw_input,
        user_id=current_user.id,
        organization_id=flow_data.organization_id,
    )
    await flow.save()
    return ProcessFlowResponse(**flow.dict())


@router.get("/", response_model=List[ProcessFlowResponse])
async def get_flows(current_user: User = Depends(get_current_active_user)):
    """Get all flows for current user"""
    flows = await ProcessFlow.get_by_user(current_user.id)
    return [ProcessFlowResponse(**flow.dict()) for flow in flows]


@router.get("/{flow_id}", response_model=ProcessFlowResponse)
async def get_flow(flow_id: str, current_user: User = Depends(get_current_active_user)):
    """Get a specific flow by ID"""
    flow = await ProcessFlow.get_by_id_and_user(flow_id, current_user.id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    return ProcessFlowResponse(**flow.dict())
