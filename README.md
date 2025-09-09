# 🔍 FlawFinder AI

A modern SaaS platform for analyzing business workflows and detecting operational flaws using AI. Combines a React frontend with a FastAPI backend.

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
- **Database Migrations**: Alembic-managed schemas

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
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Task Queue**: Celery + Redis
- **ML Libraries**: spaCy, Stanza, NetworkX

## 📦 Project Structure

```
/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core config
│   │   ├── models/        # SQLAlchemy models
│   │   └── schemas/       # Pydantic schemas
│   ├── migrations/        # Alembic migrations
│   └── tests/            # Backend tests
├── client/               # React frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   └── contexts/     # React contexts
│   └── public/          # Static assets
└── database_setup.sql   # Database init script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js v16+
- PostgreSQL 15
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

3. **Setup environment**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

4. **Run migrations**
   ```bash
   alembic upgrade head
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

## 🔐 Demo Access

Use these credentials for testing:
- **Email**: admin@flawfinder.ai
- **Password**: password123

## 📝 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://flawfinder:password@localhost:5432/flawfinder_db
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-super-secret-jwt-key
CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- CORS protection
- Input validation
- SQL injection protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Built with ❤️ using React, FastAPI, and modern web technologies**
