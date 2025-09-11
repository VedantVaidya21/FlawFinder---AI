from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..core.neo4j import get_neo4j
from ..core.deps import get_current_active_user, User
from ..schemas.flow import ProcessFlowCreate, ProcessFlowResponse, FlowParseRequest, FlowParseResponse, BrutalityScoreResponse
import uuid
from datetime import datetime

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("/", response_model=ProcessFlowResponse)
def create_flow(
    flow_data: ProcessFlowCreate,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Create a new process flow"""
    flow_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    create_query = """
    CREATE (f:ProcessFlow {
        id: $id,
        name: $name,
        description: $description,
        raw_input: $raw_input,
        user_id: $user_id,
        organization_id: $organization_id,
        status: $status,
        is_active: $is_active,
        created_at: $created_at,
        updated_at: $updated_at
    })
    RETURN f
    """

    neo4j_conn.execute_write_query(create_query, {
        "id": flow_id,
        "name": flow_data.name,
        "description": flow_data.description,
        "raw_input": flow_data.raw_input,
        "user_id": current_user.id,
        "organization_id": flow_data.organization_id or current_user.organization_id,
        "status": "draft",
        "is_active": True,
        "created_at": now,
        "updated_at": now
    })

    return {
        "id": flow_id,
        "name": flow_data.name,
        "description": flow_data.description,
        "raw_input": flow_data.raw_input,
        "user_id": current_user.id,
        "organization_id": flow_data.organization_id or current_user.organization_id,
        "status": "draft",
        "is_active": True,
        "created_at": now,
        "updated_at": now
    }


@router.get("/", response_model=List[ProcessFlowResponse])
def get_flows(
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j),
    skip: int = 0,
    limit: int = 100
):
    """Get all flows for current user"""
    query = """
    MATCH (f:ProcessFlow)
    WHERE f.user_id = $user_id AND f.is_active = true
    RETURN f.id as id, f.name as name, f.description as description,
           f.raw_input as raw_input, f.user_id as user_id,
           f.organization_id as organization_id, f.status as status,
           f.is_active as is_active, f.created_at as created_at,
           f.updated_at as updated_at
    SKIP $skip LIMIT $limit
    """

    result = neo4j_conn.execute_query(query, {
        "user_id": current_user.id,
        "skip": skip,
        "limit": limit
    })

    return result


@router.get("/{flow_id}", response_model=ProcessFlowResponse)
def get_flow(
    flow_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Get a specific flow by ID"""
    query = """
    MATCH (f:ProcessFlow)
    WHERE f.id = $flow_id AND f.user_id = $user_id AND f.is_active = true
    RETURN f.id as id, f.name as name, f.description as description,
           f.raw_input as raw_input, f.user_id as user_id,
           f.organization_id as organization_id, f.status as status,
           f.is_active as is_active, f.created_at as created_at,
           f.updated_at as updated_at
    """

    result = neo4j_conn.execute_query(query, {
        "flow_id": flow_id,
        "user_id": current_user.id
    })

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )

    return result[0]


@router.post("/{flow_id}/parse", response_model=FlowParseResponse)
def parse_flow(
    flow_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Parse a process flow and extract findings"""
    # First check if flow exists
    query = """
    MATCH (f:ProcessFlow)
    WHERE f.id = $flow_id AND f.user_id = $user_id AND f.is_active = true
    RETURN f
    """

    result = neo4j_conn.execute_query(query, {
        "flow_id": flow_id,
        "user_id": current_user.id
    })

    if not result:
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
    update_query = """
    MATCH (f:ProcessFlow)
    WHERE f.id = $flow_id
    SET f.status = $status, f.parsed_graph = $parsed_graph, f.updated_at = $updated_at
    """

    neo4j_conn.execute_write_query(update_query, {
        "flow_id": flow_id,
        "status": "completed",
        "parsed_graph": parsed_graph,
        "updated_at": datetime.utcnow().isoformat()
    })

    return {
        "flow_id": flow_id,
        "parsed_graph": parsed_graph,
        "findings": findings,
        "status": "completed"
    }


@router.get("/{flow_id}/score", response_model=BrutalityScoreResponse)
def get_brutality_score(
    flow_id: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Get brutality score for a flow"""
    # Check if flow exists
    query = """
    MATCH (f:ProcessFlow)
    WHERE f.id = $flow_id AND f.user_id = $user_id AND f.is_active = true
    RETURN f
    """

    result = neo4j_conn.execute_query(query, {
        "flow_id": flow_id,
        "user_id": current_user.id
    })

    if not result:
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
    flow_id: str,
    role: str,
    current_user: User = Depends(get_current_active_user),
    neo4j_conn = Depends(get_neo4j)
):
    """Get role-based fixes for a flow"""
    # Check if flow exists
    query = """
    MATCH (f:ProcessFlow)
    WHERE f.id = $flow_id AND f.user_id = $user_id AND f.is_active = true
    RETURN f
    """

    result = neo4j_conn.execute_query(query, {
        "flow_id": flow_id,
        "user_id": current_user.id
    })

    if not result:
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
