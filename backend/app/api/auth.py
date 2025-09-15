from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from pydantic import BaseModel, EmailStr

from ..core import security
from ..core.config import settings
from ..core.deps import get_current_user
from ..models.user_neo4j import User, UserCreate, UserUpdate, UserInDB
from ..models.token import Token

router = APIRouter(tags=["auth"])
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=Token)
async def login_json(payload: LoginRequest) -> Any:
    """JSON login endpoint compatible with frontend (email/password in JSON)."""
    user = await authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }



async def authenticate_user(email: str, password: str) -> User | None:
    """Verify user credentials"""
    user = await User.get_by_email(email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=User)
async def register_user(user_in: UserCreate) -> Any:
    """Register a new user"""
    existing_user = await User.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = await user_in.create()
    # Ensure hashed_password is not exposed in response
    user.hashed_password = None
    return user


@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    """Get current user"""
    return current_user


@router.put("/me", response_model=UserInDB)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update current user"""
    user = await user_in.update(current_user)
    return user


@router.post("/password-change")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user)
) -> dict:
    """Change user password"""
    success = await current_user.change_password(current_password, new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    return {"status": "success", "message": "Password updated successfully"}


@router.post("/password-reset")
async def request_password_reset(email: str) -> dict:
    """Request password reset"""
    user = await User.get_by_email(email)
    if user:
        reset_token = await user.create_password_reset_token()
        return {"status": "success", "message": "Password reset email sent"}
    
    return {"status": "success", "message": "If the email exists, a password reset link has been sent"}
