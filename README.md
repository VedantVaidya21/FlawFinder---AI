# 🔍 FlawFinder AI

A modern SaaS platform for analyzing business workflows and detecting operational flaws using AI. Combines a React frontend with a FastAPI backend powered by Neo4j graph database.

## 🚀 Project Overview

### Frontend Features
- **Login & Authentication**: JWT-based authentication
- **Dashboard**: Brutality score indicator with charts
- **Upload System**: Document upload interface
- **Fix Plan**: View and manage suggested fixes
- **CEO Reports**: Executive-level summaries

### Backend Features
- **Process Flow Analysis**: NLP-based workflow analysis
- **Brutality Score**: Efficiency scoring system
- **Role-Based Access**: Customized views per user role
- **API Documentation**: OpenAPI/Swagger docs
- **Graph Database**: Neo4j-powered data relationships

## 🛠️ Tech Stack

### Frontend
- **Framework**: React (Vite)
- **UI**: Tailwind CSS
- **State**: React Context
- **Routing**: React Router
- **Components**:
  - Framer Motion (animations)
  - Chart.js (data visualization)
  - React Hot Toast (notifications)
  - React Dropzone (file uploads)

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: Neo4j 5.15+ (Graph Database)
- **Driver**: neo4j-driver 5.15+
- **Authentication**: JWT (python-jose)
- **Task Queue**: Celery + Redis
- **ML Libraries**: spaCy, Stanza, NetworkX

## 📦 Project Structure

```
/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core config & Neo4j connection
│   │   ├── models/        # Neo4j data models
│   │   └── schemas/       # Pydantic schemas
│   ├── neo4j-community-5.15.0/  # Local Neo4j instance
│   └── tests/            # Backend tests
├── client/               # React frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   └── contexts/     # React contexts
│   └── public/          # Static assets
└── docker-compose.yml   # Neo4j service configuration
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js v16+
- Neo4j 5.15+ (or Docker)
- Redis 7

### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Neo4j Database**

   **Option A: Using Docker (Recommended)**
   ```bash
   # Start Neo4j with Docker Compose
   docker-compose up -d neo4j

   # Wait for Neo4j to be ready (usually takes 30-60 seconds)
   # Default credentials: neo4j/neo4j (will prompt to change on first login)
   ```

   **Option B: Using Local Neo4j Installation**
   ```bash
   # If you have Neo4j installed locally, start the service
   # Windows: neo4j.bat start
   # Linux/Mac: neo4j start

   # Or use the provided setup script
   python setup_neo4j_local.py
   ```

4. **Setup environment**
   ```bash
   cp env.example .env
   # Edit .env with your Neo4j credentials
   ```

5. **Start the API**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd client
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Access the application**
   - Frontend: http://localhost:5173
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Neo4j Browser: http://localhost:7474 (if using local Neo4j)

## 🔐 Demo Access

Use these credentials for testing:
- **Email**: admin@flawfinder.ai
- **Password**: password123

## 📝 Environment Variables

### Backend (.env)
```
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-neo4j-password
NEO4J_DATABASE=neo4j

# Redis Configuration
REDIS_URL=redis://localhost:6379

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key

# CORS Configuration
CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🗄️ Neo4j Database Setup

### Initial Setup
1. **Access Neo4j Browser**: http://localhost:7474
2. **Login** with credentials from your `.env` file
3. **Create initial constraints** (optional but recommended):
   ```cypher
   CREATE CONSTRAINT user_email_unique FOR (u:User) REQUIRE u.email IS UNIQUE;
   CREATE CONSTRAINT organization_name_unique FOR (o:Organization) REQUIRE o.name IS UNIQUE;
   ```

### Database Schema
The application uses the following Neo4j node labels and relationships:
- **Nodes**: `User`, `Organization`, `ProcessFlow`, `Task`, `Report`, `Finding`, `BrutalityScore`
- **Relationships**: `BELONGS_TO`, `HAS_TASK`, `GENERATED_REPORT`, `HAS_FINDING`, etc.

### Backup & Restore
```bash
# Backup (using neo4j-admin)
neo4j-admin database dump neo4j --to-path=/path/to/backup

# Restore
neo4j-admin database load neo4j --from-path=/path/to/backup --overwrite-destination=true
```

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- CORS protection
- Input validation
- Cypher injection protection

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Neo4j Connection Test
```bash
cd backend
python test_import.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📚 Additional Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

**Built with ❤️ using React, FastAPI, and Neo4j graph database**
