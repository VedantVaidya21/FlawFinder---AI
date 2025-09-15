"""
Database connection and session management for Neo4j.
"""
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
import logging

from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from neo4j.exceptions import Neo4jError

from .config import settings

logger = logging.getLogger(__name__)


class Neo4jDatabase:
    """Neo4j database connection manager"""

    def __init__(self):
        self._driver: Optional[AsyncDriver] = None

    async def connect(self) -> None:
        """Connect to the Neo4j database"""
        try:
            # Normalize scheme: use bolt:// for single-instance servers
            uri = settings.NEO4J_URL
            if isinstance(uri, str) and uri.startswith("neo4j://"):
                logger.warning(
                    "NEO4J_URL uses 'neo4j://' scheme; switching to 'bolt://' for single-instance server"
                )
                uri = "bolt://" + uri[len("neo4j://"):]

            self._driver = AsyncGraphDatabase.driver(
                uri,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            )
            # Test the connection
            await self._driver.verify_connectivity()
            logger.info(f"Connected to Neo4j database: {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    async def close(self) -> None:
        """Close the database connection"""
        if self._driver is not None:
            await self._driver.close()
            self._driver = None
            logger.info("Closed Neo4j database connection")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session"""
        if self._driver is None:
            await self.connect()

        session = self._driver.session(database=settings.NEO4J_DATABASE)
        try:
            yield session
        except Neo4jError as e:
            logger.error(f"Neo4j error: {e}")
            raise
        finally:
            await session.close()

    async def __aenter__(self):
        if self._driver is None:
            await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def execute_query(self, query: str, **params) -> list:
        """Execute a read query and return results"""
        async with self.get_session() as session:
            result = await session.run(query, **params)
            return [record async for record in result]

    async def execute_write_query(self, query: str, **params) -> list:
        """Execute a write query and return results"""

        async def _tx(tx):
            result = await tx.run(query, **params)
            return [record async for record in result]

        async with self.get_session() as session:
            return await session.execute_write(_tx)


# Global database instance
db = Neo4jDatabase()

# For backward compatibility
get_db = db.get_session

# Convenience helper functions for imports
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.get_session() as session:
        yield session

async def close() -> None:
    await db.close()
