from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import ValidationError
from ..core import security
from ..core.config import settings

# OAuth2 scheme for token authentication
oauth2_scheme = security.oauth2_scheme


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current authenticated user from the JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    
    from ..models.user_neo4j import get_user_by_email
    user = await get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user


async def require_exec_or_admin(current_user=Depends(get_current_user)):
    """Require executive or admin role"""
    if current_user.role not in ["exec", "admin", "ceo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_active_user(current_user=Depends(get_current_user)):
    """Get the current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_admin(current_user=Depends(get_current_user)):
    """Require admin role"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_active_analyst(current_user=Depends(get_current_user)):
    """Require analyst or admin role"""
    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
