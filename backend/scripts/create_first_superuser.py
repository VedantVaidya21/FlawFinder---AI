import asyncio
import logging
from typing import Optional

from app.core.config import settings
from app.models.user_neo4j import User, UserCreate, UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_first_superuser() -> Optional[User]:
    """Create the first superuser if it doesn't exist"""
    try:
        # Check if the superuser already exists
        existing_user = await User.get_by_email(settings.FIRST_SUPERUSER_EMAIL)
        if existing_user:
            logger.info("Superuser already exists. Skipping creation.")
            return None
        
        # Create the superuser
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="Initial Admin User",
            role=UserRole.ADMIN,
            is_active=True,
            email_verified=True
        )
        
        user = await user_in.create()
        logger.info(f"Created first superuser: {user.email}")
        return user
    
    except Exception as e:
        logger.error(f"Error creating first superuser: {e}")
        raise

if __name__ == "__main__":
    logger.info("Creating first superuser...")
    user = asyncio.run(create_first_superuser())
    if user:
        logger.info(f"Superuser created successfully: {user.email}")
    else:
        logger.info("Superuser creation skipped (already exists)")
