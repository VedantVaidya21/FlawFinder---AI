# backend\app\core\config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache
import json
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application Settings
    PROJECT_NAME: str = "FlawFinder AI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")  # Change this in production
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days in minutes (60 * 24 * 7)
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    
    # CORS
    CORS_ORIGINS: List[str] = json.loads(os.getenv(
        "CORS_ORIGINS",
        "[\"http://localhost:3000\", \"http://localhost:5173\", \"http://localhost:8000\", \"http://127.0.0.1:3000\", \"http://127.0.0.1:5173\", \"http://127.0.0.1:8000\"]",
    ))
    
    # Neo4j Database (support both NEO4J_URL and NEO4J_URI)
    _NEO4J_URL_ENV: str = os.getenv("NEO4J_URL") or os.getenv("NEO4J_URI") or "bolt://localhost:7687"
    NEO4J_URL: str = _NEO4J_URL_ENV
    NEO4J_URI: str = _NEO4J_URL_ENV  # backward compatibility for existing imports
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    NEO4J_DATABASE: str = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Email Settings (for future use)
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "True").lower() == "true"
    SMTP_PORT: Optional[int] = int(os.getenv("SMTP_PORT")) if os.getenv("SMTP_PORT") else None
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: Optional[str] = os.getenv("EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: Optional[str] = os.getenv("EMAILS_FROM_NAME")
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = int(os.getenv("EMAIL_RESET_TOKEN_EXPIRE_HOURS", "48"))
    
    # First Superuser
    FIRST_SUPERUSER_EMAIL: str = os.getenv("FIRST_SUPERUSER_EMAIL", "admin@example.com")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "changethis")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()