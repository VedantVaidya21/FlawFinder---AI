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
- **PostgreSQL**: Primary database with SQLAlchemy ORM
- **Redis**: Caching and Celery task queue
- **Neo4j**: Graph database for flow analysis
- **JWT Authentication**: Secure role-based access control
- **Prometheus Metrics**: Observability and monitoring
- **Docker**: Containerized deployment
- **Alembic**: Database migrations

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Task Queue**: Celery + Redis
- **Graph DB**: Neo4j
- **ML Libraries**: spaCy, Stanza, NetworkX
- **Monitoring**: Prometheus
- **Testing**: pytest + httpx
- **Documentation**: OpenAPI 3.1

## 📋 Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- PostgreSQL 15
- Redis 7
- Neo4j 5.15 (optional)

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

3. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb flawfinder_db
   
   # Run migrations
   alembic upgrade head
   ```

4. **Start Redis and Neo4j**
   ```bash
   # Using Docker for dependencies
   docker run -d -p 6379:6379 redis:7-alpine
   docker run -d -p 7474:7474 -p 7687:7687 neo4j:5.15
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
│   │   ├── database.py     # Database connection
│   │   ├── security.py     # JWT and password utilities
│   │   └── deps.py         # Dependency injection
│   ├── models/             # SQLAlchemy models
│   │   ├── base.py         # Base model
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
├── migrations/             # Alembic migrations
├── tests/                  # Test suite
├── docs/                   # Documentation
│   ├── openapi.yaml       # OpenAPI specification
│   └── api-matrix.md      # API mapping documentation
├── docker-compose.yml     # Docker services
├── Dockerfile             # Application container
├── requirements.txt       # Python dependencies
├── alembic.ini           # Alembic configuration
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

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://flawfinder:password@localhost:5432/flawfinder_db` |
| `JWT_SECRET` | JWT signing secret | `your-super-secret-jwt-key-change-in-production` |
| `JWT_EXPIRES_IN` | JWT expiration (minutes) | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:5173"]` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `NEO4J_URL` | Neo4j connection string | `bolt://localhost:7687` |
| `DEBUG` | Debug mode | `False` |

### Database Configuration

The application supports PostgreSQL with the following extensions:
- `uuid-ossp` for UUID generation
- `pg_trgm` for text search (optional)

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
   ```bash
   export DATABASE_URL="postgresql://user:pass@prod-db:5432/flawfinder"
   export JWT_SECRET="your-production-secret"
   export DEBUG=False
   ```

2. **Build and deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Run database migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

### Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests.

## 🔒 Security

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **CORS**: Configurable cross-origin requests
- **Rate Limiting**: Request throttling
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM

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

---

**Built with ❤️ using FastAPI, PostgreSQL, and modern Python practices** 