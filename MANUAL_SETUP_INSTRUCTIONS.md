# FlawFinder AI - Manual Database Setup Instructions

If the automated setup script doesn't work, follow these manual instructions to set up the database infrastructure.

## Prerequisites

### 1. Install Required Software

#### Docker and Docker Compose
- **Windows**: Download Docker Desktop from https://www.docker.com/products/docker-desktop/
- **macOS**: Download Docker Desktop from https://www.docker.com/products/docker-desktop/
- **Linux**: Follow instructions at https://docs.docker.com/engine/install/

#### Python Dependencies
```bash
pip install psycopg2-binary redis neo4j
```

### 2. PostgreSQL Setup

#### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL container
docker run --name flawfinder-postgres \
  -e POSTGRES_DB=flawfinder_db \
  -e POSTGRES_USER=flawfinder \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15

# Wait for PostgreSQL to start (about 30 seconds)
docker logs flawfinder-postgres
```

#### Option B: Local PostgreSQL Installation
1. Install PostgreSQL 15+ from https://www.postgresql.org/download/
2. Create database and user:
```sql
-- Connect as postgres user
sudo -u postgres psql

-- Create database and user
CREATE DATABASE flawfinder_db;
CREATE USER flawfinder WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE flawfinder_db TO flawfinder;
\q
```

### 3. Redis Setup

#### Option A: Using Docker (Recommended)
```bash
# Start Redis container
docker run --name flawfinder-redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

#### Option B: Local Redis Installation
- **Windows**: Download from https://github.com/microsoftarchive/redis/releases
- **macOS**: `brew install redis && brew services start redis`
- **Linux**: `sudo apt-get install redis-server && sudo systemctl start redis`

### 4. Neo4j Setup

#### Option A: Using Docker (Recommended)
```bash
# Start Neo4j container
docker run --name flawfinder-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_PLUGINS='["apoc"]' \
  -d neo4j:5.15
```

#### Option B: Local Neo4j Installation
1. Download Neo4j Desktop from https://neo4j.com/download/
2. Create a new database with:
   - Username: `neo4j`
   - Password: `password`
   - Install APOC plugin

## Database Schema Setup

### 1. Create Database Schema

Run the SQL schema file:
```bash
# If using Docker PostgreSQL
docker exec -i flawfinder-postgres psql -U flawfinder -d flawfinder_db < database_setup.sql

# If using local PostgreSQL
psql -U flawfinder -d flawfinder_db -f database_setup.sql
```

### 2. Run Alembic Migrations

```bash
cd backend
alembic upgrade head
```

## Environment Configuration

### 1. Create .env File

Create `backend/.env` with the following content:

```env
# Database Configuration
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
```

## Verification

### 1. Test Database Connections

#### PostgreSQL
```bash
psql -U flawfinder -d flawfinder_db -c "SELECT version();"
```

#### Redis
```bash
redis-cli ping
# Should return: PONG
```

#### Neo4j
Open browser to http://localhost:7474
- Username: `neo4j`
- Password: `password`

### 2. Test Application

```bash
# Start backend
cd backend
python -m uvicorn app.main:app --reload

# In another terminal, start frontend
cd client
npm run dev
```

## Troubleshooting

### Common Issues

#### 1. PostgreSQL Connection Refused
- Check if PostgreSQL is running: `docker ps` or `systemctl status postgresql`
- Verify port 5432 is not blocked by firewall
- Check connection string in .env file

#### 2. Redis Connection Failed
- Check if Redis is running: `docker ps` or `redis-cli ping`
- Verify port 6379 is available

#### 3. Neo4j Connection Issues
- Wait for Neo4j to fully start (can take 1-2 minutes)
- Check Neo4j logs: `docker logs flawfinder-neo4j`
- Verify APOC plugin is installed

#### 4. Alembic Migration Errors
- Ensure database exists and user has proper permissions
- Check DATABASE_URL in .env file
- Try: `alembic current` to see current migration state

#### 5. Port Conflicts
If ports are already in use, modify the Docker commands:
```bash
# Use different ports
docker run --name flawfinder-postgres -p 5433:5432 ...
docker run --name flawfinder-redis -p 6380:6379 ...
docker run --name flawfinder-neo4j -p 7475:7474 -p 7688:7687 ...
```

Then update the .env file accordingly.

### Reset Everything

To start fresh:
```bash
# Stop and remove containers
docker stop flawfinder-postgres flawfinder-redis flawfinder-neo4j
docker rm flawfinder-postgres flawfinder-redis flawfinder-neo4j

# Remove volumes (this will delete all data!)
docker volume prune

# Start over with the setup process
```

## Production Considerations

For production deployment:

1. **Change default passwords** in all services
2. **Use environment variables** for sensitive configuration
3. **Set up SSL/TLS** for database connections
4. **Configure proper backup** strategies
5. **Set up monitoring** and logging
6. **Use connection pooling** for better performance
7. **Configure proper firewall rules**

## Support

If you encounter issues:
1. Check the logs: `docker logs <container-name>`
2. Verify all services are running: `docker ps`
3. Test connections individually
4. Check the application logs in the backend directory

For additional help, refer to the project documentation or create an issue in the repository.
