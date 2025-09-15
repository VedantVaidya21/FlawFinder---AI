# app/core/schema_setup.py
import logging
from typing import Optional
from neo4j import AsyncGraphDatabase
from neo4j.exceptions import ClientError

logger = logging.getLogger(__name__)

class SchemaManager:
    def __init__(self, driver: AsyncGraphDatabase.driver):
        self.driver = driver

    async def _execute_query(self, query: str, **params):
        async with self.driver.session() as session:
            try:
                await session.run(query, **params)
                return True
            except ClientError as e:
                logger.error(f"Error executing query: {e}")
                return False

    async def create_constraints(self):
        """Create all necessary constraints"""
        constraints = [
            # User constraints
            "CREATE CONSTRAINT user_username IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",
            "CREATE CONSTRAINT user_email IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE",
            
            # ProcessFlow constraints
            "CREATE CONSTRAINT process_flow_id IF NOT EXISTS FOR (p:ProcessFlow) REQUIRE p.id IS UNIQUE",
            
            # Flaw constraints
            "CREATE CONSTRAINT flaw_id IF NOT EXISTS FOR (f:Flaw) REQUIRE f.id IS UNIQUE",
            
            # Report constraints
            "CREATE CONSTRAINT report_id IF NOT EXISTS FOR (r:Report) REQUIRE r.id IS UNIQUE",
            
            # Fix constraints
            "CREATE CONSTRAINT fix_id IF NOT EXISTS FOR (f:Fix) REQUIRE f.id IS UNIQUE",
            
            # Score constraints
            "CREATE CONSTRAINT score_id IF NOT EXISTS FOR (s:Score) REQUIRE s.id IS UNIQUE"
        ]
        
        for constraint in constraints:
            await self._execute_query(constraint)

    async def create_indexes(self):
        """Create all necessary indexes"""
        indexes = [
            # Indexes for faster lookups
            "CREATE INDEX user_role IF NOT EXISTS FOR (u:User) ON (u.role)",
            "CREATE INDEX process_flow_created IF NOT EXISTS FOR (p:ProcessFlow) ON (p.created_at)",
            "CREATE INDEX flaw_severity IF NOT EXISTS FOR (f:Flaw) ON (f.severity)",
            "CREATE INDEX report_created IF NOT EXISTS FOR (r:Report) ON (r.created_at)"
        ]
        
        for index in indexes:
            await self._execute_query(index)

    async def initialize_schema(self):
        """Initialize the complete schema"""
        logger.info("Initializing Neo4j schema...")
        await self.create_constraints()
        await self.create_indexes()
        logger.info("Neo4j schema initialized successfully")

# Singleton instance
_schema_manager = None

async def init_schema(driver: AsyncGraphDatabase.driver):
    """Initialize the schema manager and create all constraints/indexes"""
    global _schema_manager
    if _schema_manager is None:
        _schema_manager = SchemaManager(driver)
        await _schema_manager.initialize_schema()
    return _schema_manager

async def get_schema_manager() -> Optional[SchemaManager]:
    """Get the schema manager instance"""
    return _schema_manager