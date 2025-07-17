from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import SessionLocal
from models.workflow import Workflow
from utils.response import standard_response
from utils.auth import JWTBearer
import pandas as pd
import json

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", dependencies=[Depends(JWTBearer())])
async def upload_workflow(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content = await file.read()
    if file.filename.endswith('.csv'):
        df = pd.read_csv(pd.compat.StringIO(content.decode()))
        data = df.to_dict(orient="records")
    elif file.filename.endswith('.json'):
        data = json.loads(content.decode())
    else:
        return standard_response("fail", "Unsupported file type", status_code=400)
    workflow = Workflow(user_id=1, raw_data=data)  # Dummy user_id, replace with JWT
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return standard_response("success", "File uploaded", {"workflow_id": workflow.id, "parsed": data})
