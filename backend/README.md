# 🔍 FlawFinder AI Backend

The Ruthless Business & ML Critic - Production-ready FastAPI backend for analyzing business workflows and detecting operational flaws using AI.

## 🚀 Features

### Core Functionality
- **Process Flow Ingestion**: Accept natural language text or uploaded diagrams
- **Flow Parsing & Detection**: NLP + graph extraction with flaw detection
- **Brutality Score**: Compute efficiency scores with detailed breakdowns
- **CEO Reports**: Generate executive-level summaries and recommendations
- **Role-Based Fixes**: Tailored action lists per user role (Engineer, Ops, Data, Exec)
- **AgentOps Plugin**: ML pipeline monitoring, drift detection, and autonomous retraining

### Technical Features
- **FastAPI**: High-performance async API framework
- **Neo4j**: Graph database for flow analysis and complex relationships
- **Redis**: Caching and Celery task queue
- **JWT Authentication**: Secure role-based access control
- **Prometheus Metrics**: Observability and monitoring
- **Docker**: Containerized deployment

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+
- **Database**: Neo4j 5.15+ (Graph Database)
- **Driver**: neo4j-driver 5.15+
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Task Queue**: Celery + Redis
- **Graph Analysis**: NetworkX
- **ML Libraries**: spaCy, Stanza
- **Monitoring**: Prometheus
- **Testing**: pytest + httpx
- **Documentation**: OpenAPI 3.1

## 📋 Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Neo4j 5.15 (optional)
- Redis 7

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FlawFinder---AI/backend
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start the entire stack**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Neo4j Browser: http://localhost:7474
   - Redis Commander: http://localhost:8081

### Option 2: Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Neo4j Database**
   ```bash
   # Using Docker for Neo4j
   docker run -d \
     --name flawfinder-neo4j \
     -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/password \
     -e NEO4J_PLUGINS='["apoc"]' \
     neo4j:5.15

   # Wait for Neo4j to start (usually takes 30-60 seconds)
   ```

4. **Start Redis**
   ```bash
   # Using Docker for Redis
   docker run -d \
     --name flawfinder-redis \
     -p 6379:6379 \
     redis:7-alpine
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/                 # API routers
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── flows.py        # Process flow endpoints
│   │   ├── reports.py      # Report generation endpoints
│   │   └── agentops.py     # ML pipeline endpoints
│   ├── core/               # Core configuration
│   │   ├── config.py       # Settings and configuration
│   │   ├── neo4j.py        # Neo4j connection and utilities
│   │   ├── deps.py         # Dependency injection
│   │   └── security.py     # JWT and password utilities
│   ├── models/             # Neo4j data models
│   │   ├── base.py         # Base model patterns
│   │   ├── user.py         # User model
│   │   ├── process_flow.py # Process flow model
│   │   ├── finding.py      # Finding model
│   │   ├── report.py       # Report model
│   │   ├── task.py         # Task model
│   │   └── agentops.py     # ML pipeline models
│   ├── schemas/            # Pydantic schemas
│   │   ├── base.py         # Base schemas
│   │   ├── auth.py         # Auth schemas
│   │   ├── flow.py         # Flow schemas
│   │   ├── report.py       # Report schemas
│   │   └── agentops.py     # AgentOps schemas
│   ├── services/           # Business logic
│   ├── workers/            # Celery tasks
│   ├── integrations/       # External integrations
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── docs/                   # Documentation
│   ├── openapi.yaml       # OpenAPI specification
│   └── api-matrix.md      # API mapping documentation
├── docker-compose.yml     # Docker services
├── Dockerfile             # Application container
├── requirements.txt       # Python dependencies
├── setup_neo4j_local.py   # Neo4j local setup script
└── README.md             # This file
```

## 🔐 Authentication

The API uses JWT-based authentication with role-based access control:

### User Roles
- **Admin**: Full system access
- **Analyst**: View and analyze flows
- **Engineer**: Technical implementation
- **Exec**: Executive-level access

### Demo Credentials
```
Email: admin@flawfinder.ai
Password: password123
```

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

### Process Flows
- `POST /api/v1/flows` - Create new flow
- `GET /api/v1/flows` - List user's flows
- `GET /api/v1/flows/{id}` - Get flow details
- `POST /api/v1/flows/{id}/parse` - Parse flow
- `GET /api/v1/flows/{id}/score` - Get brutality score
- `GET /api/v1/flows/{id}/fixes` - Get role-based fixes

### Reports
- `POST /api/v1/reports/ceo` - Generate CEO report
- `GET /api/v1/reports` - List reports
- `GET /api/v1/reports/{id}` - Get report details
- `GET /api/v1/reports/{id}/download` - Download report

### AgentOps
- `POST /api/v1/agentops/pipelines` - Register ML pipeline
- `GET /api/v1/agentops/pipelines` - List pipelines
- `POST /api/v1/agentops/pipelines/{id}/monitor` - Monitor drift
- `POST /api/v1/agentops/pipelines/{id}/retrain` - Trigger retraining
- `GET /api/v1/agentops/pipelines/{id}/status` - Get pipeline status

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v
```

## 📈 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEO4J_URI` | Neo4j connection string | `bolt://localhost:7687` |
| `NEO4J_USER` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | `password` |
| `NEO4J_DATABASE` | Neo4j database name | `neo4j` |
| `JWT_SECRET` | JWT signing secret | `your-super-secret-jwt-key-change-in-production` |
| `JWT_EXPIRES_IN` | JWT expiration (minutes) | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:5173"]` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `DEBUG` | Debug mode | `False` |`

### Neo4j Configuration

The application connects to Neo4j using the following patterns:
- **Connection**: Bolt protocol (bolt://localhost:7687)
- **Authentication**: Username/password
- **Database**: Default 'neo4j' database
- **Constraints**: Unique constraints on User.email and Organization.name

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
   ```bash
   export NEO4J_URI="bolt://prod-neo4j:7687"
   export NEO4J_USER="neo4j"
   export NEO4J_PASSWORD="your-production-password"
   export JWT_SECRET="your-production-secret"
   export DEBUG=False
   ```

2. **Build and deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests.

## 🔒 Security

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **CORS**: Configurable cross-origin requests
- **Rate Limiting**: Request throttling
- **Input Validation**: Pydantic schema validation
- **Cypher Injection Protection**: Parameterized queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Issues**: GitHub Issues
- **Email**: support@flawfinder.ai

## 🔄 Changelog

### v1.0.0
- Initial release
- Core API endpoints
- Authentication system
- Process flow analysis
- CEO report generation
- AgentOps integration
- Neo4j graph database integration

---

**Built with ❤️ using FastAPI, Neo4j, and modern Python practices**
