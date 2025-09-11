# Neo4j database connection utilities
from neo4j import GraphDatabase
from .config import settings

# Create Neo4j driver
driver = GraphDatabase.driver(
    settings.NEO4J_URL,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)


def get_db():
    """Dependency to get Neo4j driver session"""
    session = driver.session()
    try:
        yield session
    finally:
        session.close()


def close_driver():
    """Close the Neo4j driver"""
    driver.close()
