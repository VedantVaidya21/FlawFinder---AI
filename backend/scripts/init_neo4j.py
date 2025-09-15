import asyncio
import logging
from app.core.database import db
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constraints and indexes to create
CONSTRAINTS = [
    # User constraints
    "CREATE CONSTRAINT user_email IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE",
    "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
    
    # Add other constraints as needed for your domain models
    # Example:
    # "CREATE CONSTRAINT organization_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE",
]

INDEXES = [
    # Add any additional indexes for better query performance
    # Example:
    # "CREATE INDEX user_email_index IF NOT EXISTS FOR (u:User) ON (u.email)",
]

async def init_constraints():
    """Initialize all constraints in the Neo4j database"""
    logger.info("Creating constraints...")
    async with db.get_session() as session:
        for constraint in CONSTRAINTS:
            try:
                await session.run(constraint)
                logger.info(f"Created constraint: {constraint}")
            except Exception as e:
                logger.error(f"Error creating constraint {constraint}: {e}")
                raise

async def init_indexes():
    """Initialize all indexes in the Neo4j database"""
    logger.info("Creating indexes...")
    async with db.get_session() as session:
        for index in INDEXES:
            try:
                await session.run(index)
                logger.info(f"Created index: {index}")
            except Exception as e:
                logger.error(f"Error creating index {index}: {e}")
                raise

async def init_database():
    """Initialize the database with constraints and indexes"""
    try:
        # Connect to the database
        await db.connect()
        logger.info("Connected to Neo4j database")
        
        # Initialize constraints and indexes
        await init_constraints()
        await init_indexes()
        
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        # Ensure the connection is properly closed
        await db.close()
        logger.info("Disconnected from Neo4j database")

if __name__ == "__main__":
    logger.info("Starting database initialization...")
    asyncio.run(init_database())
