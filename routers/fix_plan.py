from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import SessionLocal
from models.flaw import Flaw
from models.fix_suggestion import FixSuggestion
from utils.response import standard_response
from utils.auth import JWTBearer
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/{workflow_id}", dependencies=[Depends(JWTBearer())])
async def fix_plan(workflow_id: int, db: AsyncSession = Depends(get_db)):
    # Dummy fix suggestions
    q = await db.execute(select(Flaw).where(Flaw.workflow_id == workflow_id))
    flaws = q.scalars().all()
    suggestions = [
        {"flaw_id": flaw.id, "suggestion": f"Fix suggestion for flaw {flaw.id}"} for flaw in flaws
    ]
    return standard_response("success", "Fix suggestions", {"suggestions": suggestions})
