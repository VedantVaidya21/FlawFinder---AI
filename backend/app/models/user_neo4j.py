from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import EmailStr, Field, validator, field_validator
from passlib.context import CryptContext
from neo4j.time import DateTime as Neo4jDateTime
from .base_neo4j import BaseNode

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Enums ---
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    ANALYST = "analyst"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


# --- Base User ---
class UserBase(BaseNode):
    """Base user model with common fields"""
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
    is_active: bool = True
    email_verified: bool = False
    last_login: Optional[datetime] = None

    # 🔥 Neo4j datetime conversion
    @field_validator("last_login", mode="before")
    def convert_neo4j_datetime(cls, v):
        if isinstance(v, Neo4jDateTime):
            return datetime(
                year=v.year,
                month=v.month,
                day=v.day,
                hour=v.hour,
                minute=v.minute,
                second=v.second,
                microsecond=v.nanosecond // 1000,
                tzinfo=v.tzinfo,
            )
        return v

    class Config:
        json_encoders = {
            **BaseNode.Config.json_encoders,
        }


# --- DB User ---
class UserInDB(UserBase, BaseNode):
    """User model with database-specific fields"""
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 🔥 Neo4j datetime conversion
    @field_validator("created_at", "updated_at", mode="before")
    def convert_neo4j_datetime(cls, v):
        if isinstance(v, Neo4jDateTime):
            return datetime(
                year=v.year,
                month=v.month,
                day=v.day,
                hour=v.hour,
                minute=v.minute,
                second=v.second,
                microsecond=v.nanosecond // 1000,
                tzinfo=v.tzinfo,
            )
        return v

    class Config:
        json_encoders = {
            **BaseNode.Config.json_encoders,
            datetime: lambda v: v.isoformat() if v else None,
        }


# --- Create User ---
class UserCreate(UserBase):
    """Model for user creation"""
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    async def create(self) -> "User":
        """Create a new user with hashed password"""
        hashed_password = pwd_context.hash(self.password)
        user_data = self.dict(exclude={"password"}, exclude_unset=True)
        user_data["hashed_password"] = hashed_password

        # Create the user in the database
        user = UserInDB(**user_data)
        await user.save()

        # Return a User instance (without hashed_password, timestamps)
        return User(
            **user.dict(
                exclude={"hashed_password", "created_at", "updated_at"},
                exclude_unset=True,
            )
        )


# --- Update User ---
class UserUpdate(BaseNode):
    """Model for updating user data"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

    async def update(self, user: "User") -> "User":
        """Update user data"""
        update_data = self.dict(exclude_unset=True, exclude_none=True)

        if "password" in update_data:
            update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        await user.save()
        return user


# --- Main User ---
class User(UserBase):
    """Main user model with authentication methods. Does not require hashed_password for API output."""
    hashed_password: Optional[str] = None
    # Query against the stored label created via UserInDB
    label_name: str | None = "UserInDB"

    # 🔥 Neo4j datetime conversion
    @field_validator("created_at", "updated_at", "last_login", mode="before")
    def convert_neo4j_datetime(cls, v):
        if isinstance(v, Neo4jDateTime):
            return datetime(
                year=v.year,
                month=v.month,
                day=v.day,
                hour=v.hour,
                minute=v.minute,
                second=v.second,
                microsecond=v.nanosecond // 1000,
                tzinfo=v.tzinfo,
            )
        return v

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        """Get user by email"""
        return await cls.find_one(email=email)

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return pwd_context.verify(password, self.hashed_password)

    async def update_last_login(self) -> None:
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        await self.save()

    async def change_password(self, current_password: str, new_password: str) -> bool:
        """Change user password"""
        if not self.verify_password(current_password):
            return False

        self.hashed_password = pwd_context.hash(new_password)
        await self.save()
        return True

    async def create_password_reset_token(self) -> str:
        """Create a password reset token"""
        # In a real app, implement JWT token generation
        return "reset_token_placeholder"

    @classmethod
    def from_orm(cls, node_data: Dict[str, Any]) -> "User":
        """Create a User instance from Neo4j node data"""
        return cls(**node_data)


# --- Helper function ---
async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user"""
    user = await User.get_by_email(email)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    if not user.is_active:
        return None

    await user.update_last_login()
    return user
