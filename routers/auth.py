from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.session import SessionLocal
from models.user import User
from passlib.context import CryptContext
from utils.jwt_helper import create_access_token
from utils.response import standard_response
from pydantic import BaseModel

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/signup")
async def signup(payload: SignupRequest, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.email == payload.email))
    user = q.scalar_one_or_none()
    if user:
        return standard_response("fail", "Email already registered", status_code=400)
    hashed_password = pwd_context.hash(payload.password)
    new_user = User(name=payload.name, email=payload.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return standard_response("success", "User created", {"user_id": new_user.id})

@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.email == payload.email))
    user = q.scalar_one_or_none()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        return standard_response("fail", "Invalid credentials", status_code=401)
    token = create_access_token({"user_id": user.id, "email": user.email})
    return standard_response("success", "Login successful", {"access_token": token})
