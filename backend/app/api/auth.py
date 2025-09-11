from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core.neo4j import get_neo4j
from ..core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from ..core.deps import get_current_active_user, User
from ..schemas.auth import UserLogin, UserRegister, Token, UserResponse
import uuid
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, neo4j_conn = Depends(get_neo4j)):
    """Register a new user"""
    # Check if user already exists
    query = "MATCH (u:User {email: $email}) RETURN u"
    existing_user = neo4j_conn.execute_query(query, {"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_data.password)
    now = datetime.utcnow().isoformat()

    create_query = """
    CREATE (u:User {
        id: $id,
        email: $email,
        hashed_password: $hashed_password,
        role: $role,
        status: $status,
        is_active: $is_active,
        created_at: $created_at,
        updated_at: $updated_at
    })
    RETURN u.id as id, u.email as email, u.hashed_password as hashed_password,
           u.first_name as first_name, u.last_name as last_name, u.role as role,
           u.status as status, u.organization_id as organization_id,
           u.is_active as is_active, u.created_at as created_at, u.updated_at as updated_at
    """

    result = neo4j_conn.execute_query(create_query, {
        "id": user_id,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "role": user_data.role,
        "status": "active",
        "is_active": True,
        "created_at": now,
        "updated_at": now
    })

    user_data = result[0]
    return User(**user_data)


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, neo4j_conn = Depends(get_neo4j)):
    """Login user and return access token"""
    # Find user by email
    query = """
    MATCH (u:User {email: $email, is_active: true})
    RETURN u.id as id, u.email as email, u.hashed_password as hashed_password,
           u.first_name as first_name, u.last_name as last_name, u.role as role,
           u.status as status, u.organization_id as organization_id,
           u.is_active as is_active, u.created_at as created_at, u.updated_at as updated_at
    """
    result = neo4j_conn.execute_query(query, {"email": user_credentials.email})

    if not result or not verify_password(user_credentials.password, result[0]["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_data = result[0]
    if user_data["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )

    # Create tokens
    access_token = create_access_token(data={"user_id": user_data["id"], "email": user_data["email"], "role": user_data["role"]})
    refresh_token = create_refresh_token(data={"user_id": user_data["id"]})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 30 * 60  # 30 minutes
    }


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, neo4j_conn = Depends(get_neo4j)):
    """Refresh access token using refresh token"""
    from ..core.security import verify_token

    payload = verify_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("user_id")

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    user_data = result[0]

    # Create new tokens
    access_token = create_access_token(data={"user_id": user_data["id"], "email": user_data["email"], "role": user_data["role"]})
    new_refresh_token = create_refresh_token(data={"user_id": user_data["id"]})

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": 30 * 60
    }


@router.post("/logout")
def logout():
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user 