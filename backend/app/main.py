from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import logging

from .core.config import settings
from .core.neo4j import neo4j_conn, close_neo4j_connection
from .api import auth, flows, reports, agentops
from .core.security import get_password_hash
import uuid
from datetime import datetime

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
    """Initialize database and seed demo user"""
    try:
        # Test Neo4j connection and seed demo user if none exists
        query = "MATCH (u:User {email: $email}) RETURN u"
        result = neo4j_conn.execute_query(query, {"email": "admin@flawfinder.ai"})

        if not result:
            # Create demo user
            user_id = str(uuid.uuid4())
            now = datetime.utcnow().isoformat()

            create_query = """
            CREATE (u:User {
                id: $id,
                email: $email,
                hashed_password: $hashed_password,
                first_name: $first_name,
                last_name: $last_name,
                role: $role,
                status: $status,
                is_active: $is_active,
                created_at: $created_at,
                updated_at: $updated_at
            })
            """

            neo4j_conn.execute_write_query(create_query, {
                "id": user_id,
                "email": "admin@flawfinder.ai",
                "hashed_password": get_password_hash("password123"),
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "status": "active",
                "is_active": True,
                "created_at": now,
                "updated_at": now
            })

            logger.info("Seeded demo user admin@flawfinder.ai / password123")

        logger.info("Neo4j database initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing Neo4j database: {e}")


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
        # Test Neo4j connection with a simple query
        result = neo4j_conn.execute_query("RETURN 'Neo4j connected' as message")
        if result:
            return {"status": "connected", "database": "Neo4j"}
        else:
            return {"status": "error", "error": "No response from Neo4j"}
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