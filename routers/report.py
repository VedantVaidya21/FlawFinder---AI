from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import SessionLocal
from models.report import Report
from utils.response import standard_response
from utils.auth import JWTBearer
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/{workflow_id}", dependencies=[Depends(JWTBearer())])
async def report(workflow_id: int, db: AsyncSession = Depends(get_db)):
    # Dummy executive report
    q = await db.execute(select(Report).where(Report.workflow_id == workflow_id))
    report = q.scalar_one_or_none()
    summary = report.summary if report else "No report available."
    improvement = "Improve process flow and reduce flaws."  # Dummy
    return standard_response("success", "Report data", {
        "summary": summary,
        "improvement": improvement
    })
