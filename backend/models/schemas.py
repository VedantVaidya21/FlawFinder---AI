from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

# Workflow Schemas
class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    raw_data: Dict[str, Any]
    file_type: str = Field(..., pattern="^(csv|json)$")

class WorkflowResponse(BaseModel):
    id: int
    name: str
    raw_data: Dict[str, Any]
    processed_data: Optional[Dict[str, Any]] = None
    file_type: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Flaw Schemas
class FlawCreate(BaseModel):
    workflow_id: int
    flaw_type: str
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    title: str
    description: str
    location: Optional[str] = None
    impact_score: float = Field(default=0.0, ge=0.0, le=10.0)

class FlawResponse(BaseModel):
    id: int
    workflow_id: int
    flaw_type: str
    severity: str
    title: str
    description: str
    location: Optional[str] = None
    impact_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Fix Suggestion Schemas
class FixSuggestionCreate(BaseModel):
    flaw_id: int
    title: str
    description: str
    implementation_effort: str = Field(..., pattern="^(low|medium|high)$")
    expected_impact: str = Field(..., pattern="^(low|medium|high)$")
    priority: int = Field(default=1, ge=1, le=5)
    estimated_time: Optional[str] = None

class FixSuggestionResponse(BaseModel):
    id: int
    flaw_id: int
    title: str
    description: str
    implementation_effort: str
    expected_impact: str
    priority: int
    estimated_time: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Report Schemas
class ReportCreate(BaseModel):
    workflow_id: int
    executive_summary: str
    total_flaws: int = 0
    critical_flaws: int = 0
    high_flaws: int = 0
    medium_flaws: int = 0
    low_flaws: int = 0
    brutality_score: float = Field(default=0.0, ge=0.0, le=10.0)
    improvement_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    recommendations: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    id: int
    workflow_id: int
    executive_summary: str
    total_flaws: int
    critical_flaws: int
    high_flaws: int
    medium_flaws: int
    low_flaws: int
    brutality_score: float
    improvement_percentage: float
    recommendations: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Analysis Schemas
class AnalysisRequest(BaseModel):
    workflow_id: int

class AnalysisResponse(BaseModel):
    workflow_id: int
    flaws: List[FlawResponse]
    fix_suggestions: List[FixSuggestionResponse]
    brutality_score: float
    total_flaws: int
    processing_time: float
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_workflows: int
    total_flaws: int
    avg_brutality_score: float
    recent_workflows: List[WorkflowResponse]
    flaw_distribution: Dict[str, int]
    severity_distribution: Dict[str, int]
    
    class Config:
        from_attributes = True

# Upload Schemas
class UploadResponse(BaseModel):
    workflow_id: int
    message: str
    parsed_data: Dict[str, Any]
    
    class Config:
        from_attributes = True

# Standard API Response
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
