"""
Core functionality for the FlawFinder AI application.

This module contains the core components of the application,
including configuration, database connections, and security utilities.
"""

from .config import settings, get_settings
from .database import db, get_db
from .security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    generate_password_reset_token,
    verify_password_reset_token,
)

__all__ = [
    # Configuration
    'settings',
    'get_settings',
    
    # Database
    'db',
    'get_db',
    
    # Security
    'get_password_hash',
    'verify_password',
    'create_access_token',
    'create_refresh_token',
    'verify_token',
    'generate_password_reset_token',
    'verify_password_reset_token',
]