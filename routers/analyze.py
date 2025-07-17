from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import SessionLocal
from models.workflow import Workflow
from models.flaw import Flaw
from models.fix_suggestion import FixSuggestion
from utils.response import standard_response
from utils.auth import JWTBearer
from sqlalchemy.future import select
import networkx as nx

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", dependencies=[Depends(JWTBearer())])
async def analyze_workflow(workflow_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = q.scalar_one_or_none()
    if not workflow:
        return standard_response("fail", "Workflow not found", status_code=404)
    # Dummy graph and flaw analysis
    G = nx.DiGraph()
    # Build a mock graph from workflow.raw_data (replace with real logic)
    G.add_node("A")
    G.add_node("B")
    G.add_edge("A", "B")
    # Dummy flaws
    flaws = [
        {"flaw_type": "cycle", "description": "Found cycle in workflow"}
    ]
    fixes = [
        {"suggestion": "Remove cycle between A and B"}
    ]
    brutality_score = 42
    # Save flaws and fixes
    for flaw in flaws:
        flaw_obj = Flaw(workflow_id=workflow.id, flaw_type=flaw["flaw_type"], description=flaw["description"])
        db.add(flaw_obj)
        await db.flush()
        for fix in fixes:
            fix_obj = FixSuggestion(flaw_id=flaw_obj.id, suggestion=fix["suggestion"])
            db.add(fix_obj)
    await db.commit()
    return standard_response("success", "Analysis complete", {
        "flaws": flaws,
        "fixes": fixes,
        "brutality_score": brutality_score
    })
