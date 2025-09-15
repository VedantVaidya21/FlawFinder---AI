from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from ..core.config import settings
from ..models.user_neo4j import User
from ..models.token import TokenData

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency to get the current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = await User.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to get the current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to check if current user is a superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

# Common role-based permission dependencies
def _normalize_role(role_value) -> str:
    try:
        # Handle Enum-like values
        return role_value.value.lower()
    except AttributeError:
        return str(role_value).lower()


def require_role(required_roles: list):
    """Dependency factory for role-based access control"""
    required = {str(r).lower() for r in required_roles}

    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        user_role = _normalize_role(current_user.role)
        if user_role not in required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User doesn't have required role. Required: {sorted(required)}",
            )
        return current_user

    return role_checker

# Common permission dependencies
require_admin = require_role(["admin"])
require_analyst = require_role(["analyst", "admin"])
require_any_auth = require_role(["user", "analyst", "admin"])

# Backward-compatible alias used by reports API
require_exec_or_admin = require_role(["analyst", "admin"])
