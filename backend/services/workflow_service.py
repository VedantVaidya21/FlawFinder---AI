from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models import User, Workflow, Flaw, FixSuggestion, Report
from models.schemas import WorkflowCreate, FlawCreate, FixSuggestionCreate, ReportCreate

class WorkflowService:
    def create_workflow(self, db: Session, workflow_data: WorkflowCreate, user_id: int) -> Workflow:
        """Create a new workflow and save it to the database."""
        workflow = Workflow(
            name=workflow_data.name,
            raw_data=workflow_data.raw_data,
            processed_data={},  # Initially empty
            file_type=workflow_data.file_type,
            user_id=user_id
        )
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        return workflow
    
    def get_workflow(self, db: Session, workflow_id: int) -> Workflow:
        """Retrieve a workflow by its ID."""
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return workflow

    def create_flaw(self, db: Session, flaw_data: FlawCreate) -> Flaw:
        """Create a new flaw and link it to a workflow."""
        flaw = Flaw(**flaw_data.dict())
        db.add(flaw)
        db.commit()
        db.refresh(flaw)
        return flaw
    
    def create_fix_suggestion(self, db: Session, suggestion_data: FixSuggestionCreate) -> FixSuggestion:
        """Create a new fix suggestion and link it to a flaw."""
        suggestion = FixSuggestion(**suggestion_data.dict())
        db.add(suggestion)
        db.commit()
        db.refresh(suggestion)
        return suggestion
    
    def create_report(self, db: Session, report_data: ReportCreate) -> Report:
        """Create a report for the workflow analysis."""
        report = Report(**report_data.dict())
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
    
    def list_workflows_by_user(self, db: Session, user_id: int) -> list:
        """List all workflows by a specific user."""
        return db.query(Workflow).filter(Workflow.user_id == user_id).all()
    
    def list_flaws_by_workflow(self, db: Session, workflow_id: int) -> list:
        """List all flaws associated with a specific workflow."""
        return db.query(Flaw).filter(Flaw.workflow_id == workflow_id).all()

    def list_fix_suggestions_by_flaw(self, db: Session, flaw_id: int) -> list:
        """List all fix suggestions for a specific flaw."""
        return db.query(FixSuggestion).filter(FixSuggestion.flaw_id == flaw_id).all()

    def get_report_by_workflow(self, db: Session, workflow_id: int) -> Report:
        """Retrieve the report associated with a specific workflow."""
        report = db.query(Report).filter(Report.workflow_id == workflow_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report

