from neo4j import GraphDatabase
from .config import settings


class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URL,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        """Execute a Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record for record in result]

    def execute_write_query(self, query, parameters=None):
        """Execute a write Cypher query"""
        with self.driver.session() as session:
            session.run(query, parameters or {})


# Global Neo4j connection instance
neo4j_conn = Neo4jConnection()


def get_neo4j():
    """Dependency to get Neo4j connection"""
    return neo4j_conn


def close_neo4j_connection():
    """Close the Neo4j connection"""
    neo4j_conn.close()
