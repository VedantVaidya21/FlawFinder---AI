# FlawFinder AI - Backend

This is the backend service for the FlawFinder AI application, built with FastAPI and Neo4j.

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **Neo4j Database**: Graph database for efficient data relationships
- **RESTful API**: Clean, well-documented API endpoints
- **Async Support**: Built with async/await for better performance
- **Type Hints**: Full Python type hints for better developer experience

## Prerequisites

- Python 3.9+
- Neo4j 5.x (local or AuraDB)
- Poetry (for dependency management)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flawfinder-ai.git
cd flawfinder-ai/backend
```

### 2. Set Up Environment Variables

Copy the example environment file and update the values:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database
NEO4J_URI="neo4j://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your-password"
NEO4J_DATABASE="neo4j"

# Security
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. Install Dependencies

Using Poetry:

```bash
poetry install
```

Or using pip:

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

Run the initialization script to set up the database:

```bash
python -m scripts.init_app
```

### 5. Run the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Development

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting

Run the following commands before committing:

```bash
black .
isort .
flake8
```

### Testing

Run tests with pytest:

```bash
pytest
```

## Project Structure

```
backend/
├── app/
│   ├── api/               # API routes
│   ├── core/              # Core functionality
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic models
│   └── main.py            # FastAPI application
├── scripts/               # Utility scripts
├── tests/                 # Test files
├── .env.example           # Example environment variables
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Deployment

### Production

For production deployment, it's recommended to use:

1. Gunicorn with Uvicorn workers
2. A reverse proxy like Nginx
3. Process manager like systemd or Supervisor

Example Gunicorn command:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.