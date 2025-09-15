"""
Standalone Neo4j utilities for management scripts.
This module provides database connection and query execution without depending on the main app's settings.
"""
import os
from typing import Any, Dict, List, Optional
from neo4j import AsyncGraphDatabase, AsyncSession
from neo4j.exceptions import Neo4jError
import logging

logger = logging.getLogger(__name__)

class Neo4jConnection:
    """Manages Neo4j database connections."""
    
    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        """Initialize the Neo4j connection.
        
        Args:
            uri: Neo4j connection URI (e.g., 'neo4j://localhost:7687')
            user: Database username
            password: Database password
            database: Database name (default: 'neo4j')
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self.driver = None
    
    async def connect(self):
        """Establish a connection to the Neo4j database."""
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.uri, 
                auth=(self.user, self.password)
            )
            # Verify the connection
            await self.driver.verify_connectivity()
            logger.info(f"Connected to Neo4j database: {self.uri}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            await self.close()
            raise
    
    async def close(self):
        """Close the database connection."""
        if self.driver is not None:
            await self.driver.close()
            self.driver = None
            logger.info("Closed Neo4j connection")
    
    async def execute_query(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None,
        read_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return the results.
        
        Args:
            query: Cypher query string
            parameters: Dictionary of parameters for the query
            read_only: Whether the query is read-only (default: True)
            
        Returns:
            List of result records as dictionaries
        """
        if self.driver is None:
            raise RuntimeError("Database connection is not established")
        
        parameters = parameters or {}
        
        try:
            async with self.driver.session(database=self.database) as session:
                if read_only:
                    result = await session.execute_read(
                        self._execute_transaction,
                        query,
                        parameters
                    )
                else:
                    result = await session.execute_write(
                        self._execute_transaction,
                        query,
                        parameters
                    )
                return result
        except Neo4jError as e:
            logger.error(f"Neo4j error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    @staticmethod
    async def _execute_transaction(tx, query: str, parameters: Dict[str, Any]):
        """Execute a Cypher query within a transaction."""
        result = await tx.run(query, **parameters)
        return await result.data()

# Global connection instance
_connection = None

async def init_neo4j(uri: str = None, user: str = None, password: str = None, database: str = None):
    """Initialize the global Neo4j connection.
    
    Args:
        uri: Neo4j connection URI (default: from environment variable NEO4J_URI)
        user: Database username (default: from environment variable NEO4J_USER)
        password: Database password (default: from environment variable NEO4J_PASSWORD)
        database: Database name (default: from environment variable NEO4J_DATABASE or 'neo4j')
    """
    global _connection
    
    if _connection is not None:
        return _connection
    
    uri = uri or os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    user = user or os.getenv("NEO4J_USER", "neo4j")
    password = password or os.getenv("NEO4J_PASSWORD")
    database = database or os.getenv("NEO4J_DATABASE", "neo4j")
    
    if not password:
        raise ValueError("Database password is required")
    
    _connection = Neo4jConnection(uri, user, password, database)
    await _connection.connect()
    return _connection

async def close_neo4j():
    """Close the global Neo4j connection."""
    global _connection
    if _connection is not None:
        await _connection.close()
        _connection = None

async def execute_query(
    query: str, 
    parameters: Optional[Dict[str, Any]] = None,
    read_only: bool = True
) -> List[Dict[str, Any]]:
    """Execute a Cypher query using the global connection.
    
    Args:
        query: Cypher query string
        parameters: Dictionary of parameters for the query
        read_only: Whether the query is read-only (default: True)
        
    Returns:
        List of result records as dictionaries
    """
    if _connection is None:
        await init_neo4j()
    return await _connection.execute_query(query, parameters, read_only)
