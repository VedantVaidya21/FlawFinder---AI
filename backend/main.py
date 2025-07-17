from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
from contextlib import asynccontextmanager

from db.database import engine, get_db
from db.models import Base
from routers import auth, upload, analyze, dashboard, fix_plan, report
from utils.auth import get_current_user
from utils.responses import create_response

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 FlawFinder AI Backend Starting...")
    yield
    # Shutdown
    print("🔥 FlawFinder AI Backend Shutting Down...")

app = FastAPI(
    title="FlawFinder AI",
    description="AI-powered business workflow analysis and flaw detection system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=create_response(
            success=False,
            message=f"Internal server error: {str(exc)}",
            data=None
        )
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return create_response(
        success=True,
        message="FlawFinder AI Backend is healthy",
        data={"status": "ok", "version": "1.0.0"}
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analysis"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(fix_plan.router, prefix="/api/fix-plan", tags=["Fix Plan"])
app.include_router(report.router, prefix="/api/report", tags=["Report"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
