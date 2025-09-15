"""
FlawFinder AI - Database Models

This module contains all the database models for the application.
It uses Neo4j as the primary database.
"""

# Import all models to ensure they are registered with the database
from .base_neo4j import BaseNode
from .user_neo4j import (
    User, UserCreate, UserUpdate, UserInDB,
    UserRole, UserStatus, authenticate_user
)
from .process_flow_neo4j import (
    ProcessFlow, ProcessFlowCreate, ProcessFlowResponse,
    FlowStatus
)
from .report_neo4j import (
    Report, ReportCreate, ReportResponse,
    ReportType, ReportStatus, CEOReportRequest
)

# Re-export models for easier imports
__all__ = [
    'BaseNode',
    'User',
    'UserCreate',
    'UserUpdate',
    'UserInDB',
    'UserRole',
    'UserStatus',
    'authenticate_user',
    'ProcessFlow',
    'ProcessFlowCreate',
    'ProcessFlowResponse',
    'FlowStatus',
    'Report',
    'ReportCreate',
    'ReportResponse',
    'ReportType',
    'ReportStatus',
    'CEOReportRequest',
]
