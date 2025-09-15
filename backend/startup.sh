#!/bin/bash

# Exit on error
set -e

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env <<EOL
# Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j

# App
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=11520
JWT_SECRET=your-jwt-secret-key
LOG_LEVEL=INFO
API_PREFIX=/api
EOL
    echo ".env file created. Please update the values as needed."
fi

# Start the application
echo "Starting the application..."
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
