from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
import pandas as pd
import json
import csv
from io import StringIO
from typing import Dict, Any

from db.database import get_db
from db.models import User, Workflow
from models.schemas import UploadResponse, WorkflowCreate
from utils.auth import get_current_user
from utils.responses import success_response, error_response
from services.workflow_service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()

@router.post("/", response_model=dict)
async def upload_workflow_file(
    file: UploadFile = File(...),
    name: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload CSV or JSON business workflow file."""
    
    # Validate file type
    if file.content_type not in ["text/csv", "application/json", "text/plain"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only CSV and JSON files are supported."
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Parse based on file type
        if file.filename.endswith('.csv') or file.content_type == 'text/csv':
            parsed_data = await _parse_csv_file(content)
            file_type = "csv"
        elif file.filename.endswith('.json') or file.content_type == 'application/json':
            parsed_data = await _parse_json_file(content)
            file_type = "json"
        else:
            # Try to auto-detect format
            try:
                parsed_data = await _parse_json_file(content)
                file_type = "json"
            except:
                parsed_data = await _parse_csv_file(content)
                file_type = "csv"
        
        # Create workflow
        workflow_data = WorkflowCreate(
            name=name,
            raw_data=parsed_data,
            file_type=file_type
        )
        
        workflow = workflow_service.create_workflow(db, workflow_data, current_user.id)
        
        upload_response = UploadResponse(
            workflow_id=workflow.id,
            message="File uploaded and processed successfully",
            parsed_data=parsed_data
        )
        
        return success_response(
            message="File uploaded successfully",
            data=upload_response.dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )

async def _parse_csv_file(content: bytes) -> Dict[str, Any]:
    """Parse CSV file content and convert to structured format."""
    try:
        # Decode bytes to string
        content_str = content.decode('utf-8')
        
        # Parse CSV
        csv_reader = csv.DictReader(StringIO(content_str))
        rows = list(csv_reader)
        
        # Convert to structured workflow format
        structured_data = {
            "format": "csv",
            "total_rows": len(rows),
            "columns": list(rows[0].keys()) if rows else [],
            "steps": []
        }
        
        # Convert each row to a workflow step
        for i, row in enumerate(rows):
            step = {
                "id": i + 1,
                "name": row.get('name', row.get('step_name', f"Step {i+1}")),
                "description": row.get('description', row.get('step_description', '')),
                "type": row.get('type', row.get('step_type', 'process')),
                "duration": row.get('duration', row.get('estimated_time', '')),
                "owner": row.get('owner', row.get('responsible_person', '')),
                "inputs": row.get('inputs', row.get('input_data', '')),
                "outputs": row.get('outputs', row.get('output_data', '')),
                "dependencies": row.get('dependencies', row.get('depends_on', '')),
                "raw_data": row
            }
            structured_data["steps"].append(step)
        
        return structured_data
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse CSV file: {str(e)}"
        )

async def _parse_json_file(content: bytes) -> Dict[str, Any]:
    """Parse JSON file content."""
    try:
        # Decode bytes to string and parse JSON
        content_str = content.decode('utf-8')
        json_data = json.loads(content_str)
        
        # If it's already in workflow format, return as is
        if isinstance(json_data, dict) and "steps" in json_data:
            return json_data
        
        # If it's a list, convert to workflow format
        if isinstance(json_data, list):
            structured_data = {
                "format": "json",
                "total_steps": len(json_data),
                "steps": []
            }
            
            for i, item in enumerate(json_data):
                if isinstance(item, dict):
                    step = {
                        "id": i + 1,
                        "name": item.get('name', item.get('step_name', f"Step {i+1}")),
                        "description": item.get('description', item.get('step_description', '')),
                        "type": item.get('type', item.get('step_type', 'process')),
                        "duration": item.get('duration', item.get('estimated_time', '')),
                        "owner": item.get('owner', item.get('responsible_person', '')),
                        "inputs": item.get('inputs', item.get('input_data', '')),
                        "outputs": item.get('outputs', item.get('output_data', '')),
                        "dependencies": item.get('dependencies', item.get('depends_on', '')),
                        "raw_data": item
                    }
                    structured_data["steps"].append(step)
            
            return structured_data
        
        # If it's a single object, wrap it
        if isinstance(json_data, dict):
            return {
                "format": "json",
                "total_steps": 1,
                "steps": [json_data]
            }
        
        # Default case
        return {
            "format": "json",
            "raw_data": json_data
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse JSON file: {str(e)}"
        )

@router.get("/workflows", response_model=dict)
async def get_user_workflows(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all workflows uploaded by the current user."""
    
    workflows = workflow_service.list_workflows_by_user(db, current_user.id)
    
    return success_response(
        message="Workflows retrieved successfully",
        data=[{
            "id": workflow.id,
            "name": workflow.name,
            "file_type": workflow.file_type,
            "status": workflow.status,
            "created_at": workflow.created_at.isoformat(),
            "updated_at": workflow.updated_at.isoformat()
        } for workflow in workflows]
    )
