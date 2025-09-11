# backend/app/db.py
from .core.neo4j import neo4j_conn

# Dependency for FastAPI endpoints
def get_db():
    """Dependency to get Neo4j session"""
    session = neo4j_conn.driver.session()
    try:
        yield session
    finally:
        session.close()
