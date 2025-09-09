from typing import List, Optional
from pydantic import BaseModel, field_validator
import os


class Settings(BaseModel):
    # Application
    APP_NAME: str = "FlawFinder AI"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://flawfinder:password@localhost:5432/flawfinder_db")
    
    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_IN: int = 30  # minutes
    JWT_REFRESH_EXPIRES_IN: int = 1440  # minutes (24 hours)
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Neo4j
    NEO4J_URL: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    
    # Storage
    STORAGE_BUCKET: str = "flawfinder-storage"
    STORAGE_REGION: str = "us-east-1"
    STORAGE_ACCESS_KEY: Optional[str] = None
    STORAGE_SECRET_KEY: Optional[str] = None
    
    # ML Models
    SPACY_MODEL: str = "en_core_web_sm"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: str = "pdf,doc,docx,txt,png,jpg,jpeg,svg,json"
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @field_validator("ALLOWED_FILE_TYPES", mode="before")
    @classmethod
    def assemble_file_types(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 