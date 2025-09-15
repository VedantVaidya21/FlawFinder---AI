import asyncio
import os
from dotenv import load_dotenv
from app.core.database import get_neo4j_driver, close_neo4j_driver
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_neo4j_connection():
    """Test Neo4j database connection"""
    try:
        driver = await get_neo4j_driver()
        async with driver.session() as session:
            result = await session.run("RETURN 'Neo4j Connection Successful' AS message")
            record = await result.single()
            logger.info(f"Neo4j: {record['message']}")
        return True
    except Exception as e:
        logger.error(f"Neo4j connection failed: {e}")
        return False
    finally:
        await close_neo4j_driver()

async def main():
    load_dotenv()

    logger.info("Testing database connections...")

    # Test Neo4j connection
    neo4j_success = await test_neo4j_connection()

    # Print summary
    logger.info("\n=== Connection Test Results ===")
    logger.info(f"Neo4j: {'✅ Success' if neo4j_success else '❌ Failed'}")

if __name__ == "__main__":
    asyncio.run(main())
