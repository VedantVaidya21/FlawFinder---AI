from typing import Optional
from pydantic import BaseModel, EmailStr
from .base import BaseSchema


class UserLogin(BaseSchema):
    """User login request schema"""
    email: EmailStr
    password: str


class UserRegister(BaseSchema):
    """User registration request schema"""
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = "analyst"


class Token(BaseSchema):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseSchema):
    """Token data schema"""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


class UserResponse(BaseSchema):
    """User response schema"""
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    status: str
    organization_id: Optional[int] = None  