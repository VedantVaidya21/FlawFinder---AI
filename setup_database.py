#!/usr/bin/env python3
"""
FlawFinder AI Database Setup Script
This script sets up the complete database infrastructure for the FlawFinder AI project.
"""

import os
import sys
import subprocess
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import redis
from neo4j import GraphDatabase
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseSetup:
    def __init__(self):
        self.postgres_config = {
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'password': 'password',
            'database': 'flawfinder_db'
        }
        
        self.redis_config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
        
        self.neo4j_config = {
            'uri': 'bolt://localhost:7687',
            'user': 'neo4j',
            'password': 'password'
        }

    def check_docker(self):
        """Check if Docker is running"""
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Docker is available")
                return True
            else:
                logger.error("Docker is not available")
                return False
        except FileNotFoundError:
            logger.error("Docker is not installed")
            return False

    def start_docker_services(self):
        """Start database services using Docker Compose"""
        logger.info("Starting database services with Docker Compose...")
        
        try:
            # Change to backend directory where docker-compose.yml is located
            os.chdir('backend')
            
            # Start services
            result = subprocess.run(['docker-compose', 'up', '-d', 'db', 'redis', 'neo4j'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Database services started successfully")
                return True
            else:
                logger.error(f"Failed to start services: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting Docker services: {e}")
            return False
        finally:
            # Change back to root directory
            os.chdir('..')

    def wait_for_postgres(self, max_retries=30):
        """Wait for PostgreSQL to be ready"""
        logger.info("Waiting for PostgreSQL to be ready...")
        
        for i in range(max_retries):
            try:
                conn = psycopg2.connect(
                    host=self.postgres_config['host'],
                    port=self.postgres_config['port'],
                    user=self.postgres_config['user'],
                    password=self.postgres_config['password'],
                    database='postgres'  # Connect to default database first
                )
                conn.close()
                logger.info("PostgreSQL is ready!")
                return True
            except psycopg2.OperationalError:
                logger.info(f"PostgreSQL not ready yet, waiting... ({i+1}/{max_retries})")
                time.sleep(2)
        
        logger.error("PostgreSQL failed to start within timeout")
        return False

    def setup_postgres_database(self):
        """Set up PostgreSQL database and schema"""
        logger.info("Setting up PostgreSQL database...")
        
        try:
            # Connect to PostgreSQL server
            conn = psycopg2.connect(
                host=self.postgres_config['host'],
                port=self.postgres_config['port'],
                user=self.postgres_config['user'],
                password=self.postgres_config['password'],
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.postgres_config['database'],))
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {self.postgres_config['database']}")
                logger.info(f"Created database: {self.postgres_config['database']}")
            
            # Create user if it doesn't exist
            cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", ('flawfinder',))
            if not cursor.fetchone():
                cursor.execute("CREATE USER flawfinder WITH PASSWORD 'password'")
                cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {self.postgres_config['database']} TO flawfinder")
                logger.info("Created user: flawfinder")
            
            cursor.close()
            conn.close()
            
            # Now connect to the new database and run schema
            self.run_sql_schema()
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up PostgreSQL: {e}")
            return False

    def run_sql_schema(self):
        """Run the SQL schema creation script"""
        logger.info("Creating database schema...")
        
        try:
            conn = psycopg2.connect(
                host=self.postgres_config['host'],
                port=self.postgres_config['port'],
                user=self.postgres_config['user'],
                password=self.postgres_config['password'],
                database=self.postgres_config['database']
            )
            cursor = conn.cursor()
            
            # Read and execute the SQL schema file
            with open('../database_setup.sql', 'r') as f:
                sql_content = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement.upper().startswith(('CREATE', 'INSERT', 'GRANT', 'ALTER')):
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        logger.warning(f"Warning executing statement: {e}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info("Database schema created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error creating schema: {e}")
            return False

    def test_redis_connection(self):
        """Test Redis connection"""
        logger.info("Testing Redis connection...")
        
        try:
            r = redis.Redis(**self.redis_config)
            r.ping()
            logger.info("Redis connection successful!")
            return True
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return False

    def test_neo4j_connection(self):
        """Test Neo4j connection"""
        logger.info("Testing Neo4j connection...")
        
        try:
            driver = GraphDatabase.driver(
                self.neo4j_config['uri'],
                auth=(self.neo4j_config['user'], self.neo4j_config['password'])
            )
            
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            
            driver.close()
            logger.info("Neo4j connection successful!")
            return True
        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            return False

    def create_env_file(self):
        """Create .env file with database configuration"""
        logger.info("Creating .env file...")
        
        env_content = """# Database Configuration
DATABASE_URL=postgresql://flawfinder:password@localhost:5432/flawfinder_db

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRES_IN=30
JWT_REFRESH_EXPIRES_IN=1440

# CORS Configuration
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Neo4j Configuration
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Storage Configuration
STORAGE_BUCKET=flawfinder-storage
STORAGE_REGION=us-east-1
STORAGE_ACCESS_KEY=your-access-key
STORAGE_SECRET_KEY=your-secret-key

# ML Model Configuration
SPACY_MODEL=en_core_web_sm

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
API_PREFIX=/api/v1

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES=pdf,doc,docx,txt,png,jpg,jpeg,svg,json
"""
        
        try:
            with open('backend/.env', 'w') as f:
                f.write(env_content)
            logger.info(".env file created successfully!")
            return True
        except Exception as e:
            logger.error(f"Error creating .env file: {e}")
            return False

    def run_alembic_migrations(self):
        """Run Alembic database migrations"""
        logger.info("Running Alembic migrations...")
        
        try:
            os.chdir('backend')
            
            # Run migrations
            result = subprocess.run(['alembic', 'upgrade', 'head'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Alembic migrations completed successfully!")
                return True
            else:
                logger.error(f"Alembic migrations failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error running migrations: {e}")
            return False
        finally:
            os.chdir('..')

    def setup_complete(self):
        """Run the complete database setup"""
        logger.info("Starting FlawFinder AI Database Setup...")
        
        # Check if Docker is available
        if not self.check_docker():
            logger.error("Docker is required but not available. Please install Docker and try again.")
            return False
        
        # Start Docker services
        if not self.start_docker_services():
            logger.error("Failed to start Docker services")
            return False
        
        # Wait for PostgreSQL
        if not self.wait_for_postgres():
            logger.error("PostgreSQL failed to start")
            return False
        
        # Set up PostgreSQL database
        if not self.setup_postgres_database():
            logger.error("Failed to set up PostgreSQL database")
            return False
        
        # Test Redis connection
        if not self.test_redis_connection():
            logger.error("Redis connection failed")
            return False
        
        # Test Neo4j connection
        if not self.test_neo4j_connection():
            logger.error("Neo4j connection failed")
            return False
        
        # Create .env file
        if not self.create_env_file():
            logger.error("Failed to create .env file")
            return False
        
        # Run Alembic migrations
        if not self.run_alembic_migrations():
            logger.error("Failed to run Alembic migrations")
            return False
        
        logger.info("🎉 Database setup completed successfully!")
        logger.info("You can now start the FlawFinder AI application.")
        
        return True

def main():
    """Main function"""
    setup = DatabaseSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
FlawFinder AI Database Setup Script

This script sets up the complete database infrastructure including:
- PostgreSQL database with schema
- Redis for caching and task queues
- Neo4j for graph analysis
- Environment configuration

Usage:
    python setup_database.py

Prerequisites:
    - Docker and Docker Compose installed
    - Python 3.11+ with required packages
    - Internet connection for downloading Docker images

The script will:
1. Start database services using Docker Compose
2. Create PostgreSQL database and schema
3. Test all database connections
4. Create environment configuration file
5. Run database migrations
        """)
        return
    
    success = setup.setup_complete()
    
    if success:
        print("\n✅ Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. Start the frontend: cd client && npm run dev")
        print("3. Access the application at http://localhost:5173")
    else:
        print("\n❌ Database setup failed. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
