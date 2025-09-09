from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import logging
from sqlalchemy import text

from .core.config import settings
from .db import engine, Base, SessionLocal
from .api import auth, flows, reports, agentops
from . import models  # ensure all models are registered
from .models.user import User, UserRole, UserStatus
from .core.security import get_password_hash

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="FlawFinder AI - The Ruthless Business & ML Critic",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(flows.router, prefix=settings.API_PREFIX)
app.include_router(reports.router, prefix=settings.API_PREFIX)
app.include_router(agentops.router, prefix=settings.API_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize database tables and seed demo user"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Seed demo user if none exists
        db = SessionLocal()
        try:
            if not db.query(User).first():
                demo = User(
                    email="admin@flawfinder.ai",
                    hashed_password=get_password_hash("password123"),
                    first_name="Admin",
                    last_name="User",
                    role=UserRole.ADMIN,
                    status=UserStatus.ACTIVE,
                )
                db.add(demo)
                db.commit()
                logger.info("Seeded demo user admin@flawfinder.ai / password123")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FlawFinder AI",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0"
    }


@app.get("/ping-db")
async def ping_db():
    """Ping database connection"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "connected", "database": "PostgreSQL"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": str(exc.status_code),
                "message": exc.detail,
                "details": None
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "500",
                "message": "Internal server error",
                "details": str(exc) if settings.DEBUG else None
            }
        }
    ) 