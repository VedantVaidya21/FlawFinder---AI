from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .neo4j import get_neo4j
from .security import verify_token
from ..schemas.auth import TokenData

# Security scheme
security = HTTPBearer()


class User:
    """Neo4j-compatible User model"""
    def __init__(self, id, email, hashed_password, first_name=None, last_name=None,
                 role="analyst", status="active", organization_id=None, is_active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.status = status
        self.organization_id = organization_id
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at


def get_current_user(
    neo4j_conn = Depends(get_neo4j),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    # Query user from Neo4j
    query = """
    MATCH (u:User {id: $user_id, is_active: true})
    RETURN u.id as id, u.email as email, u.hashed_password as hashed_password,
           u.first_name as first_name, u.last_name as last_name, u.role as role,
           u.status as status, u.organization_id as organization_id,
           u.is_active as is_active, u.created_at as created_at, u.updated_at as updated_at
    """
    result = neo4j_conn.execute_query(query, {"user_id": user_id})

    if not result:
        raise credentials_exception

    user_data = result[0]
    user = User(**user_data)
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if current_user.status != "active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(required_role: str):
    """Require specific user role"""
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Require admin role"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_exec_or_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Require exec or admin role"""
    if current_user.role not in ["exec", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Executive or admin access required"
        )
    return current_user 