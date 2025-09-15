# API routers 
from fastapi import APIRouter

# Import all routers
from . import auth, flows, reports

# Create main API router
api_router = APIRouter()

# Include all API routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(flows.router, prefix="/flows", tags=["flows"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])