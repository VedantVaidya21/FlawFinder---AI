#!/usr/bin/env python3
"""
Initialize the Neo4j database with constraints and an admin user.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import init_neo4j, close_neo4j, execute_query
from app.core.security import get_password_hash
from app.models.user import UserRole

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_admin_user():
    """Create an admin user if it doesn't exist."""
    # Check if admin user already exists
    result = await execute_query(
        "MATCH (u:User {email: $email}) RETURN u",
        {"email": settings.FIRST_SUPERUSER_EMAIL}
    )
    
    if result:
        logger.info("Admin user already exists")
        return
    
    # Create admin user
    admin_data = {
        "id": str(uuid.uuid4()),
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "hashed_password": get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        "first_name": "Admin",
        "last_name": "User",
        "is_active": True,
        "is_superuser": True,
        "role": UserRole.ADMIN.value,
    }
    
    await execute_query(
        """
        CREATE (u:User {
            id: $id,
            email: $email,
            hashed_password: $hashed_password,
            first_name: $first_name,
            last_name: $last_name,
            is_active: $is_active,
            is_superuser: $is_superuser,
            role: $role,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN u
        """,
        admin_data,
        read_only=False
    )
    
    logger.info(f"Created admin user: {settings.FIRST_SUPERUSER_EMAIL}")

async def main():
    """Main function to initialize the database."""
    try:
        # Initialize Neo4j connection
        await init_neo4j()
        
        # Create admin user
        await create_admin_user()
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        sys.exit(1)
    finally:
        # Close Neo4j connection
        await close_neo4j()

if __name__ == "__main__":
    import uuid  # Import here to avoid circular imports
    asyncio.run(main())
