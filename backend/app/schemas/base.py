from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class BaseResponse(BaseSchema):
    """Base response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ErrorResponse(BaseSchema):
    """Error response schema"""
    error: dict 