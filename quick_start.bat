@echo off
REM FlawFinder AI - Quick Start Script for Windows
REM This script provides a quick way to set up and start the FlawFinder AI application

echo 🚀 FlawFinder AI - Quick Start Setup
echo ====================================
echo.

REM Check if Docker is installed and running
echo [INFO] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)
echo [SUCCESS] Docker is installed and running

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.11+ first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [SUCCESS] Python is installed

REM Check if Node.js is installed
echo [INFO] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js first.
    echo Visit: https://nodejs.org/
    pause
    exit /b 1
)
echo [SUCCESS] Node.js is installed

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements_setup.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python setup dependencies
    pause
    exit /b 1
)

cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..
echo [SUCCESS] Python dependencies installed

REM Install Node.js dependencies
echo [INFO] Installing Node.js dependencies...
cd client
npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)
cd ..
echo [SUCCESS] Node.js dependencies installed

REM Set up database
echo [INFO] Setting up database...
python setup_database.py
if %errorlevel% neq 0 (
    echo [ERROR] Database setup failed. Please check the manual setup instructions.
    pause
    exit /b 1
)
echo [SUCCESS] Database setup completed

REM Start the application
echo [INFO] Starting FlawFinder AI application...
echo.

REM Start backend in background
echo [INFO] Starting backend server...
cd backend
start "FlawFinder Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
cd ..

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend
echo [INFO] Starting frontend server...
cd client
start "FlawFinder Frontend" cmd /k "npm run dev"
cd ..

echo.
echo [SUCCESS] Application started successfully!
echo.
echo 🌐 Application URLs:
echo    Frontend: http://localhost:5173
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📊 Database Services:
echo    PostgreSQL: localhost:5432
echo    Redis: localhost:6379
echo    Neo4j: http://localhost:7474
echo.
echo 🔑 Default Login Credentials:
echo    Email: admin@flawfinder.ai
echo    Password: admin123
echo.
echo Press any key to exit...
pause >nul
