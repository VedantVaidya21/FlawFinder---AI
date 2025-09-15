import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from app.core.config import settings
from app.core.database import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def init() -> None:
    """Initialize the application"""
    try:
        # Initialize the database
        logger.info("Initializing database...")
        await db.connect()
        
        # Import and run the database initialization script
        from scripts.init_neo4j import init_database
        await init_database()
        
        # Create the first superuser
        logger.info("Creating first superuser...")
        from scripts.create_first_superuser import create_first_superuser
        user = await create_first_superuser()
        
        if user:
            logger.info(f"Superuser created successfully: {user.email}")
        else:
            logger.info("Superuser creation skipped (already exists)")
            
        logger.info("Application initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during application initialization: {e}")
        raise
    finally:
        # Close the database connection
        await db.close()

def main():
    """Run the initialization script"""
    logger.info("Starting application initialization...")
    asyncio.run(init())
    logger.info("Initialization completed.")

if __name__ == "__main__":
    main()
