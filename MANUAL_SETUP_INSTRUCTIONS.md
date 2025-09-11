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
pip install neo4j redis
```

### 2. Neo4j Setup

#### Option A: Using Docker (Recommended)
```bash
# Start Neo4j container
docker run --name flawfinder-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_PLUGINS='["apoc"]' \
  -d neo4j:5.15

# Wait for Neo4j to start (about 30-60 seconds)
docker logs flawfinder-neo4j
```

#### Option B: Local Neo4j Installation
1. Download Neo4j Desktop from https://neo4j.com/download/
2. Create a new database with:
   - Username: `neo4j`
   - Password: `password`
   - Install APOC plugin

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

## Database Schema Setup

### 1. Create Initial Constraints

Access Neo4j Browser at http://localhost:7474 and run these Cypher commands:

```cypher
// Create unique constraints
CREATE CONSTRAINT user_email_unique FOR (u:User) REQUIRE u.email IS UNIQUE;
CREATE CONSTRAINT organization_name_unique FOR (o:Organization) REQUIRE o.name IS UNIQUE;

// Create indexes for better performance
CREATE INDEX user_id_index FOR (u:User) ON (u.id);
CREATE INDEX organization_id_index FOR (o:Organization) ON (o.id);
CREATE INDEX process_flow_id_index FOR (pf:ProcessFlow) ON (pf.id);
```

### 2. Verify Neo4j Connection

```bash
cd backend
python test_import.py
```

## Environment Configuration

### 1. Create .env File

Create `backend/.env` with the following content:

```env
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRES_IN=30
JWT_REFRESH_EXPIRES_IN=1440

# CORS Configuration
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Redis Configuration
REDIS_URL=redis://localhost:6379

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

#### Neo4j
Open browser to http://localhost:7474
- Username: `neo4j`
- Password: `password`

Test basic Cypher query:
```cypher
MATCH (n) RETURN count(n) as node_count;
```

#### Redis
```bash
redis-cli ping
# Should return: PONG
```

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

#### 1. Neo4j Connection Refused
- Check if Neo4j is running: `docker ps` or Neo4j Desktop
- Verify port 7687 (Bolt) and 7474 (Browser) are not blocked by firewall
- Check NEO4J_URI in .env file

#### 2. Redis Connection Failed
- Check if Redis is running: `docker ps` or `redis-cli ping`
- Verify port 6379 is available

#### 3. Neo4j APOC Plugin Issues
- Wait for Neo4j to fully start (can take 1-2 minutes)
- Check Neo4j logs: `docker logs flawfinder-neo4j`
- Verify APOC plugin is installed and enabled

#### 4. Cypher Query Errors
- Check Neo4j Browser for syntax errors
- Ensure constraints are created before running queries
- Verify data types match expected formats

#### 5. Port Conflicts
If ports are already in use, modify the Docker commands:
```bash
# Use different ports
docker run --name flawfinder-neo4j -p 7475:7474 -p 7688:7687 ...
docker run --name flawfinder-redis -p 6380:6379 ...
```

Then update the .env file accordingly.

### Reset Everything

To start fresh:
```bash
# Stop and remove containers
docker stop flawfinder-neo4j flawfinder-redis
docker rm flawfinder-neo4j flawfinder-redis

# Remove volumes (this will delete all data!)
docker volume prune

# Start over with the setup process
```

## Production Considerations

For production deployment:

1. **Change default passwords** in all services
2. **Use environment variables** for sensitive configuration
3. **Set up SSL/TLS** for Neo4j connections
4. **Configure proper backup** strategies
5. **Set up monitoring** and logging
6. **Configure proper firewall rules**
7. **Use Neo4j clustering** for high availability

## Neo4j Best Practices

### Performance Optimization
- Create appropriate indexes on frequently queried properties
- Use EXPLAIN and PROFILE to analyze query performance
- Consider using Neo4j's query planner hints

### Data Modeling
- Design your graph schema based on your query patterns
- Use meaningful relationship types
- Consider using labels for different entity types

### Backup and Recovery
```bash
# Create backup
neo4j-admin database dump neo4j --to-path=/path/to/backup

# Restore from backup
neo4j-admin database load neo4j --from-path=/path/to/backup --overwrite-destination=true
```

## Support

If you encounter issues:
1. Check the logs: `docker logs <container-name>`
2. Verify all services are running: `docker ps`
3. Test connections individually
4. Check the application logs in the backend directory

For additional help, refer to the project documentation or create an issue in the repository.
