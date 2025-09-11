from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import enum
from ..core.neo4j import get_neo4j


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    ENGINEER = "engineer"
    EXEC = "exec"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.ANALYST
    status: UserStatus = UserStatus.ACTIVE


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    hashed_password: Optional[str] = None


class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    organization_id: Optional[str] = None

    class Config:
        from_attributes = True


class UserService:
    """Neo4j data access layer for User operations"""

    @staticmethod
    def create_user(user_data: UserCreate) -> Optional[User]:
        """Create a new user in Neo4j"""
        neo4j_conn = get_neo4j()

        query = """
        CREATE (u:User {
            id: randomUUID(),
            email: $email,
            hashed_password: $hashed_password,
            first_name: $first_name,
            last_name: $last_name,
            role: $role,
            status: $status,
            created_at: datetime(),
            updated_at: datetime(),
            is_active: true
        })
        RETURN u
        """

        try:
            result = neo4j_conn.execute_query(query, {
                "email": user_data.email,
                "hashed_password": user_data.hashed_password,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "role": user_data.role.value,
                "status": user_data.status.value
            })

            if result:
                record = result[0]["u"]
                return User(
                    id=record["id"],
                    email=record["email"],
                    hashed_password=record["hashed_password"],
                    first_name=record.get("first_name"),
                    last_name=record.get("last_name"),
                    role=UserRole(record["role"]),
                    status=UserStatus(record["status"]),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error creating user: {e}")
        return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (u:User {email: $email, is_active: true})
        RETURN u
        """

        try:
            result = neo4j_conn.execute_query(query, {"email": email})
            if result:
                record = result[0]["u"]
                return User(
                    id=record["id"],
                    email=record["email"],
                    hashed_password=record["hashed_password"],
                    first_name=record.get("first_name"),
                    last_name=record.get("last_name"),
                    role=UserRole(record["role"]),
                    status=UserStatus(record["status"]),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting user by email: {e}")
        return None

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (u:User {id: $id, is_active: true})
        RETURN u
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": user_id})
            if result:
                record = result[0]["u"]
                return User(
                    id=record["id"],
                    email=record["email"],
                    hashed_password=record["hashed_password"],
                    first_name=record.get("first_name"),
                    last_name=record.get("last_name"),
                    role=UserRole(record["role"]),
                    status=UserStatus(record["status"]),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error getting user by ID: {e}")
        return None

    @staticmethod
    def update_user(user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        neo4j_conn = get_neo4j()

        # Build dynamic update query
        set_parts = ["u.updated_at = datetime()"]
        params = {"id": user_id}

        if user_data.email:
            set_parts.append("u.email = $email")
            params["email"] = user_data.email
        if user_data.first_name is not None:
            set_parts.append("u.first_name = $first_name")
            params["first_name"] = user_data.first_name
        if user_data.last_name is not None:
            set_parts.append("u.last_name = $last_name")
            params["last_name"] = user_data.last_name
        if user_data.role:
            set_parts.append("u.role = $role")
            params["role"] = user_data.role.value
        if user_data.status:
            set_parts.append("u.status = $status")
            params["status"] = user_data.status.value
        if user_data.hashed_password:
            set_parts.append("u.hashed_password = $hashed_password")
            params["hashed_password"] = user_data.hashed_password

        query = f"""
        MATCH (u:User {{id: $id, is_active: true}})
        SET {', '.join(set_parts)}
        RETURN u
        """

        try:
            result = neo4j_conn.execute_query(query, params)
            if result:
                record = result[0]["u"]
                return User(
                    id=record["id"],
                    email=record["email"],
                    hashed_password=record["hashed_password"],
                    first_name=record.get("first_name"),
                    last_name=record.get("last_name"),
                    role=UserRole(record["role"]),
                    status=UserStatus(record["status"]),
                    created_at=record["created_at"].to_native(),
                    updated_at=record["updated_at"].to_native(),
                    is_active=record["is_active"]
                )
        except Exception as e:
            print(f"Error updating user: {e}")
        return None

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Soft delete user by setting is_active to false"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (u:User {id: $id, is_active: true})
        SET u.is_active = false, u.updated_at = datetime()
        RETURN count(u) as deleted_count
        """

        try:
            result = neo4j_conn.execute_query(query, {"id": user_id})
            return result and result[0]["deleted_count"] > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
        return False

    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users with pagination"""
        neo4j_conn = get_neo4j()

        query = """
        MATCH (u:User {is_active: true})
        RETURN u
        ORDER BY u.created_at DESC
        SKIP $skip
        LIMIT $limit
        """

        try:
            result = neo4j_conn.execute_query(query, {"skip": skip, "limit": limit})
            users = []
            for record in result:
                user_data = record["u"]
                users.append(User(
                    id=user_data["id"],
                    email=user_data["email"],
                    hashed_password=user_data["hashed_password"],
                    first_name=user_data.get("first_name"),
                    last_name=user_data.get("last_name"),
                    role=UserRole(user_data["role"]),
                    status=UserStatus(user_data["status"]),
                    created_at=user_data["created_at"].to_native(),
                    updated_at=user_data["updated_at"].to_native(),
                    is_active=user_data["is_active"]
                ))
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
        return []
