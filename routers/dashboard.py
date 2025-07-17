from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import SessionLocal
from models.workflow import Workflow
from models.flaw import Flaw
from utils.response import standard_response
from utils.auth import JWTBearer
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/{user_id}", dependencies=[Depends(JWTBearer())])
async def dashboard(user_id: int, db: AsyncSession = Depends(get_db)):
    # Dummy stats
    q = await db.execute(select(Workflow).where(Workflow.user_id == user_id))
    workflows = q.scalars().all()
    workflow_count = len(workflows)
    flaw_count = 7  # Dummy
    score = 75  # Dummy
    charts = {"pie": [1, 2, 3], "bar": [4, 5, 6]}  # Dummy
    return standard_response("success", "Dashboard data", {
        "workflow_count": workflow_count,
        "flaw_count": flaw_count,
        "score": score,
        "charts": charts
    })
